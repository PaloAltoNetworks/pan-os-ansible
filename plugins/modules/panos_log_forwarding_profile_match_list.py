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
module: panos_log_forwarding_profile_match_list
short_description: Manage log forwarding profile match lists.
description:
    - Manages log forwarding profile match lists.
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
    log_forwarding_profile:
        description:
            - Name of the log forwarding profile to add this match list to.
        required: True
    name:
        description:
            - Name of the profile.
        required: true
    description:
        description:
            - Profile description
    log_type:
        description:
            - Log type.
        choices:
            - traffic
            - threat
            - wildfire
            - url
            - data
            - gtp
            - tunnel
            - auth
            - sctp
        default: 'traffic'
    filter:
        description:
            - The filter.  Leaving this empty means "All logs".
    send_to_panorama:
        description:
            - Send to panorama or not
        type: bool
    snmp_profiles:
        description:
            - List of SNMP server profiles.
        type: list
    email_profiles:
        description:
            - List of email server profiles.
        type: list
    syslog_profiles:
        description:
            - List of syslog server profiles.
        type: list
    http_profiles:
        description:
            - List of HTTP server profiles.
        type: list
'''

EXAMPLES = '''
# Create a server match list
- name: Create log forwarding profile match list
  panos_log_forwarding_profile_match_list:
    provider: '{{ provider }}'
    log_forwarding_profile: 'my-profile'
    name: 'ml-1'
    description: 'created by Ansible'
    log_type: 'threat'
    filter: '(action eq allow) and (zone eq DMZ)'
    syslog_profiles: ['syslog-prof1']
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection


try:
    from pandevice.objects import LogForwardingProfile
    from pandevice.objects import LogForwardingProfileMatchList
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
            log_forwarding_profile=dict(required=True),
            name=dict(required=True),
            description=dict(),
            log_type=dict(default='traffic', choices=[
                'traffic', 'threat', 'wildfire',
                'url', 'data', 'gtp', 'tunnel', 'auth', 'sctp']),
            filter=dict(),
            send_to_panorama=dict(type='bool'),
            snmp_profiles=dict(type='list'),
            email_profiles=dict(type='list'),
            syslog_profiles=dict(type='list'),
            http_profiles=dict(type='list'),
        ),
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # Verify imports, build pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    lfp = LogForwardingProfile(module.params['log_forwarding_profile'])
    parent.add(lfp)
    try:
        lfp.refresh()
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    listing = lfp.findall(LogForwardingProfileMatchList)

    spec = {
        'name': module.params['name'],
        'description': module.params['description'],
        'log_type': module.params['log_type'],
        'filter': module.params['filter'],
        'send_to_panorama': module.params['send_to_panorama'],
        'snmp_profiles': module.params['snmp_profiles'],
        'email_profiles': module.params['email_profiles'],
        'syslog_profiles': module.params['syslog_profiles'],
        'http_profiles': module.params['http_profiles'],
    }
    obj = LogForwardingProfileMatchList(**spec)
    lfp.add(obj)

    changed, diff = helper.apply_state(obj, listing, module)
    module.exit_json(changed=changed, diff=diff, msg='Done')


if __name__ == '__main__':
    main()
