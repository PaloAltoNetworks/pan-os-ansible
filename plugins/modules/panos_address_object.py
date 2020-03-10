#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright 2018 Palo Alto Networks, Inc
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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: panos_address_object
short_description: Create address objects on PAN-OS devices.
description:
    - Create address objects on PAN-OS devices.
author:
    - Michael Richardson (@mrichardson03)
    - Garfield Lee Freeman (@shinmog)
version_added: "2.8"
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
            - Name of object to create.
        required: true
    value:
        description:
            - IP address, IP range, or FQDN for the object.  Must specify if state is I(present).
        required: true
    address_type:
        description:
            - Type of address object.
        choices: ['ip-netmask', 'ip-range', 'fqdn']
        default: 'ip-netmask'
    description:
        description:
            - Descriptive name for this address object.
    tag:
        description:
            - List of tags to add to this address object.
        type: list
    commit:
        description:
            - Commit changes after creating object.  If I(ip_address) is a Panorama device, and I(device_group) is
              also set, perform a commit to Panorama and a commit-all to the device group.
        required: false
        type: bool
        default: true
'''

EXAMPLES = '''
- name: Create object 'Test-One'
  panos_address_object:
    provider: '{{ provider }}'
    name: 'Test-One'
    value: '1.1.1.1'
    description: 'Description One'
    tag: ['Prod']

- name: Create object 'Test-Two'
  panos_address_object:
    provider: '{{ provider }}'
    name: 'Test-Two'
    address_type: 'ip-range'
    value: '1.1.1.1-2.2.2.2'
    description: 'Description Two'
    tag: ['SI']

- name: Create object 'Test-Three'
  panos_address_object:
    provider: '{{ provider }}'
    name: 'Test-Three'
    address_type: 'fqdn'
    value: 'foo.bar.baz'
    description: 'Description Three'

- name: Delete object 'Test-Two'
  panos_address_object:
    provider: '{{ provider }}'
    name: 'Test-Two'
    state: 'absent'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from pandevice.objects import AddressObject
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
            name=dict(required=True),
            value=dict(),
            address_type=dict(default='ip-netmask', choices=['ip-netmask', 'ip-range', 'fqdn']),
            description=dict(),
            tag=dict(type='list'),
            commit=dict(type='bool', default=True),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        required_one_of=helper.required_one_of,
        supports_check_mode=True,
    )

    # Verify libs are present, get parent object.
    parent = helper.get_pandevice_parent(module)

    # Object params.
    spec = {
        'name': module.params['name'],
        'value': module.params['value'],
        'type': module.params['address_type'],
        'description': module.params['description'],
        'tag': module.params['tag'],
    }

    # Other info.
    commit = module.params['commit']

    # Retrieve current info.
    try:
        listing = AddressObject.refreshall(parent, add=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    # Build the object based on the user spec.
    obj = AddressObject(**spec)
    parent.add(obj)

    # Apply the state.
    changed, diff = helper.apply_state(obj, listing, module)

    # Commit.
    if commit and changed:
        helper.commit(module)

    # Done.
    module.exit_json(changed=changed, diff=diff)


if __name__ == '__main__':
    main()
