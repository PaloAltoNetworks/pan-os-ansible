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

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: panos_api_key
short_description: retrieve api_key for username/password combination
description:
    - This module will allow retrieval of the api_key for a given username/password
author:
    - Joshua Colson (@freakinhippie)
    - Garfield Lee Freeman (@shinmog)
version_added: "2.8"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is supported.
    - Checkmode is NOT supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
'''

EXAMPLES = '''
- name: retrieve api_key
  panos_op:
    provider: '{{ provider }}'
  register: auth

- name: show system info
  panos_op:
    ip_address: '{{ ip_address }}'
    api_key: '{{ auth.api_key }}'
    cmd: show system info
'''

RETURN = '''
api_key:
    description: output of the api_key
    returned: success
    type: string
    sample: "LUFRPT14MW5xOEo1R09KVlBZNnpnemh0VHRBOWl6TGM9bXcwM3JHUGVhRlNiY0dCR0srNERUQT09"
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection


def main():
    helper = get_connection(
        with_classic_provider_spec=True,
        argument_spec={},
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=False,
        required_one_of=helper.required_one_of,
    )

    # Verify imports, build pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    # Done.
    if helper.device.parent is not None:
        # Firewall via Panorama connections.
        api_key = helper.device.parent.api_key
    else:
        # Standard.
        api_key = helper.device.api_key

    module.exit_json(changed=False, msg="Done",
                     api_key=api_key)


if __name__ == '__main__':
    main()
