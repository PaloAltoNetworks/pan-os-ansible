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
module: panos_loopback_interface
short_description: Manage network loopback interfaces
description:
    - Manage loopback interfaces on PanOS
author:
    - Geraint Jones (@nexus_moneky_nz)
    - Garfield Lee Freeman (@shinmog)
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPi U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPi U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is supported.
    - Panorama is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.vsys_import
    - paloaltonetworks.panos.fragments.template_only
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
    - paloaltonetworks.panos.fragments.deprecated_commit
options:
    if_name:
        description:
            - Name of the interface to configure.
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
            - MTU for loopback interface.
        type: int
    adjust_tcp_mss:
        description:
            - Adjust TCP MSS.
        type: bool
    netflow_profile:
        description:
            - Netflow profile for loopback interface.
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
    zone_name:
        description:
            - Name of the zone for the interface. If the zone does not exist it is created but if the
            - zone exists and it is not of the correct mode the operation will fail.
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
# Delete loopback.1
- name: delete loopback.1
  paloaltonetworks.panos.panos_loopback_interface:
    provider: '{{ provider }}'
    if_name: "loopback.1"
    state: 'absent'

# Update/create loopback comment.
- name: update loopback.1 comment
  paloaltonetworks.panos.panos_loopback_interface:
    provider: '{{ provider }}'
    if_name: "loopback.1"
    ip: ["10.1.1.1/32"]
    comment: "Loopback iterface"
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
        elif vsys is None:
            # TODO(gfreeman) - v2.12, just set the default for vsys to 'vsys1'.
            vsys = "vsys1"

        # Make sure 'vsys' is set appropriately.
        module.params["vsys"] = vsys


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
        with_set_vsys_reference=True,
        with_set_zone_reference=True,
        with_set_virtual_router_reference=True,
        default_zone_mode="layer3",
        sdk_cls=("network", "LoopbackInterface"),
        sdk_params=dict(
            if_name=dict(required=True, sdk_param="name"),
            ip=dict(type="list", elements="str"),
            ipv6_enabled=dict(type="bool"),
            management_profile=dict(),
            mtu=dict(type="int"),
            adjust_tcp_mss=dict(type="bool"),
            netflow_profile=dict(),
            comment=dict(),
            ipv4_mss_adjust=dict(type="int"),
            ipv6_mss_adjust=dict(type="int"),
        ),
        extra_params=dict(
            # TODO(gfreeman) - remove this in 2.12
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
