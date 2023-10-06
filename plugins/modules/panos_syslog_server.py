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
module: panos_syslog_server
short_description: Manage syslog server profile syslog servers.
description:
    - Manages syslog servers in an syslog server profile.
author: "Garfield Lee Freeman (@shinmog)"
version_added: '1.0.0'
requirements:
    - pan-python
    - pandevice >= 0.11.1
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
    syslog_profile:
        description:
            - Name of the syslog server profile.
        type: str
        required: True
    name:
        description:
            - Server name.
        type: str
    server:
        description:
            - IP address or FQDN of the syslog server
        type: str
    transport:
        description:
            - Syslog transport.
        type: str
        choices:
            - UDP
            - TCP
            - SSL
        default: "UDP"
    syslog_port:
        description:
            - Syslog port number
        type: int
    format:
        description:
            Format of the syslog message.
        type: str
        choices:
            - BSD
            - IETF
        default: "BSD"
    facility:
        description:
            - Syslog facility.
        type: str
        choices:
            - LOG_USER
            - LOG_LOCAL0
            - LOG_LOCAL1
            - LOG_LOCAL2
            - LOG_LOCAL3
            - LOG_LOCAL4
            - LOG_LOCAL5
            - LOG_LOCAL6
            - LOG_LOCAL7
        default: "LOG_USER"
"""

EXAMPLES = """
- name: Create syslog server
  paloaltonetworks.panos.panos_syslog_server:
    provider: '{{ provider }}'
    syslog_profile: 'my-profile'
    name: 'my-syslog-server'
    server: '10.1.1.1'
    syslog_port: 514
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
        min_panos_version=(7, 1, 0),
        parents=(("device", "SyslogServerProfile", "syslog_profile"),),
        sdk_cls=("device", "SyslogServer"),
        sdk_params=dict(
            name=dict(required=True),
            server=dict(),
            transport=dict(default="UDP", choices=["UDP", "TCP", "SSL"]),
            syslog_port=dict(type="int", sdk_param="port"),
            format=dict(default="BSD", choices=["BSD", "IETF"]),
            facility=dict(
                default="LOG_USER",
                choices=[
                    "LOG_USER",
                    "LOG_LOCAL0",
                    "LOG_LOCAL1",
                    "LOG_LOCAL2",
                    "LOG_LOCAL3",
                    "LOG_LOCAL4",
                    "LOG_LOCAL5",
                    "LOG_LOCAL6",
                    "LOG_LOCAL7",
                ],
            ),
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
