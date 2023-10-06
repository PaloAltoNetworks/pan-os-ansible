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
module: panos_aggregate_interface
short_description: Manage aggregate network interfaces
description:
    - Manage aggregate network interfaces on PanOS
author:
    - Heiko Burghardt (@odysseus107)
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPi U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPi U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is supported.
    - Panorama is supported.
    - If the PAN-OS device is a Panorama, I(vsys) should be specified,
      otherwise the default is I(null), and I(zone-name) assignment will fail.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.vsys_import
    - paloaltonetworks.panos.fragments.template_only
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.deprecated_commit
    - paloaltonetworks.panos.fragments.gathered_filter
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
            - ha
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
            - MTU for aggregate interface.
        type: int
    adjust_tcp_mss:
        description:
            - Adjust TCP MSS.
        type: bool
    netflow_profile:
        description:
            - Netflow profile for aggregate interface.
        type: str
    lldp_enabled:
        description:
            - (Layer2) Enable LLDP
        type: bool
    lldp_profile:
        description:
            - (Layer2) Reference to an lldp profile
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
            - Enable DHCP on this interface
        type: bool
    create_dhcp_default_route:
        description:
            - Create default route pointing to default gateway provided by server
        type: bool
    dhcp_default_route_metric:
        description:
            - Metric for the DHCP default route
        type: int
    lacp_enable:
        description:
            - Enable LACP on this interface
        type: bool
    lacp_passive_pre_negotiation:
        description:
            - Enable LACP passive pre-negotiation
        type: bool
    lacp_rate:
        description:
            - Set LACP transmission rate
        type: str
        choices: ['fast', 'slow']
    lacp_mode:
        description:
            - Set LACP mode
        type: str
        choices: ['active', 'passive']
    lacp_fast_failover:
        description:
            - Enable LACP fast failover
        type: bool
    zone_name:
        description:
            - The zone to put this interface into.
        type: str
    vr_name:
        description:
            - The virtual router to associate with this interface.
        type: str
        default: default
"""

EXAMPLES = """
# Create ae1 interface.
- name: create ae1 interface with IP in untrust zone
  paloaltonetworks.panos.panos_aggregate_interface:
    provider: '{{ provider }}'
    if_name: "ae1"
    ip: '[ "192.168.0.1" ]'
    zone_name: 'untrust'
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


def main():
    helper = get_connection(
        helper_cls=Helper,
        vsys_importable=True,
        template=True,
        with_classic_provider_spec=True,
        with_network_resource_module_state=True,
        with_commit=True,
        with_set_vsys_reference=True,
        with_set_zone_reference=True,
        with_set_virtual_router_reference=True,
        with_gathered_filter=True,
        min_pandevice_version=(1, 9, 0),
        sdk_cls=("network", "AggregateInterface"),
        sdk_params=dict(
            if_name=dict(required=True, sdk_param="name"),
            mode=dict(
                default="layer3",
                choices=["layer3", "layer2", "virtual-wire", "ha"],
            ),
            ip=dict(type="list", elements="str"),
            ipv6_enabled=dict(type="bool"),
            management_profile=dict(),
            mtu=dict(type="int"),
            adjust_tcp_mss=dict(type="bool"),
            netflow_profile=dict(),
            lldp_enabled=dict(type="bool"),
            lldp_profile=dict(),
            comment=dict(),
            ipv4_mss_adjust=dict(type="int"),
            ipv6_mss_adjust=dict(type="int"),
            enable_dhcp=dict(type="bool"),
            create_dhcp_default_route=dict(type="bool"),
            dhcp_default_route_metric=dict(type="int"),
            lacp_enable=dict(type="bool"),
            lacp_passive_pre_negotiation=dict(type="bool"),
            lacp_rate=dict(type="str", choices=["fast", "slow"]),
            lacp_mode=dict(type="str", choices=["active", "passive"]),
            lacp_fast_failover=dict(type="bool"),
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
