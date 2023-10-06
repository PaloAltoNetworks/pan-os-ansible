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
module: panos_pbf_rule
short_description: Manage Policy Based Forwarding rules on PAN-OS.
description:
    - Manage Policy Based Forwarding rules on PAN-OS.
author:
    - Garfield Lee Freeman (@shinmog)
version_added: '1.0.0'
requirements:
    - pandevice >= 0.13.0
    - pan-python
notes:
    - Checkmode is supported.
    - Panorama is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
    - paloaltonetworks.panos.fragments.device_group
    - paloaltonetworks.panos.fragments.vsys
    - paloaltonetworks.panos.fragments.rulebase
    - paloaltonetworks.panos.fragments.uuid
    - paloaltonetworks.panos.fragments.target
    - paloaltonetworks.panos.fragments.movement
    - paloaltonetworks.panos.fragments.audit_comment
options:
    name:
        description:
            - Name of the rule.
        type: str
    description:
        description:
            - The description.
        type: str
    tags:
        description:
            - List of tags.
        type: list
        elements: str
    from_type:
        description:
            - Source from type.
        type: str
        choices:
            - zone
            - interface
        default: 'zone'
    from_value:
        description:
            - The source values for the given type.
        type: list
        elements: str
    source_addresses:
        description:
            - List of source IP addresses.
            - When referencing predefined EDLs, use config names of the EDLS not
              their full names. The config names can be found with the CLI...
              request system external-list show type predefined-ip name <tab>
                panw-bulletproof-ip-list   panw-bulletproof-ip-list
                panw-highrisk-ip-list      panw-highrisk-ip-list
                panw-known-ip-list         panw-known-ip-list
                panw-torexit-ip-list       panw-torexit-ip-list
        type: list
        elements: str
        default: ["any"]
    source_users:
        description:
            - List of source users.
        type: list
        elements: str
        default: ["any"]
    negate_source:
        description:
            - Set to negate the source.
        type: bool
    destination_addresses:
        description:
            - List of destination addresses.
            - When referencing predefined EDLs, use config names of the EDLS not
              their full names. The config names can be found with the CLI...
              request system external-list show type predefined-ip name <tab>
                panw-bulletproof-ip-list   panw-bulletproof-ip-list
                panw-highrisk-ip-list      panw-highrisk-ip-list
                panw-known-ip-list         panw-known-ip-list
                panw-torexit-ip-list       panw-torexit-ip-list
        type: list
        elements: str
        default: ["any"]
    negate_destination:
        description:
            - Set to negate the destination.
        type: bool
    applications:
        description:
            - List of applications.
        type: list
        elements: str
        default: ["any"]
    services:
        description:
            - List of services.
        type: list
        elements: str
        default: ["any"]
    schedule:
        description:
            - The schedule.
        type: str
    disabled:
        description:
            - Disable this rule.
        type: bool
    action:
        description:
            - The action to take.
        type: str
        choices:
            - forward
            - forward-to-vsys
            - discard
            - no-pbf
        default: 'forward'
    forward_vsys:
        description:
            - The vsys to forward to if action is set to forward to a vsys.
        type: str
    forward_egress_interface:
        description:
            - The egress interface.
        type: str
    forward_next_hop_type:
        description:
            - The next hop type.
            - Leave this as None for a next hop type of 'None'.
            - To specify a next-hop of none, leave this parameter unset.
        type: str
        choices:
            - ip-address
            - fqdn
    forward_next_hop_value:
        description:
            - The next hop value if forward next hop type is not None.
        type: str
    forward_monitor_profile:
        description:
            - The monitor profile to use.
        type: str
    forward_monitor_ip_address:
        description:
            - The monitor IP address.
        type: str
    forward_monitor_disable_if_unreachable:
        description:
            - Set to disable this rule if nexthop / monitor IP is unreachable.
        type: bool
    enable_enforce_symmetric_return:
        description:
            - Set to enforce symmetric return.
        type: bool
    symmetric_return_addresses:
        description:
            - List of symmetric return addresses.
        type: list
        elements: str
    group_tag:
        description:
            - The group tag.
        type: str
"""

EXAMPLES = """
- name: add a pbf rule
  paloaltonetworks.panos.panos_pbf_rule:
    provider: '{{ provider }}'
    name: 'my-pbf'
    description: 'Made by Ansible'
    from_value: ['myZone']
    action: 'discard'
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
        rulebase=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        with_classic_provider_spec=True,
        error_on_firewall_shared=True,
        min_pandevice_version=(1, 5, 0),
        with_uuid=True,
        with_target=True,
        with_movement=True,
        with_audit_comment=True,
        sdk_cls=("policies", "PolicyBasedForwarding"),
        sdk_params=dict(
            name=dict(required=True),
            description=dict(),
            tags=dict(type="list", elements="str"),
            from_type=dict(choices=["zone", "interface"], default="zone"),
            from_value=dict(type="list", elements="str"),
            source_addresses=dict(type="list", elements="str", default=["any"]),
            source_users=dict(type="list", elements="str", default=["any"]),
            negate_source=dict(type="bool"),
            destination_addresses=dict(type="list", elements="str", default=["any"]),
            negate_destination=dict(type="bool"),
            applications=dict(type="list", elements="str", default=["any"]),
            services=dict(type="list", elements="str", default=["any"]),
            schedule=dict(),
            disabled=dict(type="bool"),
            action=dict(
                choices=["forward", "forward-to-vsys", "discard", "no-pbf"],
                default="forward",
            ),
            forward_vsys=dict(),
            forward_egress_interface=dict(),
            forward_next_hop_type=dict(choices=["ip-address", "fqdn"]),
            forward_next_hop_value=dict(),
            forward_monitor_profile=dict(),
            forward_monitor_ip_address=dict(),
            forward_monitor_disable_if_unreachable=dict(type="bool"),
            enable_enforce_symmetric_return=dict(type="bool"),
            symmetric_return_addresses=dict(type="list", elements="str"),
            group_tag=dict(),
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
