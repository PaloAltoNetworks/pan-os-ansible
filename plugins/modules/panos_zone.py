#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

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

DOCUMENTATION = '''
---
module: panos_zone
short_description: configure security zone
description:
    - Configure security zones on PAN-OS firewall or in Panorama template.
author:
    - Robert Hagen (@stealthllama)
    - Garfield Lee Freeman (@shinmog)
version_added: "2.8"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
    - pandevice >= 0.8.0
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.state
    - paloaltonetworks.panos.fragments.full_template_support
    - paloaltonetworks.panos.fragments.vsys
options:
    zone:
        description:
            - Name of the security zone to configure.
        required: true
    mode:
        description:
            - The mode of the security zone. Must match the mode of the interface.
        choices:
            - tap
            - virtual-wire
            - layer2
            - layer3
            - external
        default: "layer3"
    interface:
        description:
            - List of member interfaces.
        type: list
    zone_profile:
        description:
            - Zone protection profile.
    log_setting:
        description:
            - Log forwarding setting.
    enable_userid:
        description:
            - Enable user identification.
        type: bool
    include_acl:
        description:
            - User identification ACL include list.
        type: list
    exclude_acl:
        description:
            - User identification ACL exclude list.
        type: list
'''

EXAMPLES = '''
# Create an L3 zone.
- name: create DMZ zone on a firewall
  panos_zone:
    provider: '{{ provider }}'
    zone: 'dmz'
    mode: 'layer3'
    zone_profile: 'strict'

# Add an interface to the zone.
- name: add ethernet1/2 to zone dmz
  panos_interface:
    provider: '{{ provider }}'
    zone: 'dmz'
    mode: 'layer3'
    interface: ['ethernet1/2']
    zone_profile: 'strict'

# Delete the zone.
- name: delete the DMZ zone
  panos_interface:
    provider: '{{ provider }}'
    zone: 'dmz'
    state: 'absent'

# Add a zone to a multi-VSYS Panorama template
- name: add Cloud zone to template
  panos_interface:
    provider: '{{ provider }}'
    template: 'Datacenter Template'
    vsys: 'vsys4'
    zone: 'datacenter'
    mode: 'layer3'
    enable_userid: true
    exclude_acl: ['10.0.200.0/24']
'''

RETURN = '''
# Default return values
'''

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import get_exception
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection


try:
    from pandevice.network import Zone
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def main():
    helper = get_connection(
        vsys=True,
        template=True,
        template_stack=True,
        with_state=True,
        with_classic_provider_spec=True,
        argument_spec=dict(
            zone=dict(required=True),
            mode=dict(choices=['tap', 'virtual-wire', 'layer2', 'layer3', 'external'], default='layer3'),
            interface=dict(type='list'),
            zone_profile=dict(),
            log_setting=dict(),
            enable_userid=dict(type='bool', default=False),
            include_acl=dict(type='list'),
            exclude_acl=dict(type='list'),
        ),
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # Verify imports, build pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    # Set the Zone object params
    zone_spec = {
        'name': module.params['zone'],
        'mode': module.params['mode'],
        'interface': module.params['interface'],
        'zone_profile': module.params['zone_profile'],
        'log_setting': module.params['log_setting'],
        'enable_user_identification': module.params['enable_userid'],
        'include_acl': module.params['include_acl'],
        'exclude_acl': module.params['exclude_acl']
    }

    # Retrieve the current list of zones
    try:
        zones = Zone.refreshall(parent, add=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    # Build the zone and attach to the parent
    new_zone = Zone(**zone_spec)
    parent.add(new_zone)

    # Perform the requeseted action.
    changed, diff = helper.apply_state(new_zone, zones, module)

    # Done!
    module.exit_json(changed=changed, diff=diff, msg='Done!')


if __name__ == '__main__':
    main()
