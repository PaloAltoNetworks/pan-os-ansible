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
module: panos_ipsec_profile
short_description: Configures IPSec Crypto profile on the firewall with subset of settings.
description:
    - IPSec Crypto profiles specify protocols and algorithms for authentication and encryption in VPN tunnels based on
      IPSec SA negotiation (Phase 2).
author: "Ivan Bojer (@ivanbojer)"
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.state
    - paloaltonetworks.panos.fragments.full_template_support
    - paloaltonetworks.panos.fragments.deprecated_commit
options:
    name:
        description:
            - Name for the profile.
        type: str
        required: true
    esp_encryption:
        description: Encryption algorithms for ESP mode.
        type: list
        elements: str
        choices: ['des', '3des', 'null', 'aes-128-cbc', 'aes-192-cbc',
                  'aes-256-cbc', 'aes-128-gcm', 'aes-256-gcm']
        aliases:
            - encryption
    esp_authentication:
        description: Authentication algorithms for ESP mode.
        type: list
        elements: str
        choices: ['none', 'md5', 'sha1', 'sha256', 'sha384', 'sha512']
        aliases:
            - authentication
    ah_authentication:
        description: Authentication algorithms for AH mode.
        type: list
        elements: str
        choices: ['md5', 'sha1', 'sha256', 'sha384', 'sha512']
    dh_group:
        description:
            - Diffie-Hellman (DH) groups.
        type: str
        choices: ['no-pfs', 'group1', 'group2', 'group5', 'group14', 'group19', 'group20']
        default: group2
        aliases:
            - dhgroup
    lifetime_seconds:
        description:
            -  IPSec SA lifetime in seconds.
        type: int
    lifetime_minutes:
        description:
            - IPSec SA lifetime in minutes.
        type: int
    lifetime_hours:
        description:
            - IPSec SA lifetime in hours.  If no other key lifetimes are
              specified, default to 1 hour.
        type: int
        aliases:
            - lifetime_hrs
    lifetime_days:
        description:
            - IPSec SA lifetime in days.
        type: int
    lifesize_kb:
        description:
            -  IPSec SA lifetime in kilobytes.
        type: int
    lifesize_mb:
        description:
            - IPSec SA lifetime in megabytes.
        type: int
    lifesize_gb:
        description:
            - IPSec SA lifetime in gigabytes.
        type: int
    lifesize_tb:
        description:
            - IPSec SA lifetime in terabytes.
        type: int
'''

EXAMPLES = '''
- name: Add IPSec crypto config to the firewall
  panos_ipsec_profile:
    provider: '{{ provider }}'
    state: 'present'
    name: 'ipsec-vpn-0cc61dd8c06f95cfd-0'
    esp_authentication: ['sha1']
    esp_encryption: ['aes-128-cbc']
    lifetime_seconds: '3600'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from panos.network import IpsecCryptoProfile
    from panos.errors import PanDeviceError
except ImportError:
    try:
        from pandevice.network import IpsecCryptoProfile
        from pandevice.errors import PanDeviceError
    except ImportError:
        pass


def main():
    helper = get_connection(
        template=True,
        template_stack=True,
        with_classic_provider_spec=True,
        with_state=True,
        argument_spec=dict(
            name=dict(required=True),
            esp_encryption=dict(
                type='list',
                elements='str',
                choices=[
                    'des', '3des', 'null', 'aes-128-cbc', 'aes-192-cbc',
                    'aes-256-cbc', 'aes-128-gcm', 'aes-256-gcm'
                ],
                aliases=['encryption']
            ),
            esp_authentication=dict(
                type='list',
                elements='str',
                choices=[
                    'none', 'md5', 'sha1', 'sha256', 'sha384', 'sha512'
                ],
                aliases=['authentication']
            ),
            ah_authentication=dict(
                type='list',
                elements='str',
                choices=[
                    'md5', 'sha1', 'sha256', 'sha384', 'sha512'
                ]
            ),
            dh_group=dict(
                choices=[
                    'no-pfs', 'group1', 'group2', 'group5', 'group14', 'group19',
                    'group20'
                ],
                default='group2',
                aliases=['dhgroup']
            ),
            lifetime_seconds=dict(type='int'),
            lifetime_minutes=dict(type='int'),
            lifetime_hours=dict(type='int', aliases=['lifetime_hrs']),
            lifetime_days=dict(type='int'),
            lifesize_kb=dict(type='int'),
            lifesize_mb=dict(type='int'),
            lifesize_gb=dict(type='int'),
            lifesize_tb=dict(type='int'),
            commit=dict(type='bool', default=False)
        )
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        required_one_of=helper.required_one_of,
        mutually_exclusive=[
            ['esp_encryption', 'ah_authentication'],
            ['esp_authentication', 'ah_authentication'],
            ['lifetime_seconds', 'lifetime_minutes', 'lifetime_hours', 'lifetime_days'],
            ['lifesize_kb', 'lifesize_mb', 'lifesize_gb', 'lifesize_tb']
        ],
        supports_check_mode=True
    )

    # Verify libs are present, get parent object.
    parent = helper.get_pandevice_parent(module)

    spec = {
        'name': module.params['name'],
        'esp_encryption': module.params['esp_encryption'],
        'esp_authentication': module.params['esp_authentication'],
        'ah_authentication': module.params['ah_authentication'],
        'dh_group': module.params['dh_group'],
        'lifetime_seconds': module.params['lifetime_seconds'],
        'lifetime_minutes': module.params['lifetime_minutes'],
        'lifetime_hours': module.params['lifetime_hours'],
        'lifetime_days': module.params['lifetime_days'],
        'lifesize_kb': module.params['lifesize_kb'],
        'lifesize_mb': module.params['lifesize_mb'],
        'lifesize_gb': module.params['lifesize_gb'],
        'lifesize_tb': module.params['lifesize_tb']
    }

    # Other info.
    commit = module.params['commit']

    if spec['esp_encryption'] is None and spec['ah_authentication'] is None:
        spec['esp_encryption'] = ['aes-256-cbc', '3des']

    if spec['esp_authentication'] is None and spec['ah_authentication'] is None:
        spec['esp_authentication'] = ['sha1']

    # Reflect GUI behavior.  Default is 1 hour key lifetime if nothing else is
    # specified.
    if not any([
        spec['lifetime_seconds'], spec['lifetime_minutes'], spec['lifetime_hours'], spec['lifetime_days']
    ]):
        spec['lifetime_hours'] = 1

    # Retrieve current info.
    try:
        listing = IpsecCryptoProfile.refreshall(parent, add=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    # Build the object based on the user spec.
    obj = IpsecCryptoProfile(**spec)
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
