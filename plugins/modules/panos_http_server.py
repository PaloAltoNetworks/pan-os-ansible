#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: panos_http_server
short_description: Manage HTTP servers in a HTTP server profile.
description:
    - Manages HTTP servers in a HTTP server profile.
author: "Garfield Lee Freeman (@shinmog)"
version_added: "2.8"
requirements:
    - pan-python
    - pandevice >= 0.11.1
    - PAN-OS >= 8.0
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.vsys_shared
    - paloaltonetworks.panos.fragments.device_group
options:
    http_profile:
        description:
            - Name of the http server profile.
        required: True
    name:
        description:
            - Server name.
        required: True
    address:
        description:
            - IP address or FQDN of the HTTP server
        required: True
    protocol:
        description:
            - The protocol.
        choices:
            - HTTP
            - HTTPS
        default: 'HTTPS'
    http_port:
        description:
            - Port number.
        type: int
        default: 443
    tls_version:
        description:
            - PAN-OS 9.0+
            - TLS handshake protocol version
        choices:
            - 1.0
            - 1.1
            - 1.2
    certificate_profile:
        description:
            - PAN-OS 9.0+
            - Certificate profile for validating server cert.
    http_method:
        description:
            - HTTP method to use.
        default: 'POST'
    http_username:
        description:
            - Username for basic HTTP auth.
    http_password:
        description:
            - Password for basic HTTP auth.
'''

EXAMPLES = '''
- name: Create http server
  panos_http_server:
    provider: '{{ provider }}'
    http_profile: 'my-profile'
    name: 'my-http-server'
    address: '192.168.1.5'
    http_method: 'GET'
    http_username: 'jack'
    http_password: 'burton'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection


try:
    from pandevice.device import HttpServerProfile
    from pandevice.device import HttpServer
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
        min_panos_version=(8, 0, 0),
        argument_spec=dict(
            http_profile=dict(required=True),
            name=dict(required=True),
            address=dict(required=True),
            protocol=dict(default='HTTPS', choices=['HTTP', 'HTTPS']),
            http_port=dict(type='int', default=443),
            tls_version=dict(choices=['1.0', '1.1', '1.2']),
            certificate_profile=dict(),
            http_method=dict(default='POST'),
            http_username=dict(),
            http_password=dict(no_log=True),
        ),
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # Verify imports, build pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    sp = HttpServerProfile(module.params['http_profile'])
    parent.add(sp)
    try:
        sp.refresh()
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    listing = sp.findall(HttpServer)

    spec = {
        'name': module.params['name'],
        'address': module.params['address'],
        'protocol': module.params['protocol'],
        'port': module.params['http_port'],
        'tls_version': module.params['tls_version'],
        'certificate_profile': module.params['certificate_profile'],
        'http_method': module.params['http_method'],
        'username': module.params['http_username'],
        'password': module.params['http_password'],
    }
    obj = HttpServer(**spec)
    sp.add(obj)

    changed, diff = helper.apply_state(obj, listing, module)
    module.exit_json(changed=changed, diff=diff, msg='Done')


if __name__ == '__main__':
    main()
