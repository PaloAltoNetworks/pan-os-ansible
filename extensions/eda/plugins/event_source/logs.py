#  Copyright 2023 Palo Alto Networks, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""An ansible-rulebook event source module.

An ansible-rulebook event source module for receiving events via a webhook from
PAN-OS firewall or Panorama appliance.

Arguments:
---------
    host: The webserver hostname to listen to. Set to 0.0.0.0 to listen on all
          interfaces. Defaults to 127.0.0.1
    port: The TCP port to listen to.  Defaults to 5000

Example:
-------
    - paloaltonetworks.panos.logs:
        host: 0.0.0.0
        port: 5000
        type: decryption


"""

# ruff: noqa: UP001, UP010
from __future__ import absolute_import, division, print_function

# pylint: disable-next=invalid-name
__metaclass__ = type

import asyncio
import logging
from json import JSONDecodeError
from typing import Any

from aiohttp import web
from dpath import util

DOCUMENTATION = r"""
---
short_description: Receive events from PAN-OS firewall or Panorama appliance.
description:
  - An ansible-rulebook event source plugin for receiving events via a webhook from
    PAN-OS firewall or Panorama appliance.
options:
  host:
    description:
      - The webserver hostname to listen to. Set to 0.0.0.0 to listen on all
        interfaces.
    type: str
    default: "localhost"
  port:
    description:
      - The TCP port to listen to.
    type: int
    default: 5000
  type:
    description:
      - The log type to filter events.
    type: str
    default: "decryption"
"""

EXAMPLES = r"""
- paloaltonetworks.panos.logs:
    host: 0.0.0.0
    port: 5000
    type: decryption
"""


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

routes = web.RouteTableDef()


@routes.get("/")
async def status() -> web.Response:
    """Return a simple status response.

    Returns
    -------
    A web.Response object with status 200 and the text "up" returned by the function.

    """
    return web.Response(status=200, text="up")


@routes.post("/{endpoint}")
async def webhook(request: web.Request) -> web.Response:
    """Handle webhook requests.

    Process the incoming JSON payload and forward it to the event queue
    if it matches the configured log type.

    Parameters
    ----------
    request
        The incoming webhook request.

    Returns
    -------
    A web.Response object with status 200 and the status.

    """
    try:
        payload = await request.json()
    except JSONDecodeError:
        logger.exception("Failed to parse JSON payload")
        return web.Response(status=400, text="Invalid JSON payload")

    if request.app["type"] == "decryption":
        log_type = payload.get("type", "log_type")
        if log_type != "decryption":
            log_type = "log_type"

        data = process_payload(request, payload, log_type)
        await request.app["queue"].put(data)

    return web.Response(
        status=202,
        text=str({"status": "received", "payload": "happy"}),
    )


def process_payload(
    request: web.Request,
    payload: dict[str, Any],
    log_type: str,
) -> dict[str, Any]:
    """Process the payload and extract the necessary information.

    Parameters
    ----------
    request
        The incoming webhook request.
    payload
        The JSON payload from the request.
    log_type : str
        The log type to filter events.

    Returns
    -------
    A dictionary containing the processed payload and metadata.

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


async def main(
    queue: asyncio.Queue,
    args: dict[str, Any],
    custom_logger: None = None,
) -> None:
    """Run the plugin as a standalone application.

    Parameters
    ----------
    queue
        The event queue to forward incoming events to.
    args
        A dictionary containing configuration arguments.
    custom_logger
        An optional custom logger.

    """
    if custom_logger is None:
        custom_logger = logging.getLogger(__name__)

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
        custom_logger.info("Plugin Task Cancelled")
    finally:
        await runner.cleanup()


if __name__ == "__main__":

    class MockQueue:
        """A mock queue for handling events asynchronously."""

        async def put(self: "MockQueue", event: str) -> None:
            """Put an event into the queue.

            Parameters
            ----------
            event: str
                The event to be added to the queue.

            """
            the_logger.info(event)

        async def get(self: "MockQueue") -> None:
            """Get an event from the queue."""
            the_logger.info("Getting event from the queue.")

    the_logger = logging.getLogger()
    asyncio.run(main(MockQueue(), {}, the_logger))
