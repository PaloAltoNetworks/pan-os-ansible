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
module: panos_syslog_profile
short_description: Manage syslog server profiles.
description:
    - Manages syslog server profiles.
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
    name:
        description:
            - Name of the profile.
        required: true
    config:
        description:
            - Custom config log format.
    system:
        description:
            - Custom system log format.
    threat:
        description:
            - Custom threat log format.
    traffic:
        description:
            - Custom traffic log format.
    hip_match:
        description:
            - Custom HIP match log format.
    url:
        description:
            - PAN-OS 8.0+
            - Custom url log format.
    data:
        description:
            - PAN-OS 8.0+
            - Custom data log format.
    wildfire:
        description:
            - PAN-OS 8.0+
            - Custom wildfire log format.
    tunnel:
        description:
            - PAN-OS 8.0+
            - Custom tunnel log format.
    user_id:
        description:
            - PAN-OS 8.0+
            - Custom user-ID log format.
    gtp:
        description:
            - PAN-OS 8.0+
            - Custom GTP log format.
    auth:
        description:
            - PAN-OS 8.0+
            - Custom auth log format.
    sctp:
        description:
            - PAN-OS 8.1+
            - Custom SCTP log format.
    iptag:
        description:
            - PAN-OS 9.0+
            - Custom Iptag log format.
    escaped_characters:
        description:
            - Characters to be escaped.
    escape_character:
        description:
            - Escape character
'''

EXAMPLES = '''
# Create a profile
- name: Create syslog profile
  panos_syslog_profile:
    provider: '{{ provider }}'
    name: 'my-profile'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection


try:
    from pandevice.device import SyslogServerProfile
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
            config=dict(),
            system=dict(),
            threat=dict(),
            traffic=dict(),
            hip_match=dict(),
            url=dict(),
            data=dict(),
            wildfire=dict(),
            tunnel=dict(),
            user_id=dict(),
            gtp=dict(),
            auth=dict(),
            sctp=dict(),
            iptag=dict(),
            escaped_characters=dict(),
            escape_character=dict(),
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
        listing = SyslogServerProfile.refreshall(parent)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    spec = {
        'name': module.params['name'],
        'config': module.params['config'],
        'system': module.params['system'],
        'threat': module.params['threat'],
        'traffic': module.params['traffic'],
        'hip_match': module.params['hip_match'],
        'url': module.params['url'],
        'data': module.params['data'],
        'wildfire': module.params['wildfire'],
        'tunnel': module.params['tunnel'],
        'user_id': module.params['user_id'],
        'gtp': module.params['gtp'],
        'auth': module.params['auth'],
        'sctp': module.params['sctp'],
        'iptag': module.params['iptag'],
        'escaped_characters': module.params['escaped_characters'],
        'escape_character': module.params['escape_character'],
    }
    obj = SyslogServerProfile(**spec)
    parent.add(obj)

    changed, diff = helper.apply_state(obj, listing, module)
    module.exit_json(changed=changed, diff=diff, msg='Done')


if __name__ == '__main__':
    main()
