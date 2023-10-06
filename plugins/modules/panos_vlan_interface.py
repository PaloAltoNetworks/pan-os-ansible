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
module: panos_vlan_interface
short_description: Manage VLAN interfaces
description:
    - Manage VLAN interfaces.
author: "Garfield Lee Freeman (@shinmog)"
version_added: '1.0.0'
requirements:
    - pan-python
    - pandevice
notes:
    - Checkmode is supported.
    - If the PAN-OS device is a firewall and I(vsys) is not specified, then
      the vsys will default to I(vsys=vsys1).
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
    - paloaltonetworks.panos.fragments.vsys_import
    - paloaltonetworks.panos.fragments.template_only
options:
    name:
        description:
            - Name of the interface to configure.
            - This should be in the format "vlan.<some_number>".
        type: str
    ip:
        description:
            - List of static IP addresses.
        type: list
        elements: str
    ipv6_enabled:
        description:
            - Enable IPv6.
        type: bool
    management_profile:
        description:
            - Interface management profile name.
        type: str
    mtu:
        description:
            - MTU for layer3 interface.
        type: int
    adjust_tcp_mss:
        description:
            - Adjust TCP MSS for layer3 interface.
        type: bool
    netflow_profile:
        description:
            - Netflow profile for layer3 interface.
        type: str
    comment:
        description:
            - Interface comment.
        type: str
    ipv4_mss_adjust:
        description:
            - (7.1+) TCP MSS adjustment for IPv4.
        type: int
    ipv6_mss_adjust:
        description:
            - (7.1+) TCP MSS adjustment for IPv6.
        type: int
    enable_dhcp:
        description:
            - Enable DHCP on this interface.
        type: bool
    create_dhcp_default_route:
        description:
            - Whether or not to add default route with router learned via DHCP.
        type: bool
    dhcp_default_route_metric:
        description:
            - Metric for the DHCP default route.
        type: int
    zone_name:
        description:
            - Name of the zone for the interface.
            - If the zone does not exist it is created.
            - If the zone already exists it should be I(mode=layer3).
        type: str
    vlan_name:
        description:
            - The VLAN to put this interface in.
            - If the VLAN does not exist it is created.
        type: str
    vr_name:
        description:
            - Name of the virtual router
        type: str
"""

EXAMPLES = """
# Create vlan.2 as DHCP
- name: enable DHCP client on ethernet1/1 in zone public
  paloaltonetworks.panos.panos_vlan_interface:
    provider: '{{ provider }}'
    name: "vlan.2"
    zone_name: "public"
    enable_dhcp: true
    create_default_route: true

# Set vlan.7 with a static IP
- name: Configure vlan.7
  paloaltonetworks.panos.panos_vlan_interface:
    provider: '{{ provider }}'
    name: "vlan.7"
    ip: ["10.1.1.1/24"]
    management_profile: "allow ping"
    vlan_name: "dmz"
    zone_name: "L3-untrust"
    vr_name: "default"
"""

RETURN = """
# Default return values
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    ConnectionHelper,
    get_connection,
)


class Helper(ConnectionHelper):
    def initial_handling(self, module):
        if module.params["state"] not in ("present", "replaced"):
            return

        if module.params["vsys"] is None:
            module.params["vsys"] = "vsys1"

    def spec_handling(self, spec, module):
        if module.params["state"] not in ("present", "replaced"):
            return

        for p in ("enable_dhcp", "create_dhcp_default_route"):
            if not spec[p]:
                spec[p] = None


def main():
    helper = get_connection(
        helper_cls=Helper,
        vsys_importable=True,
        template=True,
        with_classic_provider_spec=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        min_pandevice_version=(0, 9, 0),
        with_set_vsys_reference=True,
        with_set_zone_reference=True,
        with_set_vlan_interface_reference=True,
        with_set_virtual_router_reference=True,
        virtual_router_reference_default=None,
        default_zone_mode="layer3",
        sdk_cls=("network", "VlanInterface"),
        sdk_params=dict(
            name=dict(required=True),
            ip=dict(type="list", elements="str"),
            ipv6_enabled=dict(type="bool"),
            management_profile=dict(),
            mtu=dict(type="int"),
            adjust_tcp_mss=dict(type="bool"),
            netflow_profile=dict(),
            comment=dict(),
            ipv4_mss_adjust=dict(type="int"),
            ipv6_mss_adjust=dict(type="int"),
            enable_dhcp=dict(type="bool"),
            create_dhcp_default_route=dict(type="bool"),
            dhcp_default_route_metric=dict(type="int"),
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
