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

DOCUMENTATION = '''
---
module: panos_security_rule
short_description: Create security rule policy on PAN-OS devices or Panorama management console.
description:
    - Security policies allow you to enforce rules and take action, and can be as general or specific as needed.
    - The policy rules are compared against the incoming traffic in sequence, and because the first rule that matches
    - the traffic is applied, the more specific rules must precede the more general ones.
author:
    - Ivan Bojer (@ivanbojer)
    - Robert Hagen (@stealthllama)
    - Michael Richardson (@mrichardson03)
    - Garfield Lee Freeman (@shinmog)
version_added: '1.0.0'
requirements:
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
    rule_name:
        description:
            - Name of the security rule.
        type: str
        required: true
    source_zone:
        description:
            - List of source zones.
        default: ["any"]
        type: list
        elements: str
    source_ip:
        description:
            - List of source addresses.
        default: ["any"]
        type: list
        elements: str
    source_user:
        description:
            - Use users to enforce policy for individual users or a group of users.
        default: ["any"]
        type: list
        elements: str
    hip_profiles:
        description: >
            - If you are using GlobalProtect with host information profile (HIP) enabled, you can also base the policy
            on information collected by GlobalProtect. For example, the user access level can be determined HIP that
            notifies the firewall about the user's local configuration.
        default: ["any"]
        type: list
        elements: str
    destination_zone:
        description:
            - List of destination zones.
        default: ["any"]
        type: list
        elements: str
    destination_ip:
        description:
            - List of destination addresses.
        default: ["any"]
        type: list
        elements: str
    application:
        description:
            - List of applications, application groups, and/or application filters.
        default: ["any"]
        type: list
        elements: str
    service:
        description:
            - List of services and/or service groups.
        default: ['application-default']
        type: list
        elements: str
    category:
        description:
            - List of destination URL categories.
        default: ["any"]
        type: list
        elements: str
    action:
        description:
            - Action to apply once rules matches.
        type: str
        choices:
            - allow
            - deny
            - drop
            - reset-client
            - reset-server
            - reset-both
        default: "allow"
    log_setting:
        description:
            - Log forwarding profile.
        type: str
    log_start:
        description:
            - Whether to log at session start.
        default: false
        type: bool
    log_end:
        description:
            - Whether to log at session end.
        default: true
        type: bool
    description:
        description:
            - Description of the security rule.
        type: str
    rule_type:
        description:
            - Type of security rule (version 6.1 of PanOS and above).
        type: str
        choices:
            - universal
            - intrazone
            - interzone
        default: 'universal'
    tag_name:
        description:
            - List of tags associated with the rule.
        type: list
        elements: str
    negate_source:
        description:
            - Match on the reverse of the 'source_ip' attribute
        default: false
        type: bool
    negate_destination:
        description:
            - Match on the reverse of the 'destination_ip' attribute
        default: false
        type: bool
    disabled:
        description:
            - Disable this rule.
        default: false
        type: bool
    schedule:
        description:
            - Schedule in which this rule is active.
        type: str
    icmp_unreachable:
        description:
            - Send 'ICMP Unreachable'. Used with 'deny', 'drop', and 'reset' actions.
        type: bool
    disable_server_response_inspection:
        description:
            - Disables packet inspection from the server to the client. Useful under heavy server load conditions.
        default: false
        type: bool
    group_profile:
        description: >
            - Security profile group that is already defined in the system. This property supersedes antivirus,
            vulnerability, spyware, url_filtering, file_blocking, data_filtering, and wildfire_analysis properties.
        type: str
    antivirus:
        description:
            - Name of the already defined antivirus profile.
        type: str
    vulnerability:
        description:
            - Name of the already defined vulnerability profile.
        type: str
    spyware:
        description:
            - Name of the already defined spyware profile.
        type: str
    url_filtering:
        description:
            - Name of the already defined url_filtering profile.
        type: str
    file_blocking:
        description:
            - Name of the already defined file_blocking profile.
        type: str
    data_filtering:
        description:
            - Name of the already defined data_filtering profile.
        type: str
    wildfire_analysis:
        description:
            - Name of the already defined wildfire_analysis profile.
        type: str
    location:
        description:
            - Position to place the created rule in the rule base.  Supported values are
              I(top)/I(bottom)/I(before)/I(after).
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
    devicegroup:
        description:
            - B(Deprecated)
            - Use I(device_group) instead.
            - HORIZONTALLINE
            - Device groups are logical groups of firewalls in Panorama.
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
'''

EXAMPLES = '''
- name: add SSH inbound rule to Panorama device group
  panos_security_rule:
    provider: '{{ provider }}'
    device_group: 'Cloud Edge'
    rule_name: 'SSH permit'
    description: 'SSH rule test'
    tag_name: ['production']
    source_zone: ['public']
    source_ip: ['any']
    destination_zone: ['private']
    destination_ip: ['1.1.1.1']
    application: ['ssh']
    action: 'allow'

- name: add a rule to allow HTTP multimedia only to CDNs
  panos_security_rule:
    provider: '{{ provider }}'
    rule_name: 'HTTP Multimedia'
    description: 'Allow HTTP multimedia only to host at 1.1.1.1'
    source_zone: ['private']
    destination_zone: ['public']
    category: ['content-delivery-networks']
    application: ['http-video', 'http-audio']
    service: ['service-http', 'service-https']
    action: 'allow'

- name: add a more complex rule that uses security profiles
  panos_security_rule:
    provider: '{{ provider }}'
    rule_name: 'Allow HTTP'
    source_zone: ['public']
    destination_zone: ['private']
    log_start: false
    log_end: true
    action: 'allow'
    antivirus: 'strict'
    vulnerability: 'strict'
    spyware: 'strict'
    url_filtering: 'strict'
    wildfire_analysis: 'default'

- name: disable a Panorama pre-rule
  panos_security_rule:
    provider: '{{ provider }}'
    device_group: 'Production edge'
    rule_name: 'Allow telnet'
    source_zone: ['public']
    destination_zone: ['private']
    source_ip: ['any']
    destination_ip: ['1.1.1.1']
    log_start: false
    log_end: true
    action: 'allow'
    disabled: true

- name: delete a device group security rule
  panos_security_rule:
    provider: '{{ provider }}'
    state: 'absent'
    device_group: 'DC Firewalls'
    rule_name: 'Allow telnet'

- name: add a rule at a specific location in the rulebase
  panos_security_rule:
    provider: '{{ provider }}'
    rule_name: 'SSH permit'
    description: 'SSH rule test'
    source_zone: ['untrust']
    destination_zone: ['trust']
    source_ip: ['any']
    source_user: ['any']
    destination_ip: ['1.1.1.1']
    category: ['any']
    application: ['ssh']
    service: ['application-default']
    action: 'allow'
    location: 'before'
    existing_rule: 'Allow MySQL'
'''

RETURN = '''
# Default return values
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


ACCEPTABLE_MOVE_ERRORS = (
    'already at the top',
    'already at the bottom',
)


def main():
    helper = get_connection(
        vsys=True,
        device_group=True,
        rulebase=True,
        with_state=True,
        with_classic_provider_spec=True,
        error_on_firewall_shared=True,
        argument_spec=dict(
            rule_name=dict(required=True),
            source_zone=dict(type='list', elements='str', default=['any']),
            source_ip=dict(type='list', elements='str', default=["any"]),
            source_user=dict(type='list', elements='str', default=['any']),
            hip_profiles=dict(type='list', elements='str', default=['any']),
            destination_zone=dict(type='list', elements='str', default=['any']),
            destination_ip=dict(type='list', elements='str', default=["any"]),
            application=dict(type='list', elements='str', default=['any']),
            service=dict(type='list', elements='str', default=['application-default']),
            category=dict(type='list', elements='str', default=['any']),
            action=dict(
                default='allow',
                choices=['allow', 'deny', 'drop', 'reset-client', 'reset-server', 'reset-both'],
            ),
            log_setting=dict(),
            log_start=dict(type='bool', default=False),
            log_end=dict(type='bool', default=True),
            description=dict(),
            rule_type=dict(default='universal', choices=['universal', 'intrazone', 'interzone']),
            tag_name=dict(type='list', elements='str'),
            negate_source=dict(type='bool', default=False),
            negate_destination=dict(type='bool', default=False),
            disabled=dict(type='bool', default=False),
            schedule=dict(),
            icmp_unreachable=dict(type='bool'),
            disable_server_response_inspection=dict(type='bool', default=False),
            group_profile=dict(),
            antivirus=dict(),
            spyware=dict(),
            vulnerability=dict(),
            url_filtering=dict(),
            file_blocking=dict(),
            wildfire_analysis=dict(),
            data_filtering=dict(),
            target=dict(type='list', elements='str'),
            negate_target=dict(type='bool'),
            location=dict(choices=['top', 'bottom', 'before', 'after']),
            existing_rule=dict(),
            commit=dict(type='bool', default=False),

            # TODO(gfreeman) - remove this in the next role release.
            devicegroup=dict(),
        ),
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # TODO(gfreeman) - remove when devicegroup is removed.
    if module.params['devicegroup'] is not None:
        module.deprecate(
            'Param "devicegroup" is deprecated; use "device_group"',
            version='3.0.0', collection_name='paloaltonetworks.panos'
        )
        if module.params['device_group'] is not None:
            msg = [
                'Both "devicegroup" and "device_group" are specified',
                'Specify one or the other, not both.',
            ]
            module.fail_json(msg='. '.join(msg))
        module.params['device_group'] = module.params['devicegroup']

    # Verify imports, build pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    # Set the SecurityRule object params.
    rule_spec = {
        'name': module.params['rule_name'],
        'fromzone': module.params['source_zone'],
        'tozone': module.params['destination_zone'],
        'source': module.params['source_ip'],
        'source_user': module.params['source_user'],
        'hip_profiles': module.params['hip_profiles'],
        'destination': module.params['destination_ip'],
        'application': module.params['application'],
        'service': module.params['service'],
        'category': module.params['category'],
        'action': module.params['action'],
        'log_setting': module.params['log_setting'],
        'log_start': module.params['log_start'],
        'log_end': module.params['log_end'],
        'description': module.params['description'],
        'type': module.params['rule_type'],
        'tag': module.params['tag_name'],
        'negate_source': module.params['negate_source'],
        'negate_destination': module.params['negate_destination'],
        'disabled': module.params['disabled'],
        'schedule': module.params['schedule'],
        'icmp_unreachable': module.params['icmp_unreachable'],
        'disable_server_response_inspection': module.params['disable_server_response_inspection'],
        'group': module.params['group_profile'],
        'virus': module.params['antivirus'],
        'spyware': module.params['spyware'],
        'vulnerability': module.params['vulnerability'],
        'url_filtering': module.params['url_filtering'],
        'file_blocking': module.params['file_blocking'],
        'wildfire_analysis': module.params['wildfire_analysis'],
        'data_filtering': module.params['data_filtering'],
        'target': module.params['target'],
        'negate_target': module.params['negate_target'],
    }

    # Other module info.
    location = module.params['location']
    existing_rule = module.params['existing_rule']
    commit = module.params['commit']

    # Retrieve the current rules.
    try:
        rules = SecurityRule.refreshall(parent, add=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    # Create new rule object from the params.
    new_rule = SecurityRule(**rule_spec)
    parent.add(new_rule)

    # Which action shall we take on the rule object?
    changed, diff = helper.apply_state(new_rule, rules, module)

    # Move the rule to the correct spot, if applicable.
    if module.params['state'] == 'present':
        changed |= helper.apply_position(new_rule, location, existing_rule, module)

    # Optional commit.
    if changed and commit:
        helper.commit(module)

    # Done.
    module.exit_json(changed=changed, diff=diff, msg='Done')


if __name__ == '__main__':
    main()
