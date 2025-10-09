#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2022 Palo Alto Networks, Inc
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
module: panos_dhcp_relay
short_description: Manage dhcp relay.
description:
    - Manage dhcp relay on PAN-OS firewall.
    - Due to the implementation details of PAN-OS itself, you can use this
      module to create a DHCP config without ever having to use M(paloaltonetworks.panos.panos_dhcp)
      first.
    - However, if you intend to delete an interface that was ever reference by
      this module, you will need to use M(paloaltonetworks.panos.panos_dhcp) to delete the parent reference
      or PAN-OS's internal validation checks will prevent the deletion, seeing that
      a DHCP config is referring to the interface.
author:
    - Sean O'Brien (@undodelete)
version_added: '2.10.0'
requirements:
    - pan-python >= 0.17
    - pan-os-python >= 1.7.3
notes:
    - Check mode is supported.
    - Panorama is not supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
options:
    dhcp_interface:
        description:
            - The interface name.
            - This is probably the same as I(interface).
        type: str
        required: true
    interface:
        description:
            - The interface name for the DHCP relay.
            - This is probably the same as the I(dhcp_interface).
        type: str
    ipv4_enabled:
        description:
            - Enable IPv4 on DHCP Relay
        type: bool
    ipv4_servers:
        description:
            - Relay server IP addresses.
        type: list
        elements: str
    ipv6_enabled:
        description:
            - Enable DHCPv6 relay.
        type: bool
"""

EXAMPLES = """
# Create IPv4 DHCP Relay
- paloaltonetworks.panos.panos_dhcp_relay:
    provider: '{{ provider }}'
    dhcp_interface: 'ethernet1/1'
    interface: 'ethernet1/1'
    ipv4_enabled: true
    ipv4_servers:
      - '1.1.1.1'
      - '2.2.2.2'

# Delete DHCP Relay
- paloaltonetworks.panos.panos_dhcp_relay:
    provider: '{{ provider }}'
    dhcp_interface: 'ethernet1/1'
    interface: 'ethernet1/1'
    state: absent
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
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        with_classic_provider_spec=True,
        panorama_error="This is a firewall only module",
        min_pandevice_version=(1, 7, 3),
        parents=(("network", "Dhcp", "dhcp_interface"),),
        sdk_cls=("network", "DhcpRelay"),
        sdk_params=dict(
            interface=dict(required=True, sdk_param="name"),
            ipv4_enabled=dict(type="bool", sdk_param="enabled"),
            ipv4_servers=dict(type="list", elements="str", sdk_param="servers"),
            ipv6_enabled=dict(type="bool"),
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
