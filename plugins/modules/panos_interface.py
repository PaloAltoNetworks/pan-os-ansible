#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2016 Palo Alto Networks, Inc
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
module: panos_interface
short_description: Manage data-port network interfaces
description:
    - Manage data-port (DP) network interface. By default DP interfaces are static.
author:
    - Luigi Mori (@jtschichold)
    - Ivan Bojer (@ivanbojer)
    - Garfield Lee Freeman (@shinmog)
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
    - pandevice >= 0.8.0
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
    - paloaltonetworks.panos.fragments.deprecated_commit
options:
    if_name:
        description:
            - Name of the interface to configure.
        type: str
    mode:
        description:
            - The interface mode.
        type: str
        default: "layer3"
        choices:
            - layer3
            - layer2
            - virtual-wire
            - tap
            - ha
            - decrypt-mirror
            - aggregate-group
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
    lldp_enabled:
        description:
            - Enable LLDP for layer2 interface.
        type: str
    lldp_profile:
        description:
            - LLDP profile name for layer2 interface.
        type: str
    netflow_profile_l2:
        description:
            - Netflow profile name for layer2 interface.
        type: str
    link_speed:
        description:
            - Link speed.
        type: str
        choices:
            - auto
            - "10"
            - "100"
            - "1000"
    link_duplex:
        description:
            - Link duplex.
        type: str
        choices:
            - auto
            - full
            - half
    link_state:
        description:
            - Link state.
        type: str
        choices:
            - auto
            - up
            - down
    aggregate_group:
        description:
            - Aggregate interface name.
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
        default: True
    create_default_route:
        description:
            - Whether or not to add default route with router learned via DHCP.
        type: bool
        default: False
    dhcp_default_route_metric:
        description:
            - Metric for the DHCP default route.
        type: int
    zone_name:
        description:
            - Name of the zone for the interface.
            - If the zone does not exist it is created.
            - If the zone already exists its mode should match I(mode).
        type: str
    vlan_name:
        description:
            - The VLAN to put this interface in.
            - If the VLAN does not exist it is created.
            - Only specify this if I(mode=layer2).
        type: str
    vr_name:
        description:
            - Name of the virtual router; it must already exist.
        type: str
        default: "default"
    vsys_dg:
        description:
            - B(Deprecated)
            - Use I(vsys) to specify the vsys instead.
            - HORIZONTALLINE
            - Name of the vsys (if firewall) or device group (if panorama) to put this object.
        type: str
"""

EXAMPLES = """
# Create ethernet1/1 as DHCP.
- name: enable DHCP client on ethernet1/1 in zone public
  paloaltonetworks.panos.panos_interface:
    provider: '{{ provider }}'
    if_name: "ethernet1/1"
    zone_name: "public"
    create_default_route: "yes"

# Update ethernet1/2 with a static IP address in zone dmz.
- name: ethernet1/2 as static in zone dmz
  paloaltonetworks.panos.panos_interface:
    provider: '{{ provider }}'
    if_name: "ethernet1/2"
    mode: "layer3"
    ip: ["10.1.1.1/24"]
    enable_dhcp: false
    zone_name: "dmz"
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
        vsys = module.params["vsys"]
        vsys_dg = module.params["vsys_dg"]

        # TODO(gfreeman) - Remove vsys_dg in 2.12, as well as this code chunk.
        # In the mean time, we'll need to do this special handling.
        if vsys_dg is not None:
            module.deprecate(
                'Param "vsys_dg" is deprecated, use "vsys"',
                version="4.0.0",
                collection_name="paloaltonetworks.panos",
            )
            if vsys is None:
                vsys = vsys_dg
            else:
                msg = [
                    'Params "vsys" and "vsys_dg" both given',
                    "Specify one or the other, not both.",
                ]
                module.fail_json(msg=".  ".join(msg))
        elif vsys is None and module.params["state"] != "merged":
            # TODO(gfreeman) - v2.12, just set the default for vsys to 'vsys1'.
            vsys = "vsys1"

        module.params["vsys"] = vsys

    def spec_handling(self, spec, module):
        if module.params["state"] not in ("present", "replaced"):
            return

        spec["enable_dhcp"] = True if module.params["enable_dhcp"] else None

        if spec["enable_dhcp"] is None:
            spec["create_dhcp_default_route"] = None
            spec["dhcp_default_route_metric"] = None
        else:
            spec["create_dhcp_default_route"] = bool(spec["create_dhcp_default_route"])


def main():
    helper = get_connection(
        helper_cls=Helper,
        vsys_importable=True,
        template=True,
        with_classic_provider_spec=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        min_pandevice_version=(0, 8, 0),
        with_commit=True,
        with_set_vlan_reference=True,
        with_set_vsys_reference=True,
        with_set_zone_reference=True,
        with_set_virtual_router_reference=True,
        sdk_cls=("network", "EthernetInterface"),
        sdk_params=dict(
            if_name=dict(required=True, sdk_param="name"),
            mode=dict(
                default="layer3",
                choices=[
                    "layer3",
                    "layer2",
                    "virtual-wire",
                    "tap",
                    "ha",
                    "decrypt-mirror",
                    "aggregate-group",
                ],
            ),
            ip=dict(type="list", elements="str"),
            ipv6_enabled=dict(type="bool"),
            management_profile=dict(),
            mtu=dict(type="int"),
            adjust_tcp_mss=dict(type="bool"),
            netflow_profile=dict(),
            lldp_enabled=dict(),
            lldp_profile=dict(),
            netflow_profile_l2=dict(),
            link_speed=dict(choices=["auto", "10", "100", "1000"]),
            link_duplex=dict(choices=["auto", "full", "half"]),
            link_state=dict(choices=["auto", "up", "down"]),
            aggregate_group=dict(),
            comment=dict(),
            ipv4_mss_adjust=dict(type="int"),
            ipv6_mss_adjust=dict(type="int"),
            enable_dhcp=dict(type="bool", default=True),
            create_default_route=dict(
                type="bool", default=False, sdk_param="create_dhcp_default_route"
            ),
            dhcp_default_route_metric=dict(type="int"),
        ),
        extra_params=dict(
            # TODO(gfreeman) - remove this in 2.12.
            vsys_dg=dict(),
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
