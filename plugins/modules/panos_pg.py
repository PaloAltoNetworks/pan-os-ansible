#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright 2016 Palo Alto Networks, Inc
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

DOCUMENTATION = '''
---
module: panos_pg
short_description: create a security profiles group
description:
    - Create a security profile group
author: "Luigi Mori (@jtschichold), Ivan Bojer (@ivanbojer)"
version_added: "2.3"
requirements:
    - pan-python
    - pandevice
notes:
    - Panorama is supported.
    - Checkmode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.vsys
    - paloaltonetworks.panos.fragments.device_group
    - paloaltonetworks.panos.fragments.state
options:
    pg_name:
        description:
            - name of the security profile group
        required: true
    data_filtering:
        description:
            - name of the data filtering profile
    file_blocking:
        description:
            - name of the file blocking profile
    spyware:
        description:
            - name of the spyware profile
    url_filtering:
        description:
            - name of the url filtering profile
    virus:
        description:
            - name of the anti-virus profile
    vulnerability:
        description:
            - name of the vulnerability profile
    wildfire:
        description:
            - name of the wildfire analysis profile
    commit:
        description:
            - commit if changed
        default: True
        type: bool
'''

EXAMPLES = '''
- name: setup security profile group
  panos_pg:
    provider: '{{ provider }}'
    pg_name: "pg-default"
    virus: "default"
    spyware: "default"
    vulnerability: "default"
'''

RETURN = '''
# Default return values
'''

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection


try:
    from pandevice.errors import PanDeviceError
    from pandevice.objects import SecurityProfileGroup
except ImportError:
    pass


def main():
    helper = get_connection(
        vsys=True,
        device_group=True,
        with_state=True,
        with_classic_provider_spec=True,
        argument_spec=dict(
            pg_name=dict(required=True),
            data_filtering=dict(),
            file_blocking=dict(),
            spyware=dict(),
            url_filtering=dict(),
            virus=dict(),
            vulnerability=dict(),
            wildfire=dict(),
            commit=dict(type='bool', default=True)
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # Verify libs are present, build the pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    # Other info.
    commit = module.params['commit']

    # Retrieve current profiles.
    try:
        listing = SecurityProfileGroup.refreshall(parent, add=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    spec = {
        'name': module.params['pg_name'],
        'virus': module.params['virus'],
        'spyware': module.params['spyware'],
        'vulnerability': module.params['vulnerability'],
        'url_filtering': module.params['url_filtering'],
        'file_blocking': module.params['file_blocking'],
        'data_filtering': module.params['data_filtering'],
        'wildfire_analysis': module.params['wildfire'],
    }
    obj = SecurityProfileGroup(**spec)
    parent.add(obj)

    # Apply the state.
    changed, diff = helper.apply_state(obj, listing, module)

    # Optional commit.
    if changed and commit:
        helper.commit(module)

    module.exit_json(changed=changed, diff=diff, msg='done')


if __name__ == '__main__':
    main()
