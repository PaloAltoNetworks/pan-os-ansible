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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: panos_bgp_dampening
short_description: Configures a BGP Dampening Profile
description:
    - Use BGP to publish and consume routes from disparate networks.
author:
    - Joshua Colson (@freakinhippie)
    - Garfield Lee Freeman (@shinmog)
version_added: "2.8"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is supported.
    - Panorama is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.full_template_support
    - paloaltonetworks.panos.fragments.state
options:
    commit:
        description:
            - Commit configuration if changed.
        default: True
        type: bool
    vr_name:
        description:
            - Name of the virtual router; it must already exist.
            - See M(panos_virtual_router).
        default: 'default'
    cutoff:
        description:
            - Cutoff threshold value.
        type: float
    decay_half_life_reachable:
        description:
            - Decay half-life while reachable (in seconds).
        type: int
    decay_half_life_unreachable:
        description:
            - Decay half-life while unreachable (in seconds).
        type: int
    enable:
        description:
            - Enable profile.
        default: True
        type: bool
    max_hold_time:
        description:
            - Maximum of hold-down time (in seconds).
        type: int
    name:
        description:
            - Name of Dampening Profile.
        required: True
    reuse:
        description:
            - Reuse threshold value.
        type: float
'''

EXAMPLES = '''
- name: Create BGP Dampening Profile
  panos_bgp_dampening:
    name: damp-profile-1
    enable: true
    commit: true
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection


try:
    from pandevice.errors import PanDeviceError
    from pandevice.network import VirtualRouter
    from pandevice.network import Bgp
    from pandevice.network import BgpDampeningProfile
except ImportError:
    pass


def setup_args():
    return dict(
        commit=dict(
            type='bool', default=True,
            help='Commit configuration if changed'),

        vr_name=dict(
            default='default',
            help='Name of the virtual router; it must already exist; see panos_virtual_router'),

        name=dict(
            type='str', required=True,
            help='Name of Dampening Profile'),
        enable=dict(
            default=True, type='bool',
            help='Enable profile'),
        cutoff=dict(
            type='float',
            help='Cutoff threshold value'),
        reuse=dict(
            type='float',
            help='Reuse threshold value'),
        max_hold_time=dict(
            type='int',
            help='Maximum of hold-down time (in seconds)'),
        decay_half_life_reachable=dict(
            type='int',
            help='Decay half-life while reachable (in seconds)'),
        decay_half_life_unreachable=dict(
            type='int',
            help='Decay half-life while unreachable (in seconds)'),
    )


def main():
    helper = get_connection(
        template=True,
        template_stack=True,
        with_state=True,
        with_classic_provider_spec=True,
        argument_spec=setup_args(),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # Verify libs, initialize pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    vr = VirtualRouter(module.params['vr_name'])
    parent.add(vr)
    try:
        vr.refresh()
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    bgp = vr.find('', Bgp)
    if bgp is None:
        module.fail_json(msg='BGP is not configured for virtual router "{0}"'.format(vr.name))

    listing = bgp.findall(BgpDampeningProfile)
    spec = {
        'name': module.params['name'],
        'enable': module.params['enable'],
        'cutoff': module.params['cutoff'],
        'reuse': module.params['reuse'],
        'max_hold_time': module.params['max_hold_time'],
        'decay_half_life_reachable': module.params['decay_half_life_reachable'],
        'decay_half_life_unreachable': module.params['decay_half_life_unreachable'],
    }
    obj = BgpDampeningProfile(**spec)
    bgp.add(obj)

    # Apply the requested state.
    changed, diff = helper.apply_state(obj, listing, module)

    # Optional commit.
    if changed and module.params['commit']:
        helper.commit(module)

    module.exit_json(changed=changed, diff=diff, msg='done')


if __name__ == '__main__':
    main()
