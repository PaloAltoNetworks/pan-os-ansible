#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2019 Palo Alto Networks, Inc
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
module: panos_snmp_profile
short_description: Manage SNMP server profiles.
description:
    - Manages SNMP server profiles.
author: "Garfield Lee Freeman (@shinmog)"
version_added: '1.0.0'
requirements:
    - pan-python
    - pandevice >= 0.11.1
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.vsys_shared
    - paloaltonetworks.panos.fragments.device_group
    - paloaltonetworks.panos.fragments.state
options:
    name:
        description:
            - Name of the profile.
        type: str
        required: true
    version:
        description:
            - SNMP version.
        type: str
        choices:
            - v2c
            - v3
        default: "v2c"
'''

EXAMPLES = '''
# Create snmp profile
- name: Create snmp profile
  panos_snmp_profile:
    provider: '{{ provider }}'
    name: 'my-profile'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from panos.device import SnmpServerProfile
    from panos.errors import PanDeviceError
except ImportError:
    try:
        from pandevice.device import SnmpServerProfile
        from pandevice.errors import PanDeviceError
    except ImportError:
        pass


def main():
    helper = get_connection(
        vsys_shared=True,
        device_group=True,
        with_state=True,
        with_classic_provider_spec=True,
        min_pandevice_version=(0, 11, 1),
        min_panos_version=(7, 1, 0),
        argument_spec=dict(
            name=dict(required=True),
            version=dict(default='v2c', choices=['v2c', 'v3']),
        ),
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # Verify imports, build pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    try:
        listing = SnmpServerProfile.refreshall(parent)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    spec = {
        'name': module.params['name'],
        'version': module.params['version'],
    }
    obj = SnmpServerProfile(**spec)
    parent.add(obj)

    changed, diff = helper.apply_state(obj, listing, module)
    module.exit_json(changed=changed, diff=diff, msg='Done')


if __name__ == '__main__':
    main()
