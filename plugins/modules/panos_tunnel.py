#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2018 Palo Alto Networks, Inc
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
module: panos_tunnel
short_description: Manage tunnel interfaces
description:
    - Manage tunnel interfaces on PanOS
author: "Joshua Colson (@freakinhippie)"
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPi U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPi U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is supported.
    - Panorama is supported.
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
            - Interface management profile name; it must already exist.
        type: str
    mtu:
        description:
            - MTU for tunnel interface.
        type: int
    netflow_profile:
        description:
            - Netflow profile for tunnel interface.
        type: str
    comment:
        description:
            - Interface comment.
        type: str
    zone_name:
        description:
            - Name of the zone for the interface. If the zone does not exist it is created but
              if the zone exists and it is not of the correct mode the operation will fail.
        type: str
    vr_name:
        description:
            - Name of the virtual router; it must already exist.
        type: str
    vsys_dg:
        description:
            - B(Deprecated)
            - Use I(vsys) to specify the vsys instead.
            - HORIZONTALLINE
            - Name of the vsys (if firewall) or device group (if panorama) to put this object.
        type: str
"""

EXAMPLES = """
# Create tunnel.1
- name: create tunnel.1
  paloaltonetworks.panos.panos_tunnel:
    provider: '{{ provider }}'
    if_name: "tunnel.1"
    ip: ["10.1.1.1/32"]

# Update tunnel comment.
- name: update tunnel.1 comment
  paloaltonetworks.panos.panos_tunnel:
    provider: '{{ provider }}'
    if_name: "tunnel.1"
    ip: ["10.1.1.1/32"]
    comment: "tunnel interface"
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
        virtual_router_reference_default=None,
        default_zone_mode="layer3",
        sdk_cls=("network", "TunnelInterface"),
        sdk_params=dict(
            if_name=dict(required=True, sdk_param="name"),
            ip=dict(type="list", elements="str"),
            ipv6_enabled=dict(type="bool"),
            management_profile=dict(),
            mtu=dict(type="int"),
            netflow_profile=dict(),
            comment=dict(),
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
