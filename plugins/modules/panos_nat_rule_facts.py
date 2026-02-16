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
module: panos_nat_rule_facts
short_description: Get information about a NAT rule.
description:
    - Get information about one or more NAT rules.
author: "Garfield Lee Freeman (@shinmog)"
version_added: '1.0.0'
deprecated:
    alternative: Use M(paloaltonetworks.panos.panos_nat_rule2) with I(state=gathered).
    removed_in: '4.0.0'
    why: Updating module design to network resource modules.
requirements:
    - pan-python
    - pandevice
notes:
    - Checkmode is not supported.
    - Panorama is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.device_group
    - paloaltonetworks.panos.fragments.vsys
    - paloaltonetworks.panos.fragments.rulebase
options:
    listing:
        description:
            - Return all rules.
            - Mutually exclusive with rule_name, rule_regex, and uuid.
        type: bool
    rule_name:
        description:
            - Name of the rule.
            - Mutually exclusive with rule_regex, listing, and uuid.
        type: str
    rule_regex:
        description:
            - A regex to match against the rule name.
            - Mutually exclusive with rule_name, listing, and uuid.
        type: str
    uuid:
        description:
            - Match the given rule UUID (PAN-OS 9.0+).
            - Mutually exclusive with rule_name, listing, and rule_regex.
        type: str
"""

EXAMPLES = """
- name: Get a list of all NAT rules
  paloaltonetworks.panos.panos_nat_rule_facts:
    provider: '{{ provider }}'
    listing: true
  register: res1

- debug:
    msg: '{{ res1.listing }}'

- name: Get the NAT rule foo
  paloaltonetworks.panos.panos_nat_rule_facts:
    provider: '{{ provider }}'
    rule_name: 'foo'
  register: res2

- debug:
    msg: '{{ res2.object }}'
"""

RETURN = """
object:
    description: Single rule definition
    returned: When I(rule_name) or I(uuid) is specified
    type: complex
    contains:
        description:
            description: Description
            type: str
        destination_ip:
            description: Destination addresses
            type: list
        destination_zone:
            description: To zones
            type: list
        dnat_address:
            description: Destination NAT translated address
            type: str
        dnat_port:
            description: Destination NAT translated port
            type: int
        nat_type:
            description: The NAT type
            type: str
        rule_name:
            description: Rule name
            type: str
        service:
            description: The service
            type: str
        snat_address_type:
            description: Type of source translation
            type: str
        snat_bidirectional:
            description: Bidirectional flag
            type: bool
        snat_dynamic_address:
            description: Source NAT translated address
            type: list
        snat_interface:
            description: Source NAT interface
            type: str
        snat_interface_address:
            description: SNAT interface address
            type: str
        snat_static_address:
            description: Static IP SNAT translated address
            type: str
        snat_type:
            description: Type of source translation
            type: str
        source_ip:
            description: Source addresses
            type: list
        source_zone:
            description: Source zone
            type: list
        tag_val:
            description: Administrative tags for this rule
            type: list
        to_interface:
            description: Egress interface from route lookup
            type: str
        uuid:
            description: The UUID of the rule (PAN-OS 9.0+)
            type: str
listing:
    description: List of rules
    returned: When I(listing) or I(rule_regex) is set
    type: list
"""


import re

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
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


def main():
    helper = get_connection(
        vsys=True,
        device_group=True,
        rulebase=True,
        with_classic_provider_spec=True,
        error_on_firewall_shared=True,
        required_one_of=[
            ["listing", "rule_name", "rule_regex", "uuid"],
        ],
        ansible_to_sdk_param_mapping={
            "rule_name": "name",
            "source_zone": "fromzone",
            "destination_zone": "tozone",
            "source_ip": "source",
            "destination_ip": "destination",
            "snat_type": "source_translation_type",
            "snat_static_address": "source_translation_static_translated_address",
            "snat_bidirectional": "source_translation_static_bi_directional",
            "snat_address_type": "source_translation_address_type",
            "snat_interface": "source_translation_interface",
            "snat_interface_address": "source_translation_ip_address",
            "snat_dynamic_address": "source_translation_translated_addresses",
            "dnat_address": "destination_translated_address",
            "dnat_port": "destination_translated_port",
            "tag_val": "tag",
        },
        argument_spec=dict(
            listing=dict(type="bool"),
            rule_name=dict(),
            rule_regex=dict(),
            uuid=dict(),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    module.deprecate(
        "Deprecated; use panos_nat_rule2 with state=gathered instead",
        version="4.0.0",
        collection_name="paloaltonetworks.panos",
    )

    parent = helper.get_pandevice_parent(module)

    if module.params["rule_name"]:
        obj = NatRule(module.params["rule_name"])
        parent.add(obj)
        try:
            obj.refresh()
        except PanDeviceError as e:
            module.fail_json(msg="Failed refresh: {0}".format(e))

        module.exit_json(
            changed=False,
            object=helper.describe(obj),
        )

    try:
        listing = NatRule.refreshall(parent)
    except PanDeviceError as e:
        module.fail_json(msg="Failed refreshall: {0}".format(e))

    if module.params["uuid"]:
        for x in listing:
            if x.uuid == module.params["uuid"]:
                module.exit_json(
                    changed=False,
                    object=helper.describe(x),
                )
        module.fail_json(msg='No rule with uuid "{0}"'.format(module.params["uuid"]))

    ans = []
    matcher = None
    if module.params["rule_regex"]:
        try:
            matcher = re.compile(module.params["rule_regex"])
        except Exception as e:
            module.fail_json(msg="Invalid regex: {0}".format(e))

    ans = [
        x
        for x in listing
        if module.params["listing"] or matcher.search(x.uid) is not None
    ]

    module.exit_json(changed=False, listing=helper.describe(ans))


if __name__ == "__main__":
    main()
