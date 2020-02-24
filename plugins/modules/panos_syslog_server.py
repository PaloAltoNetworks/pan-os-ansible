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
module: panos_syslog_server
short_description: Manage syslog server profile syslog servers.
description:
    - Manages syslog servers in an syslog server profile.
author: "Garfield Lee Freeman (@shinmog)"
version_added: "2.8"
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
options:
    syslog_profile:
        description:
            - Name of the syslog server profile.
        required: True
    name:
        description:
            - Server name.
        required: True
    server:
        description:
            - IP address or FQDN of the syslog server
        required: True
    transport:
        description:
            - Syslog transport.
        choices:
            - UDP
            - TCP
            - SSL
        default: "UDP"
    syslog_port:
        description:
            - Syslog port number
        type: int
    format:
        description:
            Format of the syslog message.
        choices:
            - BSD
            - IETF
        default: "BSD"
    facility:
        description:
            - Syslog facility.
        choices:
            - LOG_USER
            - LOG_LOCAL0
            - LOG_LOCAL1
            - LOG_LOCAL2
            - LOG_LOCAL3
            - LOG_LOCAL4
            - LOG_LOCAL5
            - LOG_LOCAL6
            - LOG_LOCAL7
        default: "LOG_USER"
'''

EXAMPLES = '''
- name: Create syslog server
  panos_syslog_server:
    provider: '{{ provider }}'
    syslog_profile: 'my-profile'
    name: 'my-syslog-server'
    server: '10.1.1.1'
    syslog_port: 514
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection


try:
    from pandevice.device import SyslogServerProfile
    from pandevice.device import SyslogServer
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
            syslog_profile=dict(required=True),
            name=dict(required=True),
            server=dict(required=True),
            transport=dict(default='UDP', choices=['UDP', 'TCP', 'SSL']),
            syslog_port=dict(type='int'),
            format=dict(default='BSD', choices=['BSD', 'IETF']),
            facility=dict(default='LOG_USER', choices=[
                'LOG_USER',
                'LOG_LOCAL0', 'LOG_LOCAL1', 'LOG_LOCAL2', 'LOG_LOCAL3',
                'LOG_LOCAL4', 'LOG_LOCAL5', 'LOG_LOCAL6', 'LOG_LOCAL7']),
        ),
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # Verify imports, build pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    sp = SyslogServerProfile(module.params['syslog_profile'])
    parent.add(sp)
    try:
        sp.refresh()
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    listing = sp.findall(SyslogServer)

    spec = {
        'name': module.params['name'],
        'server': module.params['server'],
        'transport': module.params['transport'],
        'port': module.params['syslog_port'],
        'format': module.params['format'],
        'facility': module.params['facility'],
    }
    obj = SyslogServer(**spec)
    sp.add(obj)

    changed, diff = helper.apply_state(obj, listing, module)
    module.exit_json(changed=changed, diff=diff, msg='Done')


if __name__ == '__main__':
    main()
