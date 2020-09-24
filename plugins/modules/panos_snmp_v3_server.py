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
module: panos_snmp_v3_server
short_description: Manage SNMP v3 servers.
description:
    - Manages SNMP v3 servers.
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
    snmp_profile:
        description:
            - Name of the SNMP server profile.
        type: str
        required: true
    name:
        description:
            - Name of the server.
        type: str
        required: true
    manager:
        description:
            - IP address or FQDN of SNMP manager to use.
        type: str
    user:
        description:
            - User
        type: str
    engine_id:
        description:
            - A hex number
        type: str
    auth_password:
        description:
            - Authentiation protocol password.
        type: str
    priv_password:
        description:
            - Privacy protocol password.
        type: str
'''

EXAMPLES = '''
# Create snmp v3 server
- name: Create snmp v3 server
  panos_snmp_v3_server:
    provider: '{{ provider }}'
    snmp_profile: 'my-profile'
    name: 'my-v3-server'
    manager: '192.168.55.10'
    user: 'jdoe'
    auth_password: 'password'
    priv_password: 'drowssap'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from panos.device import SnmpServerProfile
    from panos.device import SnmpV3Server
    from panos.errors import PanDeviceError
except ImportError:
    try:
        from pandevice.device import SnmpServerProfile
        from pandevice.device import SnmpV3Server
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
            snmp_profile=dict(required=True),
            name=dict(required=True),
            manager=dict(),
            user=dict(),
            engine_id=dict(),
            auth_password=dict(no_log=True),
            priv_password=dict(no_log=True),
        ),
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # Verify imports, build pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    sp = SnmpServerProfile(module.params['snmp_profile'])
    parent.add(sp)
    try:
        sp.refresh()
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    listing = sp.findall(SnmpV3Server)

    spec = {
        'name': module.params['name'],
        'manager': module.params['manager'],
        'user': module.params['user'],
        'engine_id': module.params['engine_id'],
        'auth_password': module.params['auth_password'],
        'priv_password': module.params['priv_password'],
    }
    obj = SnmpV3Server(**spec)
    sp.add(obj)

    changed, diff = helper.apply_state(obj, listing, module)
    module.exit_json(changed=changed, diff=diff, msg='Done')


if __name__ == '__main__':
    main()
