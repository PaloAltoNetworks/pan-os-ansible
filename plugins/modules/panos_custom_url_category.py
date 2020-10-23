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
module: panos_custom_url_category
short_description: Create custom url category objects on PAN-OS devices.
description:
    - Create custom url category objects on PAN-OS devices.
author: "Borislav Varadinov (@bvaradinov-c)"
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
    url_value:
        description:
            - List with urls
        type: list
        elements: str
    type:
        description:
            - Custom category type (currently unused)
        type: str
        choices: ['URL List', 'Category Match']
        default: 'URL List'
'''

EXAMPLES = '''
- name: Create Custom Url Category 'Internet Access List'
  panos_custom_url_category:
    provider: '{{ provider }}'
    name: 'Internet Access List'
    url_value:
        - microsoft.com
        - redhat.com

- name: Remove Custom Url Category 'Internet Access List'
  panos_tag_object:
    provider: '{{ provider }}'
    name: 'Internet Access List'
    state: 'absent'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from panos.objects import CustomUrlCategory
    from panos.errors import PanDeviceError
except ImportError:
    try:
        from pandevice.objects import CustomUrlCategory
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
            url_value=dict(type='list', elements='str'),
            type=dict(type='str', choices=['URL List', 'Category Match'], default="URL List")
        )
    )

    required_if = [
        ["state", "present", ["url_value"]]
    ]

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        required_one_of=helper.required_one_of,
        required_if=required_if,
        supports_check_mode=True
    )

    parent = helper.get_pandevice_parent(module)
    device = parent.nearest_pandevice()

    spec = {
        'name': module.params['name'],
        'url_value': module.params['url_value'],
    }

    if device.get_device_version() >= (9, 0, 0):
        spec.update({'type': module.params['type']})

    try:
        listing = CustomUrlCategory.refreshall(parent, add=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    obj = CustomUrlCategory(**spec)
    parent.add(obj)

    changed, diff = helper.apply_state(obj, listing, module)
    module.exit_json(changed=changed, diff=diff)


if __name__ == '__main__':
    main()
