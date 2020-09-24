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
module: panos_match_rule
short_description: Test for match against a security rule on PAN-OS devices or Panorama management console.
description:
    - Security policies allow you to enforce rules and take action, and can be as general or specific as needed.
author: "Robert Hagen (@stealthllama)"
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
    - xmltodict
notes:
    - Checkmode is not supported.
    - Panorama NOT is supported.  However, specifying Panorama I(provider) info with a target serial number is.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.vsys
options:
    rule_type:
        description:
            - Type of rule.
        type: str
        choices:
            - security
            - nat
        default: "security"
    source_zone:
        description:
            - The source zone.
        type: str
    source_ip:
        description:
            - The source IP address.
        type: str
        required: true
    source_port:
        description:
            - The source port.
        type: int
    source_user:
        description:
            - The source user or group.
        type: str
    to_interface:
        description:
            - The inbound interface in a NAT rule.
        type: str
    destination_zone:
        description:
            - The destination zone.
        type: str
    destination_ip:
        description:
            - The destination IP address.
        type: str
        required: true
    destination_port:
        description:
            - The destination port.
        type: int
        required: true
    application:
        description:
            - The application.
        type: str
    protocol:
        description:
            - The IP protocol number from 1 to 255.
        type: int
        required: true
    category:
        description:
            - URL category
        type: str
    vsys_id:
        description:
            - B(Removed)
            - Use I(vsys) instead.
        type: str
    rulebase:
        description:
            - B(DEPRECATED)
            - This is no longer used and may safely be removed from your playbook.
        type: str
'''

EXAMPLES = '''
- name: check security rules for Google DNS
  panos_match_rule:
    provider: '{{ provider }}'
    source_ip: '10.0.0.0'
    destination_ip: '8.8.8.8'
    application: 'dns'
    destination_port: '53'
    protocol: '17'
  register: result
- debug: msg='{{ result.rule }}'

- name: check security rules inbound SSH with user match
  panos_match_rule:
    provider: '{{ provider }}'
    source_ip: '0.0.0.0'
    source_user: 'mydomain\\jsmith'
    destination_ip: '192.168.100.115'
    destination_port: '22'
    protocol: '6'
  register: result
- debug: msg='{{ result.rule }}'

- name: check NAT rules for source NAT
  panos_match_rule:
    provider: '{{ provider }}'
    rule_type: 'nat'
    source_zone: 'Prod-DMZ'
    source_ip: '10.10.118.50'
    to_interface: 'ethernet1/2'
    destination_zone: 'Internet'
    destination_ip: '0.0.0.0'
    protocol: '6'
  register: result
- debug: msg='{{ result.rule }}'

- name: check NAT rules for inbound web
  panos_match_rule:
    provider: '{{ provider }}'
    rule_type: 'nat'
    source_zone: 'Internet'
    source_ip: '0.0.0.0'
    to_interface: 'ethernet1/1'
    destination_zone: 'Prod DMZ'
    destination_ip: '192.168.118.50'
    destination_port: '80'
    protocol: '6'
  register: result
- debug: msg='{{ result.rule }}'

- name: check security rules for outbound POP3 in vsys4
  panos_match_rule:
    provider: '{{ provider }}'
    vsys_id: 'vsys4'
    source_ip: '10.0.0.0'
    destination_ip: '4.3.2.1'
    application: 'pop3'
    destination_port: '110'
    protocol: '6'
  register: result
- debug: msg='{{ result.rule }}'
'''

RETURN = '''
stdout_lines:
    description: B(DEPRECATED); use "rule" instead
    returned: always
    type: str
rule:
    description: The rule definition, either security rule or NAT rule
    returned: always
    type: dict
rulebase:
    description: Rule location; panorama-pre-rulebase, firewall-rulebase, or panorama-post-rulebase
    returned: always
    type: str
'''

import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from panos.errors import PanDeviceError
    from panos.policies import NatRule
    from panos.policies import SecurityRule
except ImportError:
    try:
        from pandevice.errors import PanDeviceError
        from pandevice.policies import NatRule
        from pandevice.policies import SecurityRule
    except ImportError:
        pass


# TODO(gfreeman) - Remove this dependency in the next role release.
HAS_LIB = True
try:
    import xmltodict
    import xml.etree.ElementTree as ET
except ImportError:
    HAS_LIB = False


def main():
    helper = get_connection(
        vsys=True,
        with_classic_provider_spec=True,
        panorama_error='Panorama is not supported',
        argument_spec=dict(
            rule_type=dict(default='security', choices=['security', 'nat']),
            source_zone=dict(),
            source_ip=dict(required=True),
            source_port=dict(type='int'),
            source_user=dict(),
            to_interface=dict(),
            destination_zone=dict(),
            destination_ip=dict(required=True),
            destination_port=dict(required=True, type='int'),
            application=dict(),
            protocol=dict(required=True, type='int'),
            category=dict(),

            # TODO(gfreeman) - Remove this in the next role release.
            vsys_id=dict(),
            rulebase=dict(),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=False,
        required_one_of=helper.required_one_of,
    )

    # TODO(gfreeman) - Remove this in the next role release.
    if not HAS_LIB:
        module.fail_json(msg='Missing xmltodict library')
    if module.params['vsys_id'] is not None:
        module.fail_json(msg='Param "vsys_id" is removed; use vsys')
    if module.params['rulebase'] is not None:
        module.deprecate(
            'Param "rulebase" is deprecated and may safely be removed from your playbook',
            version='3.0.0',
            collection_name='paloaltonetworks.panos'
        )

    parent = helper.get_pandevice_parent(module)

    params = (
        ('application', 'application', ['security', ]),
        ('category', 'category', ['security', ]),
        ('destination_ip', 'destination', ['security', 'nat']),
        ('destination_port', 'destination-port', ['security', 'nat']),
        ('source_zone', 'from', ['security', 'nat']),
        ('protocol', 'protocol', ['security', 'nat']),
        ('source_ip', 'source', ['security', 'nat']),
        ('source_user', 'source-user', ['security', ]),
        ('destination_zone', 'to', ['security', 'nat']),
        ('to_interface', 'to-interface', ['nat', ]),
    )

    cmd = []
    rtype = module.params['rule_type']
    vsys = module.params['vsys']

    # This module used to refreshall on either the security rules or the NAT
    # rules, however if the rule matched came from Panorama, then this module
    # failed.  To account for this, instead directly query the 3 path locations
    # where the rule could exist, and return that instead.  When pandevice
    # supports querying the firewall for the pushed down Panorama config, change
    # this back to using normal pandevice objects.
    rule_locations = (
        (
            'panorama-pre-rulebase',
            "/config/panorama/vsys/entry[@name='{0}']/pre-rulebase",
        ),
        (
            'firewall-rulebase',
            "/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='{0}']/rulebase",
        ),
        (
            'panorama-post-rulebase',
            "/config/panorama/vsys/entry[@name='{0}']/post-rulebase",
        ),
    )
    suffix = "/{0}/rules/entry[@name='{1}']"

    if rtype == 'security':
        cmd.append('test security-policy-match')
        obj = SecurityRule()
    else:
        cmd.append('test nat-policy-match')
        obj = NatRule()
    parent.add(obj)

    for ansible_param, cmd_param, rule_types in params:
        if rtype not in rule_types or module.params[ansible_param] is None:
            continue
        cmd.append('{0} "{1}"'.format(cmd_param, module.params[ansible_param]))

    # Submit the op command with the appropriate test string
    test_string = ' '.join(cmd)
    try:
        response = helper.device.op(cmd=test_string, vsys=parent.vsys)
    except PanDeviceError as e:
        module.fail_json(msg='Failed "{0}": {1}'.format(test_string, e))

    elm = response.find('./result/rules/entry')
    elm2 = response.find('./result/msg/line')
    if elm is not None:
        try:
            rule_name = elm.attrib['name']
        except KeyError:
            rule_name = elm.text
    elif elm2 is not None:
        '''
        From 8.1 (matching Panorama rule):
        NOTE: Ending newlines have been truncated to appease codestyle rules.

<response cmd="status" status="success"><result><msg><line><![CDATA["Rule Name; index: 1" {
        from L3-trust;
        source [ 10.0.0.1 1.1.1.1 ];
        source-region none;
        to L3-untrust;
        destination [ 8.8.8.8 ];
        destination-region none;
        user any;
        category any;
        application/service [0:any/tcp/any/21 1:any/tcp/any/22 ];
        action allow;
        icmp-unreachable: no
        terminal yes;
}

]]></line></msg></result></response>
        '''
        rule_name = elm2.text.split(';')[0].split('"')[1].strip()
    else:
        msg = 'No matching {0} rule; resp = {1}'.format(
            rtype, ET.tostring(response, enoding='utf-8'),
        )
        module.exit_json(msg=msg)

    '''
    Example response (newlines after newlines to appease pycodestyle line length limitations):

    <response cmd="status" status="success"><result><rules>\n
\t<entry>deny all and log; index: 3</entry>\n
</rules>\n
</result></response>
    '''
    tokens = rule_name.split(';')
    if len(tokens) == 2 and tokens[1].startswith(' index: '):
        rule_name = tokens[0]

    fw = obj.nearest_pandevice()
    for rulebase, prefix in rule_locations:
        xpath = prefix.format(vsys) + suffix.format(rtype, rule_name)
        ans = fw.xapi.get(xpath)
        if ans is None:
            continue
        rules = obj.refreshall_from_xml(ans.find('./result'))
        if rules:
            x = rules[0]
            module.deprecate(
                'The "stdout_lines" output is deprecated; use "rule" instead',
                version='3.0.0',
                collection_name='paloaltonetworks.panos',
            )
            module.exit_json(
                stdout_lines=json.dumps(xmltodict.parse(x.element_str()), indent=2),
                msg='Rule matched',
                rule=x.about(),
                rulebase=rulebase,
            )

    module.fail_json(msg='Matched "{0}" with "{1}", but wasn\'t in any rulebase'.format(rule_name, test_string))


if __name__ == '__main__':
    main()
