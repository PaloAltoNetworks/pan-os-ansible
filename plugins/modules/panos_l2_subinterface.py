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
module: panos_l2_subinterface
short_description: Manage layer2 subinterface
description:
    - Manage a layer2 subinterface.
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
    lldp_enabled:
        description:
            - Enable LLDP
        type: bool
    lldp_profile:
        description:
            - Reference to an LLDP profile
        type: str
    netflow_profile:
        description:
            - Reference to a netflow profile.
        type: str
    comment:
        description:
            - Interface comment.
        type: str
    zone_name:
        description:
            - Name of the zone for the interface.
            - If the zone does not exist it is created.
        type: str
    vlan_name:
        description:
            - The VLAN to put this interface in.
            - If the VLAN does not exist it is created.
        type: str
"""

EXAMPLES = """
# Create ethernet1/1.5
- name: ethernet1/1.5 in zone sales
  paloaltonetworks.panos.panos_l2_subinterface:
    provider: '{{ provider }}'
    name: "ethernet1/1.5"
    tag: 5
    zone_name: "sales"
    vlan_name: "myVlan"
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

        eth.mode = "layer2"
        parent.add(eth)
        return eth


def main():
    helper = get_connection(
        helper_cls=Helper,
        vsys_importable=True,
        template=True,
        with_classic_provider_spec=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        min_pandevice_version=(0, 8, 0),
        with_set_vlan_reference=True,
        with_set_zone_reference=True,
        with_set_vsys_reference=True,
        default_zone_mode="layer2",
        sdk_cls=("network", "Layer2Subinterface"),
        sdk_params=dict(
            name=dict(required=True),
            tag=dict(required=True, type="int"),
            lldp_enabled=dict(type="bool"),
            lldp_profile=dict(),
            netflow_profile=dict(sdk_param="netflow_profile_l2"),
            comment=dict(),
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
