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

DOCUMENTATION = '''
---
module: panos_application_object
short_description: Create application objects on PAN-OS devices.
description:
    - Create application objects on PAN-OS devices.
author: "Michael Richardson (@mrichardson03)"
version_added: '2.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.vsys
    - paloaltonetworks.panos.fragments.device_group
    - paloaltonetworks.panos.fragments.state
options:
    name:
        description:
            - Name of the tag.
        type: str
        required: true
    category:
        description:
            - Application category
        type: str
    subcategory:
        description:
            - Application subcategory
        type: str
    technology:
        description:
            - Application technology
        type: str
    risk:
        description:
            - Risk (1-5) of the application
        type: str
        choices: ['1', '2', '3', '4', '5']
    parent_app:
        description:
            - Parent Application for which this app falls under
        type: str
    timeout:
        description:
            - Default timeout
        type: int
    tcp_timeout:
        description:
            - TCP timeout
        type: int
    udp_timeout:
        description:
            - UDP timeout
        type: int
    tcp_half_closed_timeout:
        description:
            - TCP half closed timeout
        type: int
    tcp_time_wait_timeout:
        description:
            - TCP wait time timeout
        type: int
    evasive_behavior:
        description:
            - Application is actively evasive
        type: bool
    consume_big_bandwidth:
        description:
            - Application uses large bandwidth
        type: bool
    used_by_malware:
        description:
            - Application is used by malware
        type: bool
    able_to_transfer_file:
        description:
            - Application can do file transfers
        type: bool
    has_known_vulnerability:
        description:
            - Application has known vulnerabilities
        type: bool
    tunnel_other_application:
        description:
            - Application can tunnel other applications
        type: bool
    tunnel_applications:
        description:
            - List of tunneled applications
        type: list
        elements: str
    prone_to_misuse:
        description:
            - Application is prone to misuse
        type: bool
    pervasive_use:
        description:
            - Application is used pervasively
        type: bool
    file_type_ident:
        description:
            - Scan for files
        type: bool
    virus_ident:
        description:
            - Scan for viruses
        type: bool
    data_ident:
        description:
            - Scan for data types
        type: bool
    description:
        description:
            - Description of this object
        type: str
    tag:
        description:
            - Administrative tags
        type: list
        elements: str
'''

EXAMPLES = '''
- name: Create custom application
  panos_application_object:
    provider: '{{ provider }}'
    name: 'custom-app'
    category: 'business-systems'
    subcategory: 'auth-service'
    technology: 'client-server'
    risk: '1'

- name: Remove custom application
  panos_application_object:
    provider: '{{ provider }}'
    name: 'custom-app'
    state: 'absent'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from panos.objects import ApplicationObject
    from panos.errors import PanDeviceError
except ImportError:
    try:
        from pandevice.objects import ApplicationObject
        from pandevice.errors import PanDeviceError
    except ImportError:
        pass


def main():
    helper = get_connection(
        vsys=True,
        device_group=True,
        with_classic_provider_spec=True,
        with_state=True,
        argument_spec=dict(
            name=dict(type='str', required=True),
            category=dict(type='str'),
            subcategory=dict(type='str'),
            technology=dict(type='str'),
            risk=dict(choices=['1', '2', '3', '4', '5']),
            parent_app=dict(type='str'),
            timeout=dict(type='int'),
            tcp_timeout=dict(type='int'),
            udp_timeout=dict(type='int'),
            tcp_half_closed_timeout=dict(type='int'),
            tcp_time_wait_timeout=dict(type='int'),
            evasive_behavior=dict(type='bool'),
            consume_big_bandwidth=dict(type='bool'),
            used_by_malware=dict(type='bool'),
            able_to_transfer_file=dict(type='bool'),
            has_known_vulnerability=dict(type='bool'),
            tunnel_other_application=dict(type='bool'),
            tunnel_applications=dict(type='list', elements='str'),
            prone_to_misuse=dict(type='bool'),
            pervasive_use=dict(type='bool'),
            file_type_ident=dict(type='bool'),
            virus_ident=dict(type='bool'),
            data_ident=dict(type='bool'),
            description=dict(type='str'),
            tag=dict(type='list', elements='str'),
        )
    )

    required_if = [
        ["state", "present", ["category", "subcategory", "technology"]]
    ]

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        required_one_of=helper.required_one_of,
        required_if=required_if,
        supports_check_mode=True
    )

    parent = helper.get_pandevice_parent(module)

    spec = {
        'name': module.params['name'],
        'category': module.params['category'],
        'subcategory': module.params['subcategory'],
        'technology': module.params['technology'],
        'risk': module.params['risk'],
        'parent_app': module.params['parent_app'],
        'timeout': module.params['timeout'],
        'tcp_timeout': module.params['tcp_timeout'],
        'udp_timeout': module.params['udp_timeout'],
        'tcp_half_closed_timeout': module.params['tcp_half_closed_timeout'],
        'tcp_time_wait_timeout': module.params['tcp_time_wait_timeout'],
        'evasive_behavior': module.params['evasive_behavior'],
        'consume_big_bandwidth': module.params['consume_big_bandwidth'],
        'used_by_malware': module.params['used_by_malware'],
        'able_to_transfer_file': module.params['able_to_transfer_file'],
        'has_known_vulnerability': module.params['has_known_vulnerability'],
        'tunnel_other_application': module.params['tunnel_other_application'],
        'tunnel_applications': module.params['tunnel_applications'],
        'prone_to_misuse': module.params['prone_to_misuse'],
        'pervasive_use': module.params['pervasive_use'],
        'file_type_ident': module.params['file_type_ident'],
        'virus_ident': module.params['virus_ident'],
        'data_ident': module.params['data_ident'],
        'description': module.params['description'],
        'tag': module.params['tag'],
    }

    try:
        listing = ApplicationObject.refreshall(parent, add=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    obj = ApplicationObject(**spec)
    parent.add(obj)

    changed, diff = helper.apply_state(obj, listing, module)
    module.exit_json(changed=changed, diff=diff)


if __name__ == '__main__':
    main()
