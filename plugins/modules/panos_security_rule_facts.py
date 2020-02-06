#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: panos_security_rule_facts
short_description: Get information about a security rule.
description:
    - Get information about a single security rule or the names of all security rules.
author: "Garfield Lee Freeman (@shinmog)"
version_added: "2.8"
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
    all_details:
        description:
            - Get full-policy details when name is not set.
        type: bool
'''

EXAMPLES = '''
- name: Get a list of all security rules
  panos_security_rule_facts:
    provider: '{{ provider }}'
  register: sec_rules

- debug:
    msg: '{{ sec_rules.rules }}'

- name: Get the definition for rule 'HTTP Multimedia'
  panos_security_rule_facts:
    provider: '{{ provider }}'
    rule_name: 'HTTP Multimedia'
  register: rule1

- debug:
    msg: '{{ rule1.spec }}'
'''

RETURN = '''
rules:
    description: List of security rules present
    returned: When I(rule_name) is not specified and I(all_details) is False
    type: list
    sample: ['rule1', 'rule2', 'rule3']
policy:
    description: List of security rules present with details
    returned: When I(rule_name) is not specified and I(all_details) is True
    type: complex
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
spec:
    description: The security rule definition
    returned: When I(rule_name) is specified
    type: complex
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
    from pandevice.policies import SecurityRule
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
        argument_spec=dict(
            rule_name=dict(),
            all_details=dict(default=False, type='bool'),
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

    name = module.params['rule_name']
    all_details = module.params['all_details']
    if all_details and name is None:
        try:
            listing = SecurityRule.refreshall(parent)
        except PanDeviceError as e:
            module.fail_json(msg='Failed refreshall: {0}'.format(e))
        rules = [rule.about() for rule in listing]
        for rule in rules:
            for pandevice_param, ansible_param in renames:
                rule[ansible_param] = rule[pandevice_param]
                del rule[pandevice_param]

        module.exit_json(
            changed=False,
            policy=rules,
        )
    elif name is None:
        try:
            listing = SecurityRule.refreshall(parent, name_only=True)
        except PanDeviceError as e:
            module.fail_json(msg='Failed refreshall: {0}'.format(e))
        module.exit_json(changed=False, rules=[x.name for x in listing])

    rule = SecurityRule(name)
    parent.add(rule)
    try:
        rule.refresh()
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh for "{0}": {1}'.format(name, e))

    spec = rule.about()

    for pandevice_param, ansible_param in renames:
        spec[ansible_param] = spec[pandevice_param]
        del(spec[pandevice_param])

    module.exit_json(changed=False, spec=spec)


if __name__ == '__main__':
    main()
