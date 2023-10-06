#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2020 Palo Alto Networks, Inc
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
module: panos_application_object
short_description: Manage application objects on PAN-OS devices.
description:
    - Manage application objects on PAN-OS devices.
author: "Michael Richardson (@mrichardson03)"
version_added: '2.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.vsys
    - paloaltonetworks.panos.fragments.device_group
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
options:
    name:
        description:
            - Name of the tag.
        type: str
    category:
        description:
            - Application category
        type: str
    subcategory:
        description:
            - Application subcategory
        type: str
    technology:
        description:
            - Application technology
        type: str
    risk:
        description:
            - Risk (1-5) of the application
        type: int
        choices: [1, 2, 3, 4, 5]
    default_type:
        description:
            - Default identification type of the application.
        type: str
        choices:
            - port
            - ident-by-ip-protocol
            - ident-by-icmp-type
            - ident-by-icmp6-type
    default_port:
        description:
            - Default ports.
        type: list
        elements: str
    default_ip_protocol:
        description:
            - Default IP protocol.
        type: str
    default_icmp_type:
        description:
            - Default ICMP type.
        type: int
    default_icmp_code:
        description:
            - Default ICMP code.
        type: int
    parent_app:
        description:
            - Parent Application for which this app falls under
        type: str
    timeout:
        description:
            - Default timeout
        type: int
    tcp_timeout:
        description:
            - TCP timeout
        type: int
    udp_timeout:
        description:
            - UDP timeout
        type: int
    tcp_half_closed_timeout:
        description:
            - TCP half closed timeout
        type: int
    tcp_time_wait_timeout:
        description:
            - TCP wait time timeout
        type: int
    evasive_behavior:
        description:
            - Application is actively evasive
        type: bool
    consume_big_bandwidth:
        description:
            - Application uses large bandwidth
        type: bool
    used_by_malware:
        description:
            - Application is used by malware
        type: bool
    able_to_transfer_file:
        description:
            - Application can do file transfers
        type: bool
    has_known_vulnerability:
        description:
            - Application has known vulnerabilities
        type: bool
    tunnel_other_application:
        description:
            - Application can tunnel other applications
        type: bool
    tunnel_applications:
        description:
            - List of tunneled applications
        type: list
        elements: str
    prone_to_misuse:
        description:
            - Application is prone to misuse
        type: bool
    pervasive_use:
        description:
            - Application is used pervasively
        type: bool
    file_type_ident:
        description:
            - Scan for files
        type: bool
    virus_ident:
        description:
            - Scan for viruses
        type: bool
    data_ident:
        description:
            - Scan for data types
        type: bool
    description:
        description:
            - Description of this object
        type: str
    tag:
        description:
            - Administrative tags
        type: list
        elements: str
"""

EXAMPLES = """
- name: Create custom application
  paloaltonetworks.panos.panos_application_object:
    provider: '{{ provider }}'
    name: 'custom-app'
    category: 'business-systems'
    subcategory: 'auth-service'
    technology: 'client-server'
    risk: 1

- name: Remove custom application
  paloaltonetworks.panos.panos_application_object:
    provider: '{{ provider }}'
    name: 'custom-app'
    state: 'absent'
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
        vsys=True,
        device_group=True,
        with_classic_provider_spec=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        sdk_cls=("objects", "ApplicationObject"),
        sdk_params=dict(
            name=dict(required=True),
            category=dict(),
            subcategory=dict(),
            technology=dict(),
            risk=dict(type="int", choices=[1, 2, 3, 4, 5]),
            default_type=dict(
                choices=[
                    "port",
                    "ident-by-ip-protocol",
                    "ident-by-icmp-type",
                    "ident-by-icmp6-type",
                ],
            ),
            default_port=dict(type="list", elements="str"),
            default_ip_protocol=dict(),
            default_icmp_type=dict(type="int"),
            default_icmp_code=dict(type="int"),
            parent_app=dict(),
            timeout=dict(type="int"),
            tcp_timeout=dict(type="int"),
            udp_timeout=dict(type="int"),
            tcp_half_closed_timeout=dict(type="int"),
            tcp_time_wait_timeout=dict(type="int"),
            evasive_behavior=dict(type="bool"),
            consume_big_bandwidth=dict(type="bool"),
            used_by_malware=dict(type="bool"),
            able_to_transfer_file=dict(type="bool"),
            has_known_vulnerability=dict(type="bool"),
            tunnel_other_application=dict(type="bool"),
            tunnel_applications=dict(type="list", elements="str"),
            prone_to_misuse=dict(type="bool"),
            pervasive_use=dict(type="bool"),
            file_type_ident=dict(type="bool"),
            virus_ident=dict(type="bool"),
            data_ident=dict(type="bool"),
            description=dict(),
            tag=dict(type="list", elements="str"),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        required_one_of=helper.required_one_of,
        supports_check_mode=True,
    )

    helper.process(module)


if __name__ == "__main__":
    main()
