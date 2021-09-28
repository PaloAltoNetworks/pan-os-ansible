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
    - paloaltonetworks.panos.fragments.state
    - paloaltonetworks.panos.fragments.device_group
    - paloaltonetworks.panos.fragments.vsys
    - paloaltonetworks.panos.fragments.rulebase
options:
    name:
        description:
            - Name of the rule.
        type: str
        required: true
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
        type: str
        choices:
            - None
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
    location:
        description:
            - Position to place the created rule in the rule base.
        type: str
        choices:
            - top
            - bottom
            - before
            - after
    existing_rule:
        description:
            - If 'location' is set to 'before' or 'after', this option specifies an existing
              rule name.  The new rule will be created in the specified position relative to this
              rule.  If 'location' is set to 'before' or 'after', this option is required.
        type: str
    target:
        description:
            - For Panorama devices only.
            - Apply this rule exclusively to the listed firewalls in Panorama.
        type: list
        elements: str
    negate_target:
        description:
            - For Panorama devices only.
            - Exclude this rule from the listed firewalls in Panorama.
        type: bool
    group_tag:
        description:
            - The group tag.
        type: str
    audit_comment:
        description:
            - Add an audit comment to the rule being defined.
        type: str
"""

EXAMPLES = """
- name: add a pbf rule
  panos_pbf_rule:
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

try:
    from panos.errors import PanDeviceError
    from panos.policies import PolicyBasedForwarding
except ImportError:
    try:
        from pandevice.errors import PanDeviceError
        from pandevice.policies import PolicyBasedForwarding
    except ImportError:
        pass


def main():
    helper = get_connection(
        vsys=True,
        device_group=True,
        rulebase=True,
        with_state=True,
        with_classic_provider_spec=True,
        error_on_firewall_shared=True,
        min_pandevice_version=(1, 5, 0),
        argument_spec=dict(
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
            forward_next_hop_type=dict(choices=[None, "ip-address", "fqdn"]),
            forward_next_hop_value=dict(),
            forward_monitor_profile=dict(),
            forward_monitor_ip_address=dict(),
            forward_monitor_disable_if_unreachable=dict(type="bool"),
            enable_enforce_symmetric_return=dict(type="bool"),
            symmetric_return_addresses=dict(type="list", elements="str"),
            target=dict(type="list", elements="str"),
            negate_target=dict(type="bool"),
            location=dict(choices=["top", "bottom", "before", "after"]),
            existing_rule=dict(),
            group_tag=dict(),
            audit_comment=dict(),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # Verify imports, build pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    # Set the SecurityRule object params.
    rule_spec = {
        "name": module.params["name"],
        "description": module.params["description"],
        "tags": module.params["tags"],
        "from_type": module.params["from_type"],
        "from_value": module.params["from_value"],
        "source_addresses": module.params["source_addresses"],
        "source_users": module.params["source_users"],
        "negate_source": module.params["negate_source"],
        "destination_addresses": module.params["destination_addresses"],
        "negate_destination": module.params["negate_destination"],
        "applications": module.params["applications"],
        "services": module.params["services"],
        "schedule": module.params["schedule"],
        "disabled": module.params["disabled"],
        "action": module.params["action"],
        "forward_vsys": module.params["forward_vsys"],
        "forward_egress_interface": module.params["forward_egress_interface"],
        "forward_next_hop_type": module.params["forward_next_hop_type"],
        "forward_next_hop_value": module.params["forward_next_hop_value"],
        "forward_monitor_profile": module.params["forward_monitor_profile"],
        "forward_monitor_ip_address": module.params["forward_monitor_ip_address"],
        "forward_monitor_disable_if_unreachable": module.params[
            "forward_monitor_disable_if_unreachable"
        ],
        "enable_enforce_symmetric_return": module.params[
            "enable_enforce_symmetric_return"
        ],
        "symmetric_return_addresses": module.params["symmetric_return_addresses"],
        "target": module.params["target"],
        "negate_target": module.params["negate_target"],
        "group_tag": module.params["group_tag"],
    }

    # Other module info.
    location = module.params["location"]
    existing_rule = module.params["existing_rule"]

    # Retrieve the current rules.
    try:
        rules = PolicyBasedForwarding.refreshall(parent, add=False)
    except PanDeviceError as e:
        module.fail_json(msg="Failed refresh: {0}".format(e))

    # Create new rule object from the params.
    new_rule = PolicyBasedForwarding(**rule_spec)
    parent.add(new_rule)

    # Which action shall we take on the rule object?
    changed, diff = helper.apply_state(new_rule, rules, module)

    # Move the rule to the correct spot, if applicable.
    if module.params["state"] == "present":
        changed |= helper.apply_position(new_rule, location, existing_rule, module)

    # Audit comment.
    if changed and module.params["audit_comment"] and not module.check_mode:
        new_rule.opstate.audit_comment.update(module.params["audit_comment"])

    # Done.
    module.exit_json(changed=changed, diff=diff)


if __name__ == "__main__":
    main()
