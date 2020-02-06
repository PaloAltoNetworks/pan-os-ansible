#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: panos_nat_rule_facts
short_description: Get information about a NAT rule.
description:
    - Get information about one or more NAT rules.
author: "Garfield Lee Freeman (@shinmog)"
version_added: "2.9"
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
    rule_regex:
        description:
            - A regex to match against the rule name.
            - Mutually exclusive with rule_name, listing, and uuid.
    uuid:
        description:
            - Match the given rule UUID (PAN-OS 9.0+).
            - Mutually exclusive with rule_name, listing, and rule_regex.
'''

EXAMPLES = '''
- name: Get a list of all NAT rules
  panos_nat_rule_facts:
    provider: '{{ provider }}'
    listing: true
  register: res1

- debug:
    msg: '{{ res1.listing }}'

- name: Get the NAT rule foo
  panos_nat_rule_facts:
    provider: '{{ provider }}'
    rule_name: 'foo'
  register: res2

- debug:
    msg: '{{ res2.object }}'
'''

RETURN = '''
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
'''


import re

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection


try:
    from pandevice.policies import NatRule
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def main():
    helper = get_connection(
        vsys=True,
        device_group=True,
        rulebase=True,
        with_classic_provider_spec=True,
        error_on_shared=True,
        required_one_of=[
            ['listing', 'rule_name', 'rule_regex', 'uuid'],
        ],
        argument_spec=dict(
            listing=dict(type='bool'),
            rule_name=dict(),
            rule_regex=dict(),
            uuid=dict(),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=False,
        required_one_of=helper.required_one_of,
    )

    parent = helper.get_pandevice_parent(module)

    renames = (
        ('name', 'rule_name'),
        ('fromzone', 'source_zone'),
        ('tozone', 'destination_zone'),
        ('source', 'source_ip'),
        ('destination', 'destination_ip'),
        ('source_translation_type', 'snat_type'),
        ('source_translation_static_translated_address', 'snat_static_address'),
        ('source_translation_static_bi_directional', 'snat_bidirectional'),
        ('source_translation_address_type', 'snat_address_type'),
        ('source_translation_interface', 'snat_interface'),
        ('source_translation_ip_address', 'snat_interface_address'),
        ('source_translation_translated_addresses', 'snat_dynamic_address'),
        ('destination_translated_address', 'dnat_address'),
        ('destination_translated_port', 'dnat_port'),
        ('tag', 'tag_val'),
    )

    if module.params['rule_name']:
        obj = NatRule(module.params['rule_name'])
        parent.add(obj)
        try:
            obj.refresh()
        except PanDeviceError as e:
            module.fail_json(msg='Failed refresh: {0}'.format(e))

        module.exit_json(
            changed=False,
            object=helper.to_module_dict(obj, renames),
        )

    try:
        listing = NatRule.refreshall(parent)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refreshall: {0}'.format(e))

    if module.params['uuid']:
        for x in listing:
            if x.uuid == module.params['uuid']:
                module.exit_json(
                    changed=False,
                    object=helper.to_module_dict(x, renames),
                )
        module.fail_json(msg='No rule with uuid "{0}"'.format(module.params['uuid']))

    ans = []
    matcher = None
    if module.params['rule_regex']:
        try:
            matcher = re.compile(module.params['rule_regex'])
        except Exception as e:
            module.fail_json(msg='Invalid regex: {0}'.format(e))

    ans = [
        helper.to_module_dict(x, renames)
        for x in listing
        if module.params['listing'] or matcher.search(x.uid) is not None
    ]

    module.exit_json(changed=False, listing=ans)


if __name__ == '__main__':
    main()
