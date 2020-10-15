#!/usr/bin/python
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

DOCUMENTATION = '''
---
module: panos_address_group
short_description: Create address group objects on PAN-OS devices.
description:
    - Create address group objects on PAN-OS devices.
author:
    - Michael Richardson (@mrichardson03)
    - Garfield Lee Freeman (@shinmog)
version_added: '1.0.0'
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
    - paloaltonetworks.panos.fragments.deprecated_commit
options:
    name:
        description:
            - Name of address group to create.
        required: true
        type: str
    static_value:
        description:
            - List of address objects to be included in the group.
        type: list
        elements: str
    dynamic_value:
        description:
            - Registered IP tags for a dynamic address group.
        type: str
    description:
        description:
            - Descriptive name for this address group.
        type: str
    tag:
        description:
            - List of tags to add to this address group.
        type: list
        elements: str
'''

EXAMPLES = '''
- name: Create object group 'Prod'
  panos_address_group:
    provider: '{{ provider }}'
    name: 'Prod'
    static_value: ['Test-One', 'Test-Three']
    tag: ['Prod']

- name: Create object group 'SI'
  panos_address_group:
    provider: '{{ provider }}'
    name: 'SI'
    dynamic_value: "'SI_Instances'"
    tag: ['SI']

- name: Delete object group 'SI'
  panos_address_group:
    provider: '{{ provider }}'
    name: 'SI'
    state: 'absent'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from panos.objects import AddressGroup
    from panos.errors import PanDeviceError
except ImportError:
    try:
        from pandevice.objects import AddressGroup
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
            static_value=dict(type='list', elements='str'),
            dynamic_value=dict(),
            description=dict(),
            tag=dict(type='list', elements='str'),
            commit=dict(type='bool', default=False),
        ),
    )
    mutually_exclusive = [
        ['static_value', 'dynamic_value']
    ]

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        required_one_of=helper.required_one_of,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )

    # Verify libs are present, get parent object.
    parent = helper.get_pandevice_parent(module)

    if module.params['state'] == 'present':
        if (module.params['static_value'] is None and
                module.params['dynamic_value'] is None):
            module.fail_json(
                msg="One of 'static_value' or 'dynamic_value' is required when "
                "state' is 'present'"
            )

    # Object params.
    spec = {
        'name': module.params['name'],
        'static_value': module.params['static_value'],
        'dynamic_value': module.params['dynamic_value'],
        'description': module.params['description'],
        'tag': module.params['tag'],
    }

    # Other info.
    commit = module.params['commit']

    # Retrieve current info.
    try:
        listing = AddressGroup.refreshall(parent, add=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    # Build the object based on the user spec.
    obj = AddressGroup(**spec)
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
