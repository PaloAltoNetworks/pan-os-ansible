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
module: panos_commit
short_description: Commit a PAN-OS device's candidate configuration.
description:
    - Module that will commit the candidate configuration of a PAN-OS device.
    - The new configuration will become active immediately.
author:
    - Michael Richardson (@mrichardson03)
    - Garfield Lee Freeman (@shinmog)
version_added: '1.0.0'
deprecated:
    alternative: 'Use M(panos_commit_firewall), M(panos_commit_panorama), M(panos_commit_push) instead.'
    removed_in: '3.0.0'
    why: 'This module is a subset of functionality found in other modules.'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.device_group
options:
    include_template:
        description:
            - (Panorama only) Include template changes with the commit.
        type: bool
    devicegroup:
        description:
            - B(Deprecated)
            - Use I(device_group) instead.
            - HORIZONTALLINE
            - (Panorama only) The device group.
        type: str
    admins:
        description:
            - (PanOS 8.0+ only) Commit only the changes made by specified list of administrators.
        type: list
        elements: str
'''

EXAMPLES = '''
- name: commit candidate config on firewall
  panos_commit:
    provider: '{{ provider }}'

- name: commit candidate config on Panorama
  panos_commit:
    provider: '{{ provider }}'
    device_group: 'Cloud-Edge'

- name: commit changes by specified admins to firewall
  panos_commit:
    provider: '{{ provider }}'
    admins: ['admin1','admin2']
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection


def main():
    helper = get_connection(
        device_group=True,
        with_classic_provider_spec=True,
        min_pandevice_version=(0, 12, 0),
        argument_spec=dict(
            include_template=dict(type='bool'),
            admins=dict(type='list', elements='str'),
            # TODO(gfreeman) - remove in 2.12.
            devicegroup=dict(),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=False,
        required_one_of=helper.required_one_of,
    )

    module.deprecate(
        'This module is deprecated; use panos_commit_firewall, panos_commit_panorama, panos_commit_push',
        version='3.0.0', collection_name='paloaltonetworks.panos'
    )

    changed = False

    # TODO(gfreeman) - remove in 2.12
    if module.params['devicegroup'] is not None:
        module.deprecate(
            'Param "devicegroup" is deprecated; use "device_group"',
            version='3.0.0', collection_name='paloaltonetworks.panos'
        )
        if module.params['device_group'] is not None:
            msg = [
                'Both "devicegroup" and "device_group" specified',
                'please use one or the other.',
            ]
            module.fail_json(msg='; '.join(msg))
        module.params['device_group'] = module.params['devicegroup']

    helper.get_pandevice_parent(module)
    changed = helper.commit(
        module,
        include_template=module.params['include_template'],
        admins=module.params['admins'],
    )

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
