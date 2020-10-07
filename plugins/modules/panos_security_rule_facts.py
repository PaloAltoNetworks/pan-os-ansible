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

DOCUMENTATION = '''
---
module: panos_security_rule_facts
short_description: Retrieve information about security rules.
description:
    - Retrieve information about security rules.
author:
    - 'Garfield Lee Freeman (@shinmog)'
    - 'Michael Richardson (@mrichardson03)'
version_added: '1.0.0'
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
    rule_name:
        description:
            - Name of the security rule.
        type: str
    names:
        description:
            - List of security rule names to return data for.
        type: list
        elements: str
    details:
        description:
            - Retrieve full details instead of just rule names.
            - Implied when I(names) is set and not using I(match_rules).
        type: bool
        aliases: ['all_details']
    match_rules:
        description:
            Returns security rule(s) in the policy that will match the
            specified traffic using the 'test security-policy-match' API
            command.
        type: dict
        suboptions:
            source_zone:
                description: Source zone
                type: str
                required: True
            source_ip:
                description: Source IP address
                type: str
                required: True
            source_user:
                description: Source user
                type: str
            destination_zone:
                description: Destination zone
                type: str
                required: True
            destination_ip:
                description: Destination IP address
                type: str
                required: True
            destination_port:
                description: Destination port
                type: str
                required: True
            protocol:
                description: IP protocol type
                type: str
                choices: ['tcp', 'udp', 'icmp']
                required: True
            application:
                description: Application name
                type: str
            category:
                description: URL filtering category
                type: str
            show_all:
                description: Show all potential matches until first allow rule
                type: bool
'''

EXAMPLES = '''
- name: Get a list of all security rules
  panos_security_rule_facts:
    provider: '{{ provider }}'
  register: sec_rules

- debug:
    msg: '{{ sec_rules.rule_names }}'

- name: Get the definition for rule 'HTTP Multimedia'
  panos_security_rule_facts:
    provider: '{{ provider }}'
    names:
        - 'HTTP Multimedia'
  register: rule1

- debug:
    msg: '{{ rule1.spec }}'

- name: Get rule names matching DNS traffic
  panos_security_rule_facts:
    provider: '{{ provider }}'
    match_rules:
      source_zone: 'trust'
      source_ip: '192.168.1.10'
      destination_zone: 'untrust'
      destination_ip: '8.8.8.8'
      destination_port: '53'
      protocol: 'udp'
  register: dns_rule

- debug:
    msg: '{{ dns_rule.spec }}'
'''

RETURN = '''
rule_names:
    description:
        List of security rules present, or matching traffic as specified in
        I(match_rules).
    returned: When I(details=False)
    type: list
    sample: ['rule1', 'rule2', 'rule3']
rule_details:
    description:
        Full details of requested security rules, or matching traffic as
        specified in I(match_rules).
    returned: When I(details=True)
    type: list
    elements: dict
    contains:
        rule_name:
            description: Name of the security rule.
            type: str
        source_zone:
            description: List of source zones.
            type: list
        source_ip:
            description: List of source addresses.
            type: list
        source_user:
            description: List of source users.
            type: list
        hip_profiles:
            description: GlobalProtect host information profile list.
            type: list
        destination_zone:
            description: List of destination zones.
            type: list
        destination_ip:
            description: List of destination addresses.
            type: list
        application:
            description: List of applications, application groups, and/or application filters.
            type: list
        service:
            description: List of services and/or service groups.
            type: list
        category:
            description: List of destination URL categories.
            type: list
        action:
            description: The rule action.
            type: str
        log_setting:
            description: Log forwarding profile.
            type: str
        log_start:
            description: Whether to log at session start.
            type: bool
        log_end:
            description: Whether to log at session end.
            type: bool
        description:
            description: Description of the security rule.
            type: str
        rule_type:
            description: Type of security rule (version 6.1 of PanOS and above).
            type: str
        tag_name:
            description: List of tags associated with the rule.
            type: list
        negate_source:
            description: Match on the reverse of the 'source_ip' attribute
            type: bool
        negate_destination:
            description: Match on the reverse of the 'destination_ip' attribute
            type: bool
        disabled:
            description: Disable this rule.
            type: bool
        schedule:
            description: Schedule in which this rule is active.
            type: str
        icmp_unreachable:
            description: Send 'ICMP Unreachable'.
            type: bool
        disable_server_response_inspection:
            description: Disables packet inspection from the server to the client.
            type: bool
        group_profile:
            description: Security profile group setting.
            type: str
        antivirus:
            description: Name of the already defined antivirus profile.
            type: str
        vulnerability:
            description: Name of the already defined vulnerability profile.
            type: str
        spyware:
            description: Name of the already defined spyware profile.
            type: str
        url_filtering:
            description: Name of the already defined url_filtering profile.
            type: str
        file_blocking:
            description: Name of the already defined file_blocking profile.
            type: str
        data_filtering:
            description: Name of the already defined data_filtering profile.
            type: str
        wildfire_analysis:
            description: Name of the already defined wildfire_analysis profile.
            type: str
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from panos.policies import SecurityRule
    from panos.errors import PanDeviceError
except ImportError:
    try:
        from pandevice.policies import SecurityRule
        from pandevice.errors import PanDeviceError
    except ImportError:
        pass


import xml.etree.ElementTree as ET


def match_rules(module, device):
    params = module.params['match_rules']
    rule_names = []

    spec = {}

    renames = [
        ('from', 'source_zone'),
        ('source', 'source_ip'),
        ('source-user', 'source_user'),
        ('to', 'destination_zone'),
        ('destination', 'destination_ip'),
        ('destination-port', 'destination_port'),
        ('application', 'application'),
        ('category', 'category')
    ]

    for s, p in renames:
        if params[p] is not None:
            spec[s] = params[p]

    if params['protocol'] == 'icmp':
        spec['protocol'] = '1'
    elif params['protocol'] == 'tcp':
        spec['protocol'] = '6'
    elif params['protocol'] == 'udp':
        spec['protocol'] = '17'

    if params['show_all']:
        spec['show-all'] = 'yes'

    # Build XML command, starting from 'security-policy-match' element.
    cmd = '<test><security-policy-match/></test>'
    tree = ET.fromstring(cmd)
    match = tree.find('.//security-policy-match')

    for element, text in spec.items():
        e = ET.SubElement(match, element)
        e.text = text

    cmd_str = ET.tostring(tree)
    result = device.op(cmd_str, cmd_xml=False)

    # Loop through 'entry' elements in XML result, get policy names.
    rules = result.findall('.//entry')
    for rule in rules:
        rule_names.append(rule.get('name'))

    return rule_names


def main():
    helper = get_connection(
        vsys=True,
        device_group=True,
        rulebase=True,
        with_classic_provider_spec=True,
        error_on_firewall_shared=True,
        argument_spec=dict(
            rule_name=dict(),
            names=dict(type='list', elements='str'),
            details=dict(default=False, type='bool', aliases=['all_details']),
            match_rules=dict(
                type='dict',
                options=dict(
                    source_zone=dict(type='str', required=True),
                    source_ip=dict(type='str', required=True),
                    source_user=dict(type='str'),
                    destination_zone=dict(type='str', required=True),
                    destination_ip=dict(type='str', required=True),
                    destination_port=dict(type='str', required=True),
                    protocol=dict(type='str', choices=['tcp', 'udp', 'icmp'], required=True),
                    application=dict(type='str'),
                    category=dict(type='str'),
                    show_all=dict(type='bool')
                )
            ),
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
        ('type', 'rule_type'),
        ('tag', 'tag_name'),
        ('group', 'group_profile'),
        ('virus', 'antivirus'),
    )

    names = module.params['names']
    details = module.params['details']

    if module.params.get('all_details'):
        module.deprecate(
            'Please use details instead of all_details.',
            version='3.0.0', collection_name='paloaltonetworks.panos'
        )

    if module.params['rule_name']:
        module.deprecate(
            'Please use the names parameter instead of rule_name.',
            version='3.0.0', collection_name='paloaltonetworks.panos'
        )

        names = [module.params['rule_name']]

    if module.params['match_rules']:
        names = match_rules(module, parent.nearest_pandevice())

    if names is None and details is False:
        # Didn't specify specific rules, so just return list of rule names.
        listing = SecurityRule.refreshall(parent, name_only=True)
        module.exit_json(changed=False, rule_names=[r.name for r in listing])

    elif module.params['match_rules'] and details is False:
        # match_rules was set, but not details, so return list of rule names.
        module.exit_json(changed=False, rule_names=names)

    else:
        # Return full policy details.  Will return full policy details even if
        # details is False if specific rules are given, because returning the
        # user's list of rules back to them is pointless.
        if names is None:
            listing = SecurityRule.refreshall(parent)
            rules = [rule.about() for rule in listing]
        else:
            rules = []
            for name in names:
                rule = SecurityRule(name)
                parent.add(rule)

                try:
                    rule.refresh()
                except PanDeviceError as e:
                    module.fail_json(msg='Failed refresh: {0}'.format(e))

                rules.append(rule.about())

        # Fix up names in returned dict.
        for rule in rules:
            for p, a in renames:
                rule[a] = rule[p]
                del rule[p]

        module.exit_json(changed=False, rule_details=rules)


if __name__ == '__main__':
    main()
