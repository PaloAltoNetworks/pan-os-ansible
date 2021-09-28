#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2017 Palo Alto Networks, Inc
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
module: panos_nat_rule
short_description: create a policy NAT rule
description:
    - Create a policy nat rule. Keep in mind that we can either end up configuring source NAT, destination NAT, or both.
    - Instead of splitting it into two we will make a fair attempt to determine which one the user wants.
author:
    - Luigi Mori (@jtschichold)
    - Ivan Bojer (@ivanbojer)
    - Robert Hagen (@stealthllama)
    - Michael Richardson (@mrichardson03)
    - Garfield Lee Freeman (@shinmog)
    - Ken Celenza (@itdependsnetworks)
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is supported.
    - Panorama is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.state
    - paloaltonetworks.panos.fragments.device_group
    - paloaltonetworks.panos.fragments.vsys
    - paloaltonetworks.panos.fragments.rulebase
    - paloaltonetworks.panos.fragments.deprecated_commit
options:
    state:
        description:
            - The state of the NAT rule.
        type: str
        choices:
            - present
            - absent
            - enable
            - disable
        default: "present"
    operation:
        description:
            - B(Removed)
            - Use I(state) instead.
        type: str
    devicegroup:
        description:
            - B(Deprecated)
            - Use I(device_group) instead.
            - HORIZONTALLINE
            - The device group to place the NAT rule into.
            - Panorama only; ignored for firewalls.
        type: str
    tag:
        description:
            - Administrative tags.
        type: list
        elements: str
    tag_name:
        description:
            - B(Deprecated)
            - Use I(tag) instead.
            - HORIZONTALLINE
            - Administrative tag.
        type: str
    rule_name:
        description:
            - name of the SNAT rule
        type: str
        required: true
    description:
        description:
            - NAT rule description.
        type: str
    nat_type:
        description:
            - Type of NAT.
        type: str
        choices:
            - ipv4
            - nat64
            - nptv6
        default: "ipv4"
    source_zone:
        description:
            - list of source zones
        type: list
        elements: str
    source_ip:
        description:
            - list of source addresses
        required: false
        type: list
        elements: str
        default: ["any"]
    destination_zone:
        description:
            - destination zone
        type: str
    destination_ip:
        description:
            - list of destination addresses
        required: false
        type: list
        elements: str
        default: ["any"]
    to_interface:
        description:
            - Original packet's destination interface.
        type: str
        default: 'any'
    service:
        description:
            - service
        type: str
        default: "any"
    snat_type:
        description:
            - type of source translation
        type: str
        choices:
            - static-ip
            - dynamic-ip
            - dynamic-ip-and-port
    snat_address_type:
        description:
            - type of source translation.
        type: str
        choices:
            - interface-address
            - translated-address
        default: 'interface-address'
    snat_static_address:
        description:
            - Source NAT translated address. Used with Static-IP translation.
        type: str
    snat_dynamic_address:
        description:
            - Source NAT translated address.
            - Used when I(snat_type=dynamic-ip) or I(snat_type=dynamic-ip-and-port).
        type: list
        elements: str
    snat_interface:
        description:
            - snat interface
        type: str
    snat_interface_address:
        description:
            - snat interface address
        type: str
    snat_bidirectional:
        description:
            - bidirectional flag
        type: bool
    dnat_address:
        description:
            - Static dnat translated address
            - Mutually exclusive with I(dnat_dynamic_address), I(dnat_dynamic_port), and I(dnat_dynamic_distribution).
        type: str
    dnat_port:
        description:
            - Static dnat translated port
            - Mutually exclusive with I(dnat_dynamic_address), I(dnat_dynamic_port), and I(dnat_dynamic_distribution).
        type: str
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
            - If I(location=before) or I(location=after), this option specifies an existing
              rule name.  The new rule will be created in the specified position relative to this
              rule.
            - If I(location=before) or I(location=after), I(existing_rule) is required.
        type: str
    target:
        description:
            - Apply this rule exclusively to the listed firewalls in Panorama.
        type: list
        elements: str
    negate_target:
        description:
            - Exclude this rule from the listed firewalls in Panorama.
        type: bool
    group_tag:
        description:
            - The group tag.
        type: str
    dnat_dynamic_address:
        description:
            - Dynamic destination translated address.
            - Mutually exclusive with I(dnat_address) and I(dnat_port).
        type: str
    dnat_dynamic_port:
        description:
            - Dynamic destination translated port.
            - Mutually exclusive with I(dnat_address) and I(dnat_port).
        type: int
    dnat_dynamic_distribution:
        description:
            - Dynamic destination translated distribution.
            - Mutually exclusive with I(dnat_address) and I(dnat_port).
        type: str
    audit_comment:
        description:
            - Add an audit comment to the rule being defined.
        type: str
"""

EXAMPLES = """
# Create a source and destination nat rule
- name: Create NAT SSH rule for 10.0.1.101
  panos_nat_rule:
    provider: '{{ provider }}'
    rule_name: "Web SSH"
    source_zone: ["external"]
    destination_zone: "external"
    source_ip: ["any"]
    destination_ip: ["10.0.0.100"]
    service: "service-tcp-221"
    snat_type: "dynamic-ip-and-port"
    snat_interface: "ethernet1/2"
    dnat_address: "10.0.1.101"
    dnat_port: "22"

- name: disable a specific security rule
  panos_nat_rule:
    provider: '{{ provider }}'
    rule_name: 'Prod-Legacy 1'
    state: 'disable'
"""

RETURN = """
# Default return values
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    eltostr,
    get_connection,
)

try:
    from panos.errors import PanDeviceError
    from panos.policies import NatRule
except ImportError:
    try:
        from pandevice.errors import PanDeviceError
        from pandevice.policies import NatRule
    except ImportError:
        pass


def create_nat_rule(**kwargs):
    nat_rule = NatRule(
        name=kwargs["rule_name"],
        description=kwargs["description"],
        fromzone=kwargs["source_zone"],
        source=kwargs["source_ip"],
        tozone=kwargs["destination_zone"],
        destination=kwargs["destination_ip"],
        service=kwargs["service"],
        to_interface=kwargs["to_interface"],
        nat_type=kwargs["nat_type"],
        group_tag=kwargs["group_tag"],
    )

    # Source translation: Static IP
    if kwargs["snat_type"] in ["static-ip"] and kwargs["snat_static_address"]:
        nat_rule.source_translation_type = kwargs["snat_type"]
        nat_rule.source_translation_static_translated_address = kwargs[
            "snat_static_address"
        ]
        # Bi-directional flag set?
        if kwargs["snat_bidirectional"]:
            nat_rule.source_translation_static_bi_directional = kwargs[
                "snat_bidirectional"
            ]

    # Source translation: Dynamic IP and port
    elif kwargs["snat_type"] in ["dynamic-ip-and-port"]:
        nat_rule.source_translation_type = kwargs["snat_type"]
        nat_rule.source_translation_address_type = kwargs["snat_address_type"]
        # Interface address?
        if kwargs["snat_interface"]:
            nat_rule.source_translation_interface = kwargs["snat_interface"]
            # Interface IP?
            if kwargs["snat_interface_address"]:
                nat_rule.source_translation_ip_address = kwargs[
                    "snat_interface_address"
                ]
        else:
            nat_rule.source_translation_translated_addresses = kwargs[
                "snat_dynamic_address"
            ]

    # Source translation: Dynamic IP
    elif kwargs["snat_type"] in ["dynamic-ip"]:
        if kwargs["snat_dynamic_address"]:
            nat_rule.source_translation_type = kwargs["snat_type"]
            nat_rule.source_translation_translated_addresses = kwargs[
                "snat_dynamic_address"
            ]
        else:
            return False

    # Destination translation
    if kwargs["dnat_address"]:
        nat_rule.destination_translated_address = kwargs["dnat_address"]
        if kwargs["dnat_port"]:
            nat_rule.destination_translated_port = kwargs["dnat_port"]

    # Dynamic destination translation
    if kwargs["dnat_dynamic_address"]:
        nat_rule.destination_dynamic_translated_address = kwargs["dnat_dynamic_address"]
    if kwargs["dnat_dynamic_port"]:
        nat_rule.destination_dynamic_translated_port = kwargs["dnat_dynamic_port"]
    if kwargs["dnat_dynamic_distribution"]:
        nat_rule.destination_dynamic_translated_distribution = kwargs[
            "dnat_dynamic_distribution"
        ]

    # Any tags?
    if "tag_val" in kwargs:
        nat_rule.tag = kwargs["tag_val"]

    nat_rule.target = kwargs["target"]
    nat_rule.negate_target = kwargs["negate_target"]

    return nat_rule


def main():
    helper = get_connection(
        with_classic_provider_spec=True,
        vsys=True,
        device_group=True,
        rulebase=True,
        error_on_firewall_shared=True,
        min_pandevice_version=(1, 5, 0),
        argument_spec=dict(
            rule_name=dict(required=True),
            description=dict(),
            nat_type=dict(default="ipv4", choices=["ipv4", "nat64", "nptv6"]),
            source_zone=dict(type="list", elements="str"),
            source_ip=dict(type="list", elements="str", default=["any"]),
            destination_zone=dict(type="str"),
            destination_ip=dict(type="list", elements="str", default=["any"]),
            to_interface=dict(default="any"),
            service=dict(default="any"),
            snat_type=dict(choices=["static-ip", "dynamic-ip-and-port", "dynamic-ip"]),
            snat_address_type=dict(
                choices=["interface-address", "translated-address"],
                default="interface-address",
            ),
            snat_static_address=dict(),
            snat_dynamic_address=dict(type="list", elements="str"),
            snat_interface=dict(),
            snat_interface_address=dict(),
            snat_bidirectional=dict(type="bool"),
            dnat_address=dict(),
            dnat_port=dict(),
            dnat_dynamic_address=dict(),
            dnat_dynamic_port=dict(type="int"),
            dnat_dynamic_distribution=dict(),
            tag=dict(type="list", elements="str"),
            state=dict(
                default="present", choices=["present", "absent", "enable", "disable"]
            ),
            location=dict(choices=["top", "bottom", "before", "after"]),
            existing_rule=dict(),
            target=dict(type="list", elements="str"),
            negate_target=dict(type="bool"),
            commit=dict(type="bool", default=False),
            audit_comment=dict(),
            # TODO(gfreeman) - remove later.
            tag_name=dict(),
            devicegroup=dict(),
            operation=dict(),
            group_tag=dict(),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # TODO(gfreeman) - remove later.
    if module.params["operation"] is not None:
        module.fail_json(msg='Param "operation" is removed; use "state"')
    if module.params["devicegroup"] is not None:
        module.deprecate(
            'Param "devicegroup" is deprecated; use "device_group"',
            version="3.0.0",
            collection_name="paloaltonetworks.panos",
        )
        module.params["device_group"] = module.params["devicegroup"]
    if module.params["tag_name"] is not None:
        tag_val = module.params["tag_name"]
        module.deprecate(
            'Param "tag_name" is deprecated; use "tag"',
            version="3.0.0",
            collection_name="paloaltonetworks.panos",
        )
        if module.params["tag"]:
            module.fail_json(msg='Both "tag" and "tag_name" specified, use only one')
    else:
        tag_val = module.params["tag"]

    parent = helper.get_pandevice_parent(module)

    # Get object params.
    rule_name = module.params["rule_name"]
    description = module.params["description"]
    source_zone = module.params["source_zone"]
    source_ip = module.params["source_ip"]
    destination_zone = module.params["destination_zone"]
    destination_ip = module.params["destination_ip"]
    service = module.params["service"]
    to_interface = module.params["to_interface"]
    nat_type = module.params["nat_type"]
    snat_type = module.params["snat_type"]
    snat_address_type = module.params["snat_address_type"]
    snat_static_address = module.params["snat_static_address"]
    snat_dynamic_address = module.params["snat_dynamic_address"]
    snat_interface = module.params["snat_interface"]
    snat_interface_address = module.params["snat_interface_address"]
    snat_bidirectional = module.params["snat_bidirectional"]
    dnat_address = module.params["dnat_address"]
    dnat_port = module.params["dnat_port"]
    dnat_dynamic_address = module.params["dnat_dynamic_address"]
    dnat_dynamic_port = module.params["dnat_dynamic_port"]
    dnat_dynamic_distribution = module.params["dnat_dynamic_distribution"]

    # Get other info.
    state = module.params["state"]
    location = module.params["location"]
    existing_rule = module.params["existing_rule"]
    target = module.params["target"]
    negate_target = module.params["negate_target"]

    # Sanity check the location / existing_rule params.
    if location in ("before", "after") and not existing_rule:
        module.fail_json(
            msg="'existing_rule' must be specified if location is 'before' or 'after'."
        )

    # Get the current NAT rules.
    try:
        rules = NatRule.refreshall(parent)
    except PanDeviceError as e:
        module.fail_json(msg="Failed NAT refreshall: {0}".format(e))

    # Create the desired rule.
    new_rule = create_nat_rule(
        rule_name=rule_name,
        description=description,
        tag_val=tag_val,
        source_zone=source_zone,
        destination_zone=destination_zone,
        source_ip=source_ip,
        destination_ip=destination_ip,
        service=service,
        to_interface=to_interface,
        nat_type=nat_type,
        snat_type=snat_type,
        snat_address_type=snat_address_type,
        snat_static_address=snat_static_address,
        snat_dynamic_address=snat_dynamic_address,
        snat_interface=snat_interface,
        snat_interface_address=snat_interface_address,
        snat_bidirectional=snat_bidirectional,
        dnat_address=dnat_address,
        dnat_port=dnat_port,
        dnat_dynamic_address=dnat_dynamic_address,
        dnat_dynamic_port=dnat_dynamic_port,
        dnat_dynamic_distribution=dnat_dynamic_distribution,
        target=target,
        negate_target=negate_target,
        group_tag=module.params["group_tag"],
    )

    if not new_rule:
        module.fail_json(msg="Incorrect NAT rule params specified; quitting")

    # Perform the desired operation.
    changed = False
    diff = None
    if state in ("enable", "disable"):
        for rule in rules:
            if rule.name == new_rule.name:
                break
        else:
            module.fail_json(msg='Rule "{0}" not present'.format(new_rule.name))
        if state == "enable" and rule.disabled:
            changed = True
        elif state == "disable" and not rule.disabled:
            changed = True
        if changed:
            diff = dict(before=eltostr(rule))
            rule.disabled = not rule.disabled
            diff["after"] = eltostr(rule)
            if not module.check_mode:
                try:
                    rule.update("disabled")
                except PanDeviceError as e:
                    module.fail_json(msg="Failed enable: {0}".format(e))
    else:
        parent.add(new_rule)
        changed, diff = helper.apply_state(new_rule, rules, module)
        if state == "present":
            changed |= helper.apply_position(new_rule, location, existing_rule, module)

    # Audit comment.
    if changed and module.params["audit_comment"] and not module.check_mode:
        new_rule.opstate.audit_comment.update(module.params["audit_comment"])

    if changed and module.params["commit"]:
        helper.commit(module)

    module.exit_json(changed=changed, diff=diff, msg="Done")


if __name__ == "__main__":
    main()
