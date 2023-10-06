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
module: panos_dhcp_relay_ipv6_address
short_description: Manage DHCP IPv6 relay addresses.
description:
    - Manage DHCP relay IPv6 addresses on PAN-OS firewall.
author:
    - Garfield Lee Freeman (@shinmog)
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
            - This is probably the same as I(dhcp_relay_interface) and
              I(interface).
        type: str
        required: true
    dhcp_relay_interface:
        description:
            - The interface name for the DHCP relay.
            - This is probably the same as I(dhcp_interface) and
              I(interface).
        type: str
        required: true
    ipv6_address:
        description:
            - The DHCP server IPv6 address.
        type: str
    interface:
        description:
            - Outgoing interface when using an IPv6 multicast address
              for the DHCPv6 server.
            - This is probably the same as I(dhcp_interface) and
              I(dhcp_relay_interface).
        type: str
"""

EXAMPLES = """
# Create IPv6 DHCP Relay address
- paloaltonetworks.panos.panos_dhcp_relay:
    provider: '{{ provider }}'
    dhcp_interface: 'ethernet1/1'
    dhcp_relay_interface: 'ethernet1/1'
    ipv6_address: '2001:0db8:85a3:0000:0000:8a2e:0370:7334'
    interface: 'ethernet1/1'

# Delete DHCP Relay ipv6 address
- paloaltonetworks.panos.panos_dhcp_relay:
    provider: '{{ provider }}'
    dhcp_interface: 'ethernet1/1'
    dhcp_relay_interface: 'ethernet1/1'
    ipv6_address: '2001:0db8:85a3:0000:0000:8a2e:0370:7334'
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
        parents=(
            ("network", "Dhcp", "dhcp_interface"),
            ("network", "DhcpRelay", "dhcp_relay_interface"),
        ),
        sdk_cls=("network", "DhcpRelayIpv6Address"),
        sdk_params=dict(
            ipv6_address=dict(required=True, sdk_param="name"),
            interface=dict(),
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
