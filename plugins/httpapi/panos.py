# Copyright 2020 Palo Alto Networks, Inc
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
author:
    - Michael Richardson (@mrichardson03)
name : panos
short_description: HttpApi plugin for PAN-OS devices
description:
    - HttpApi plugin for PAN-OS devices
version_added: '1.0.0'
options:
    api_key:
        type: str
        description:
            - Use API key for authentication instead of username and password
        vars:
            - name: ansible_api_key
"""

import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

from ansible.module_utils.basic import to_text
from ansible.module_utils.six.moves import urllib
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible.plugins.httpapi import HttpApiBase
from ansible.utils.display import Display
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    cmd_xml,
)

display = Display()

# List of valid API error codes and names.
#
# Reference:
# https://docs.paloaltonetworks.com/pan-os/10-0/pan-os-panorama-api/get-started-with-the-pan-os-xml-api/pan-os-xml-api-error-codes.html
_PANOS_API_ERROR_CODES = {
    "400": "Bad Request",
    "403": "Forbidden",
    "1": "Unknown Command",
    "2": "Internal Error",
    "3": "Internal Error",
    "4": "Internal Error",
    "5": "Internal Error",
    "6": "Bad Xpath",
    "7": "Object not present",
    "8": "Object not unique",
    "10": "Reference count not zero",
    "11": "Internal Error",
    "12": "Invalid Object",
    "14": "Operation Not Possible",
    "15": "Operation Denied",
    "16": "Unauthorized",
    "17": "Invalid Command",
    "18": "Malformed Command",
    "19": "Success",
    "20": "Success",
    "21": "Internal Error",
    "22": "Session Timed Out",
}


class PanOSAPIError(ConnectionError):
    """Exception representing a PAN-OS API error."""

    def __init__(self, code, message):
        if code not in _PANOS_API_ERROR_CODES:
            self._code = "-1"
            msg = "Unspecified API Error"
        else:
            self._code = code
            msg = "{0} ({1})".format(_PANOS_API_ERROR_CODES[code], code)

        if message:
            msg += ": {0}".format(message)

        super().__init__(msg)

    @property
    def code(self):
        """
        Returns the PAN-OS API status code for this error.

        This may correspond to the HTTP status code used to deliver the
        response, but not always.
        """
        return self._code


class TimedOutException(Exception):
    pass


class HttpApi(HttpApiBase):
    def __init__(self, connection):
        super().__init__(connection)

        self._api_key = None
        self._device_info = None

    def api_key(self):
        """
        Return the API key used by this connection.

        If the plugin is set to authenticate using a username and password,
        one will be generated and reused by this method.
        """
        if self._api_key:  # pragma: no cover
            return self._api_key

        if self.get_option("api_key") is not None:
            self._api_key = self.get_option("api_key")
        else:
            username = self.connection.get_option("remote_user")
            password = self.connection.get_option("password")

            self._api_key = self.keygen(username, password)

        return self._api_key

    def keygen(self, username, password):
        """
        Generates an API key for the requested user.  If successful, this key
        can be used later as a URL encoded parameter 'key', or in the
        'X-PAN-KEY' header (PAN-OS 9.0+).

        :param username: Username used to generate API key.
        :param password: Password used to generate API key.
        :returns: String containing API key.

        Reference:
        https://docs.paloaltonetworks.com/pan-os/10-0/pan-os-panorama-api/get-started-with-the-pan-os-xml-api/get-your-api-key.html
        """
        params = {"type": "keygen", "user": username, "password": password}

        data = urllib.parse.urlencode(params)
        code, response = self.send_request(data)

        # Will throw exception if credentials are bad.
        response = self._validate_response(code, response)

        root = ET.fromstring(response)
        key = root.find("./result/key")

        if key is not None:
            return key.text
        else:
            return None

    def show(self, xpath=None):
        """
        Retrieves the running configuration from the device.

        :param xpath: Retrieve a specific portion of the configuration.

        Reference:
        https://docs.paloaltonetworks.com/pan-os/10-0/pan-os-panorama-api/pan-os-xml-api-request-types/configuration-api/get-active-configuration/use-xpath-to-get-active-configuration.html
        """
        pass

    def get(self, xpath=None):
        """
        Performs the 'get' API request.  This is used to retrieve the candidate
        configuration from the device.

        :param xpath: Retrieve a specific portion of the configuration.
        :returns: String containing XML response.

        Reference:
        https://docs.paloaltonetworks.com/pan-os/10-0/pan-os-panorama-api/pan-os-xml-api-request-types/configuration-api/get-candidate-configuration.html
        """
        params = {"type": "config", "key": self.api_key(), "action": "get"}

        if xpath:
            params.update({"xpath": xpath})

        data = urllib.parse.urlencode(params)
        code, response = self.send_request(data)

        return self._validate_response(code, response)

    def set(self, xpath, element):
        """
        Creates a new object at a specified location in the configuration.

        :param xpath: Location of the new object.
        :param element: Object to add.

        Reference:
        https://docs.paloaltonetworks.com/pan-os/10-0/pan-os-panorama-api/pan-os-xml-api-request-types/configuration-api/set-configuration.html
        """

        params = {
            "type": "config",
            "key": self.api_key(),
            "action": "set",
            "xpath": xpath,
            "element": element,
        }

        data = urllib.parse.urlencode(params)
        code, response = self.send_request(data)

        return self._validate_response(code, response)

    def edit(self, xpath, element):
        """
        Replaces an existing object with a new value.

        Commonly used after retrieving the existing value using 'show'.

        :param xpath: Location of the object.
        :param element: New value of object.

        Reference:
        https://docs.paloaltonetworks.com/pan-os/10-0/pan-os-panorama-api/pan-os-xml-api-request-types/configuration-api/edit-configuration.html
        """
        params = {
            "type": "config",
            "key": self.api_key(),
            "action": "edit",
            "xpath": xpath,
            "element": element,
        }

        data = urllib.parse.urlencode(params)
        code, response = self.send_request(data)

        return self._validate_response(code, response)

    def delete(self, xpath):
        """
        Deletes an object from the configuration.

        :param xpath: Location of the object.

        Reference:
        https://docs.paloaltonetworks.com/pan-os/10-0/pan-os-panorama-api/pan-os-xml-api-request-types/configuration-api/delete-configuration.html
        """
        params = {
            "type": "config",
            "key": self.api_key(),
            "action": "delete",
            "xpath": xpath,
        }

        data = urllib.parse.urlencode(params)
        code, response = self.send_request(data)

        return self._validate_response(code, response)

    def rename(self, xpath, newname):
        """
        Renames an object in the configuration.

        :param xpath: Location of the object.
        :param newname: New name for object.

        Reference:
        https://docs.paloaltonetworks.com/pan-os/10-0/pan-os-panorama-api/pan-os-xml-api-request-types/configuration-api/rename-configuration.html
        """
        pass

    def move(self, xpath, where, dst=None):
        """
        Moves the location of an existing object.

        :param xpath: Location of the object.
        :param where: Can be 'before', 'after', 'top', or 'bottom'.
        :param dst:   Destination XPath.  Used when 'where' is 'before' or 'after'.

        Reference:
        https://docs.paloaltonetworks.com/pan-os/10-0/pan-os-panorama-api/pan-os-xml-api-request-types/configuration-api/move-configuration.html
        """
        pass

    def override(self, xpath, element):
        """
        Overrides a setting that has been pushed to a firewall from a template.

        :param xpath: Location of the object.
        :param element: New value of the object.

        Reference:
        https://docs.paloaltonetworks.com/pan-os/10-0/pan-os-panorama-api/pan-os-xml-api-request-types/configuration-api/override-configuration.html
        """
        pass

    def commit(
        self,
        force=False,
        exclude_device_and_network=False,
        exclude_policy_and_objects=False,
        exclude_shared_objects=False,
        admins=None,
        description=None,
    ):
        """
        Commits the candidate configuration to the device.

        :param force: Perform a force commit.
        :param exclude_device_and_network: Perform a partial commit, excluding
        device and network configuration from Panorama.
        :param exclude_policy_and_objects: Perform a partial commit, excluding
        policy and object configuration from Panorama.
        :param exclude_shared_objects: Perform a partial commit, excluding
        shared object configuration from Panorama.
        :param admins: Perform a partial commit, only commiting changes from
        these administrators.

        Reference:
        https://docs.paloaltonetworks.com/pan-os/10-0/pan-os-panorama-api/pan-os-xml-api-request-types/commit-configuration-api/commit.html
        """
        cmd = ET.Element("commit")

        if force:
            sub_force = ET.SubElement(cmd, "force")

        if description:
            sub_desc = ET.SubElement(cmd, "description")
            sub_desc.text = description

        if (
            exclude_device_and_network
            or exclude_policy_and_objects
            or exclude_shared_objects
            or admins
        ):
            sub_partial = ET.SubElement(cmd, "partial")

            if exclude_device_and_network:
                sub_exclude_device_network = ET.SubElement(
                    sub_partial, "device-and-network"
                )
                sub_exclude_device_network.text = "excluded"

            if exclude_policy_and_objects:
                sub_exclude_policy_and_objects = ET.SubElement(
                    sub_partial, "policy-and-objects"
                )
                sub_exclude_policy_and_objects.text = "excluded"

            if exclude_shared_objects:
                sub_exclude_shared_objects = ET.SubElement(sub_partial, "shared-object")
                sub_exclude_shared_objects.text = "excluded"

            if isinstance(admins, list):
                sub_admins = ET.SubElement(sub_partial, "admin")

                for admin in admins:
                    m = ET.SubElement(sub_admins, "member")
                    m.text = admin

        params = {"type": "commit", "key": self.api_key(), "cmd": ET.tostring(cmd)}

        data = urllib.parse.urlencode(params)
        code, response = self.send_request(data)

        return self._validate_response(code, response)

    def commit_all(self, validate=False, device_groups=None, vsys=None, serials=None):
        """
        Push policy and template configuration from a Panorama device.

        :param device_groups: Commit to specific device groups.
        :param vsys: Commit to specific virtual system.
        :param serials: Commit to specific firewall serial numbers.

        Reference:
        https://docs.paloaltonetworks.com/pan-os/10-0/pan-os-panorama-api/pan-os-xml-api-request-types/commit-configuration-api/commit-all.html
        """
        pass

    def op(
        self,
        cmd,
        is_xml=True,
        validate=True,
        poll=False,
        poll_interval=5,
        poll_timeout=600,
    ):
        """
        Runs an operational command.

        :param cmd: Command to run.
        :param is_xml: Command is in XML format.
        :param validate: Whether the response should be validated.
        :param poll: For use with a long running task.  When set to true, poll
        until that task completes.
        :param poll_interval: How often to poll for job completion (in seconds).
        :param poll_timeout: Maximum amount of time to poll (in seconds).
        :returns: Response data.

        Reference:
        https://docs.paloaltonetworks.com/pan-os/10-0/pan-os-panorama-api/pan-os-xml-api-request-types/run-operational-mode-commands-api.html
        """

        params = {
            "type": "op",
            "key": self.api_key(),
            "cmd": cmd if is_xml else cmd_xml(cmd),
        }

        data = urllib.parse.urlencode(params)
        code, response = self.send_request(data)

        if validate:
            response = self._validate_response(code, response)

        if poll:
            op_result = ET.fromstring(response)

            job_element = op_result.find(".//job")
            job_id = job_element.text

            return self.poll_for_job(
                job_id, interval=poll_interval, timeout=poll_timeout
            )
        else:
            return response

    # reports
    # export
    # import
    # log
    # user-id

    def version(self, refresh=False):
        """
        Runs the version API command.

        Retrieves device software version, vsys mode, model, and serial number.

        :returns: Dict containing device info.
        """
        if self._device_info and refresh is False:  # pragma: no cover
            return self._device_info

        params = {"type": "version", "key": self.api_key()}

        data = urllib.parse.urlencode(params)
        code, response = self.send_request(data)

        root = ET.fromstring(response)
        result = root.find("./result")

        self._device_info = {}
        self._device_info.update(
            {
                "sw-version": result.findtext("sw-version"),
                "multi-vsys": result.findtext("multi-vsys"),
                "model": result.findtext("model"),
                "serial": result.findtext("serial"),
            }
        )

        display.vvvv("version = {0}".format(self._device_info))

        return self._device_info

    def poll_for_job(self, job_id, interval=5, timeout=600):
        """
        Polls for job completion.

        :param job_id: ID of job to poll for.
        :param interval: Poll interval, in seconds.
        """
        cmd = "<show><jobs><id>{0}</id></jobs></show>".format(job_id)

        display.vvvv(
            "poll_for_job(): job_id = {0}, interval = {1}, timeout = {2}".format(
                job_id, interval, timeout
            )
        )

        max_end_time = datetime.utcnow() + timedelta(seconds=timeout)

        while datetime.utcnow() < max_end_time:
            result = self.op(cmd, is_xml=True)

            root = ET.fromstring(result)
            status = root.find("./result/job/status")

            if status is None:
                raise ConnectionError("Could not find status element in job.")

            display.vvvv(
                "poll_for_job(): job_id {0} status = {1}".format(job_id, status.text)
            )

            if status.text == "FIN":
                return result
            else:
                time.sleep(interval)

        raise TimedOutException("Timed out waiting for job id {0}".format(job_id))

    def is_panorama(self):
        """
        Returns if the connected device is a Panorama instance.

        :returns: Boolean if this device is a Panorama or not.
        """
        if self._device_info is None:
            self.version()

        return True if self._device_info["model"] == "Panorama" else False

    def update_auth(self, response, response_text):
        """
        Returns the per-request auth token.  For PAN-OS 9.0+, this is the
        header 'X-PAN-KEY' set to the API key.

        :returns: Dictionary with the 'X-PAN-KEY' set if the connection is
        established, None if not.
        """
        if self._api_key:
            return {"X-PAN-KEY": self.api_key()}
        else:
            return None

    def send_request(
        self,
        data=None,
        path="/api/",
        params=None,
        method="POST",
        headers=None,
        **message_kwargs,
    ):
        """
        Sends a request to the PAN-OS API.

        :param data: Data to send to the API endpoint.
        :param path: URL path used for the API endpoint.
        :param params: Parameters to send with request (will be URL encoded).
        :param method: HTTP method to for request.
        :param headers: HTTP headers to include in request.
        :param request_type: API request type ('xml' or 'json')
        :returns: Tuple (HTTP response code, data object).

        Error Codes:
        https://docs.paloaltonetworks.com/pan-os/10-0/pan-os-panorama-api/get-started-with-the-pan-os-xml-api/pan-os-xml-api-error-codes.html
        """

        if params is not None:
            params = urllib.parse.urlencode(params) if params else ""
            path += "?{0}".format(params)

        if data is None:
            data = ""

        if headers is None:
            headers = {}

        if len(data.encode("utf-8")) > int(5e6):
            raise ConnectionError("Data too large for XML API request")

        headers.update(
            {
                "Content-Type": "application/x-www-form-urlencoded",
                "Content-Length": len(data),
            }
        )

        display.vvvv("send_request(): headers = {0}".format(headers))
        display.vvvv("send_request(): method = {0}".format(method))
        display.vvvv("send_request(): path = {0}".format(path))
        display.vvvv("send_request(): data = {0}".format(data))

        try:
            response, response_data = self.connection.send(
                path, data, method=method, headers=headers
            )

            display.vvvv(
                "send_request(): response code = {0}".format(response.getcode())
            )

            return response.getcode(), response_data.getvalue()
        except HTTPError as e:
            return e.code, e.read()

    @staticmethod
    def _validate_response(http_code, http_response):

        # Valid XML-API responses can be contained in the following HTTP status
        # codes:
        #   400 - Bad Request (malformed request)
        #   403 - Forbidden (invalid credentials)
        #   200 - OK (HTTP request was OK, but still can be an XML-API error)
        if http_code not in [200, 400, 403]:
            raise ConnectionError("Invalid response from API")

        data = to_text(http_response)
        root = ET.fromstring(data)

        display.vvvv("_validate_response(): response = {0}".format(data))

        status = root.attrib.get("status")
        api_code = root.attrib.get("code")

        if status == "error":
            msg = None

            # Error messages can be in multiple locations in the response.
            if root.findtext("./result/msg"):
                msg = root.findtext("./result/msg")

            elif len(root.findall("./msg/line")) > 0:
                lines = root.findall("./msg/line")
                msg = ", ".join([line.text for line in lines])

            raise PanOSAPIError(api_code, msg)

        # For whatever reason, Ansible wants a JSON serializable response ONLY,
        # so return unparsed data.
        return data
