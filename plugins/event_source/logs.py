"""
logs.py

An ansible-rulebook event source module for receiving events via a webhook from
PAN-OS firewall or Panorama appliance.

Arguments:
    host: The webserver hostname to listen to. Set to 0.0.0.0 to listen on all
          interfaces. Defaults to 127.0.0.1
    port: The TCP port to listen to.  Defaults to 5000

Example:

    - paloaltonetworks.panos.logs:
        host: 0.0.0.0
        port: 5000
        type: decryption
"""

import asyncio
import logging
from typing import Any, Dict

from aiohttp import web
from dpath import util

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

routes = web.RouteTableDef()


@routes.get("/")
async def status(request: web.Request):
    """Return a simple status response."""
    return web.Response(status=200, text="up")


@routes.post("/{endpoint}")
async def webhook(request: web.Request):
    """
    Handle webhook requests.

    Process the incoming JSON payload and forward it to the event queue
    if it matches the configured log type.
    """
    try:
        payload = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse JSON payload: {e}")
        return web.Response(status=400, text="Invalid JSON payload")

    if request.app["type"] == "decryption":
        log_type = payload.get("type", "log_type")
        if log_type != "decryption":
            log_type = "log_type"

        data = process_payload(request, payload, log_type)
        await request.app["queue"].put(data)

    return web.Response(
        status=202, text=str({"status": "received", "payload": "happy"})
    )


def process_payload(request, payload, log_type):
    """
    Process the payload and extract the necessary information.

    :param request: The incoming webhook request.
    :param payload: The JSON payload from the request.
    :param log_type: The log type to filter events.
    :return: A dictionary containing the processed payload and metadata.
    """
    try:
        device_name = util.get(payload, "details.device_name", separator=".")
        data = {
            "payload": payload,
            "meta": {
                "device_name": device_name,
                "endpoint": request.match_info["endpoint"],
                "headers": dict(request.headers),
                "log_type": log_type,
            },
        }
    except KeyError:
        logger.warning("KeyError occurred while processing the payload")
        data = {
            "payload": payload,
            "meta": {
                "message": "processing failed, check key names",
                "headers": dict(request.headers),
            },
        }
    return data


async def main(queue: asyncio.Queue, args: Dict[str, Any], logger=None):
    """
    Main function to run the plugin as a standalone application.

    :param queue: The event queue to forward incoming events to.
    :param args: A dictionary containing configuration arguments.
    :param logger: An optional custom logger.
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    app = web.Application()
    app["queue"] = queue
    app["type"] = str(args.get("type", "decryption"))

    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(
        runner,
        args.get("host", "localhost"),
        args.get("port", 5000),
    )
    await site.start()

    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        logger.info("Plugin Task Cancelled")
    finally:
        await runner.cleanup()


if __name__ == "__main__":

    class MockQueue:
        async def put(self, event):
            print(event)

    asyncio.run(main(MockQueue(), {}))
