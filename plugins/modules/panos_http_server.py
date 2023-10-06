#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2019 Palo Alto Networks, Inc
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

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: panos_http_server
short_description: Manage HTTP servers in a HTTP server profile.
description:
    - Manages HTTP servers in a HTTP server profile.
author: "Garfield Lee Freeman (@shinmog)"
version_added: '1.0.0'
requirements:
    - pan-python
    - pandevice >= 0.11.1
    - PAN-OS >= 8.0
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.vsys_shared
    - paloaltonetworks.panos.fragments.device_group
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
options:
    http_profile:
        description:
            - Name of the http server profile.
        type: str
        required: True
    name:
        description:
            - Server name.
        type: str
    address:
        description:
            - IP address or FQDN of the HTTP server
        type: str
    protocol:
        description:
            - The protocol.
        type: str
        choices:
            - HTTP
            - HTTPS
        default: 'HTTPS'
    http_port:
        description:
            - Port number.
        type: int
        default: 443
    tls_version:
        description:
            - PAN-OS 9.0+
            - TLS handshake protocol version
        type: str
        choices:
            - "1.0"
            - "1.1"
            - "1.2"
    certificate_profile:
        description:
            - PAN-OS 9.0+
            - Certificate profile for validating server cert.
        type: str
    http_method:
        description:
            - HTTP method to use.
        type: str
        default: 'POST'
    http_username:
        description:
            - Username for basic HTTP auth.
        type: str
    http_password:
        description:
            - Password for basic HTTP auth.
        type: str
"""

EXAMPLES = """
- name: Create http server
  paloaltonetworks.panos.panos_http_server:
    provider: '{{ provider }}'
    http_profile: 'my-profile'
    name: 'my-http-server'
    address: '192.168.1.5'
    http_method: 'GET'
    http_username: 'jack'
    http_password: 'burton'
"""

RETURN = """
# Default return values
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    get_connection,
)


def main():
    helper = get_connection(
        vsys_shared=True,
        device_group=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        with_classic_provider_spec=True,
        min_pandevice_version=(0, 11, 1),
        min_panos_version=(8, 0, 0),
        parents=(("device", "HttpServerProfile", "http_profile"),),
        sdk_cls=("device", "HttpServer"),
        sdk_params=dict(
            name=dict(required=True),
            address=dict(required=True),
            protocol=dict(default="HTTPS", choices=["HTTP", "HTTPS"]),
            http_port=dict(type="int", default=443, sdk_param="port"),
            tls_version=dict(choices=["1.0", "1.1", "1.2"]),
            certificate_profile=dict(),
            http_method=dict(default="POST"),
            http_username=dict(sdk_param="username"),
            http_password=dict(no_log=True, sdk_param="password"),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    helper.process(module)


if __name__ == "__main__":
    main()
