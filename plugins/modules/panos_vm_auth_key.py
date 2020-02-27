#!/usr/bin/env python
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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: panos_vm_auth_key
short_description: Create a VM auth key for VM-Series bootstrapping
description:
    - This module will ask Panorama to create a VM auth key for VM-Series bootstrapping.
author:
    - Garfield Lee Freeman (@shinmog)
version_added: "2.9"
requirements:
    - pan-python
    - pandevice
notes:
    - Checkmode is NOT supported.
    - Panorama is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
options:
    hours:
        description:
            - The number of hours the VM auth key should be valid for.
        default: 24
        type: int
'''

EXAMPLES = '''
- name: Create an 8 hour VM auth key
  panos_vm_auth_key:
    provider: '{{ provider }}'
    hours: 8
  register: res

- debug:
    msg: 'Auth key {{ res.authkey }} expires at {{ res.expires }}'
'''

RETURN = '''
authkey:
    description: The VM auth key.
    returned: success
    type: string
expires:
    description: Auth key expiration date
    returned: success
    type: string
    sample: "2020/02/14 01:02:03"
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection


try:
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def main():
    helper = get_connection(
        with_classic_provider_spec=True,
        firewall_error='This is a Panorama only module',
        min_pandevice_version=(0, 14, 0),
        argument_spec=dict(
            hours=dict(default=24, type='int'),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=False,
        required_one_of=helper.required_one_of,
    )

    # Verify libs are present, get the parent object.
    parent = helper.get_pandevice_parent(module)

    # Create the VM auth key.
    result = {}
    try:
        result = helper.device.generate_vm_auth_key(module.params['hours'])
    except PanDeviceError as e:
        module.fail_json(msg='Failed to generate VM auth key: {0}'.format(e))

    # Done.
    module.exit_json(changed=True, **result)


if __name__ == '__main__':
    main()
