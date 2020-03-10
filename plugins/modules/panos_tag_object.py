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
module: panos_tag_object
short_description: Create tag objects on PAN-OS devices.
description:
    - Create tag objects on PAN-OS devices.
author: "Michael Richardson (@mrichardson03)"
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
            - Name of the tag.
        required: true
    color:
        description:
            - Color for the tag.
        choices: ['red', 'green', 'blue', 'yellow', 'copper', 'orange', 'purple', 'gray',
                  'light green', 'cyan', 'light gray', 'blue gray', 'lime', 'black', 'gold',
                  'brown']
    comments:
        description:
            - Comments for the tag.
    commit:
        description:
            - Commit changes after creating object.  If I(ip_address) is a Panorama device, and I(device_group) is
              also set, perform a commit to Panorama and a commit-all to the device group.
        required: false
        type: bool
        default: true
'''

EXAMPLES = '''
- name: Create tag object 'Prod'
  panos_tag_object:
    provider: '{{ provider }}'
    name: 'Prod'
    color: 'red'
    comments: 'Prod Environment'

- name: Remove tag object 'Prod'
  panos_tag_object:
    provider: '{{ provider }}'
    name: 'Prod'
    state: 'absent'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from pandevice.objects import Tag
    from pandevice.errors import PanDeviceError
except ImportError:
    pass

COLOR_NAMES = [
    'red', 'green', 'blue', 'yellow', 'copper', 'orange', 'purple', 'gray', 'light green',
    'cyan', 'light gray', 'blue gray', 'lime', 'black', 'gold', 'brown'
]


def main():
    helper = get_connection(
        vsys=True,
        device_group=True,
        with_classic_provider_spec=True,
        with_state=True,
        argument_spec=dict(
            name=dict(type='str', required=True),
            color=dict(type='str', choices=COLOR_NAMES),
            comments=dict(type='str'),
            commit=dict(type='bool', default=True)
        )
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        required_one_of=helper.required_one_of,
        supports_check_mode=True
    )

    parent = helper.get_pandevice_parent(module)

    spec = {
        'name': module.params['name'],
        'color': Tag.color_code(module.params['color']),
        'comments': module.params['comments']
    }

    commit = module.params['commit']

    try:
        listing = Tag.refreshall(parent, add=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    obj = Tag(**spec)
    parent.add(obj)

    changed, diff = helper.apply_state(obj, listing, module)

    if commit and changed:
        helper.commit(module)

    module.exit_json(changed=changed, diff=diff)


if __name__ == '__main__':
    main()
