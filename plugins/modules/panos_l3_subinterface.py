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
module: panos_l3_subinterface
short_description: Manage layer3 subinterface
description:
    - Manage a layer3 subinterface.
author: "Garfield Lee Freeman (@shinmog)"
version_added: '1.0.0'
requirements:
    - pan-python
    - pandevice >= 0.8.0
notes:
    - Panorama is supported.
    - Checkmode is supported.
    - If the PAN-OS device is a firewall and I(vsys) is not specified, then
      the vsys will default to I(vsys=vsys1).
    - If the PAN-OS device is a Panorama, I(vsys) should be specified,
      otherwise the default is I(null), and I(zone-name) assignment will fail.
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
        type: str
    parent_interface:
        description:
            - Name of the parent interface
        type: str
    tag:
        description:
            - Tag (vlan id) for the interface
        type: int
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
        type: str
    vr_name:
        description:
            - Virtual router to add this interface to.
        type: str
        default: 'default'
"""

EXAMPLES = """
# Create ethernet1/1.5 as DHCP.
- name: enable DHCP client on ethernet1/1.5 in zone public
  paloaltonetworks.panos.panos_l3_subinterface:
    provider: '{{ provider }}'
    name: "ethernet1/1.5"
    tag: 1
    create_default_route: true
    zone_name: "public"

# Update ethernet1/2.7 with a static IP address in zone dmz.
- name: ethernet1/2.7 as static in zone dmz
  paloaltonetworks.panos.panos_l3_subinterface:
    provider: '{{ provider }}'
    name: "ethernet1/2.7"
    tag: 7
    enable_dhcp: false
    ip: ["10.1.1.1/24"]
    zone_name: "dmz"
"""

RETURN = """
# Default return values
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    ConnectionHelper,
    get_connection,
    to_sdk_cls,
)


class Helper(ConnectionHelper):
    def initial_handling(self, module):
        # Sanity check.
        name_set = True if module.params["name"] is not None else False
        parent_set = True if module.params["parent_interface"] is not None else False

        if module.params["state"] == "gathered" and not parent_set:
            module.fail_json(
                msg="'parent_interface' is required when state is 'gathered'."
            )

        if name_set:
            if "." not in module.params["name"]:
                module.fail_json(
                    msg="Subinterface name does not have '.' in it: {0}".format(
                        module.params["name"]
                    )
                )
            if (
                parent_set
                and module.params["parent_interface"] not in module.params["name"]
            ):
                module.fail_json(
                    msg="Parent and subinterface names do not match: {0} - {1}".format(
                        module.params["parent_interface"], module.params["name"]
                    )
                )

        if module.params["state"] not in ("present", "replaced"):
            return

        if module.params["vsys"] is None:
            module.params["vsys"] = "vsys1"

    def parent_handling(self, parent, module):
        if module.params["parent_interface"] is not None:
            iname = module.params["parent_interface"]
        else:
            iname = module.params["name"].split(".")[0]

        if iname.startswith("ae"):
            eth = to_sdk_cls("network", "AggregateInterface")(iname)
        else:
            eth = to_sdk_cls("network", "EthernetInterface")(iname)

        eth.mode = "layer3"
        parent.add(eth)
        return eth

    def spec_handling(self, spec, module):
        if module.params["state"] not in ("present", "replaced"):
            return

        spec["enable_dhcp"] = True if module.params["enable_dhcp"] else None

        if not spec["create_dhcp_default_route"] and spec["enable_dhcp"] is None:
            spec["create_dhcp_default_route"] = None


def main():
    helper = get_connection(
        helper_cls=Helper,
        vsys_importable=True,
        template=True,
        with_classic_provider_spec=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        min_pandevice_version=(0, 8, 0),
        with_set_vsys_reference=True,
        with_set_zone_reference=True,
        with_set_virtual_router_reference=True,
        default_zone_mode="layer3",
        sdk_cls=("network", "Layer3Subinterface"),
        sdk_params=dict(
            name=dict(required=True),
            tag=dict(required=True, type="int"),
            ip=dict(type="list", elements="str"),
            ipv6_enabled=dict(type="bool"),
            management_profile=dict(),
            mtu=dict(type="int"),
            adjust_tcp_mss=dict(type="bool"),
            netflow_profile=dict(),
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
            parent_interface=dict(type="str"),
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
