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
module: panos_bgp_peer_group
short_description: Configures a BGP Peer Group
description:
    - Use BGP to publish and consume routes from disparate networks.
author:
    - Joshua Colson (@freakinhippie)
    - Garfield Lee Freeman (@shinmog)
version_added: "2.9"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is supported.
    - Panorama is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.state
    - paloaltonetworks.panos.fragments.full_template_support
options:
    commit:
        description:
            - Commit configuration if changed.
        default: True
        type: bool
    aggregated_confed_as_path:
        description:
            - The peers understand Aggregated Confederation AS Path.
        type: bool
    enable:
        description:
            - Enable BGP peer group.
        default: True
        type: bool
    export_nexthop:
        description:
            - Export locally resolved nexthop.
        choices:
            - resolve
            - use-self
        default: 'resolve'
    import_nexthop:
        description:
            - I(type=ebgp) only; override nexthop with peer address.
        choices:
            - original
            - use-peer
        default: 'original'
    name:
        description:
            - Name of the BGP peer group.
        required: True
    remove_private_as:
        description:
            - I(type=ebgp) only; remove private AS when exporting route.
        type: bool
    soft_reset_with_stored_info:
        description:
            - Enable soft reset with stored info.
        type: bool
    type:
        description:
            - Peer group type.
        choices:
            - ebgp
            - ibgp
            - ebgp-confed
            - ibgp-confed
        default: 'ebgp'
    vr_name:
        description:
            - Name of the virtual router; it must already exist; see panos_virtual_router.
        default: 'default'
'''

EXAMPLES = '''
- name: Create BGP Peer Group
  panos_bgp_peer_group:
    provider: '{{ provider }}'
    name: 'peer-group-1'
    enable: true
    aggregated_confed_as_path: true
    soft_reset_with_stored_info: false
    commit: true
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection


try:
    from pandevice.errors import PanDeviceError
    from pandevice.network import Bgp
    from pandevice.network import BgpPeerGroup
    from pandevice.network import VirtualRouter
except ImportError:
    pass


def setup_args():
    return dict(
        name=dict(
            type='str', required=True,
            help='Name of the BGP peer group'),
        enable=dict(
            default=True, type='bool',
            help='Enable BGP peer group'),
        aggregated_confed_as_path=dict(
            type='bool',
            help='The peers understand Aggregated Confederation AS Path'),
        soft_reset_with_stored_info=dict(
            type='bool',
            help='Enable soft reset with stored info'),
        type=dict(
            type='str', default='ebgp', choices=['ebgp', 'ibgp', 'ebgp-confed', 'ibgp-confed'],
            help='Peer group type I("ebgp")/I("ibgp")/I("ebgp-confed")/I("ibgp-confed")'),
        export_nexthop=dict(
            type='str', default='resolve', choices=['resolve', 'use-self'],
            help='Export locally resolved nexthop I("resolve")/I("use-self")'),
        import_nexthop=dict(
            type='str', default='original', choices=['original', 'use-peer'],
            help='Override nexthop with peer address I("original")/I("use-peer"), only with "ebgp"'),
        remove_private_as=dict(
            type='bool',
            help='Remove private AS when exporting route, only with "ebgp"'),
        vr_name=dict(
            default='default',
            help='Name of the virtual router; it must already exist; see panos_virtual_router'),
        commit=dict(
            type='bool', default=True,
            help='Commit configuration if changed'),
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

    # Verify libs are present, get pandevice parent.
    parent = helper.get_pandevice_parent(module)

    # Verify the virtual router is present.
    vr = VirtualRouter(module.params['vr_name'])
    parent.add(vr)
    try:
        vr.refresh()
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    bgp = vr.find('', Bgp)
    if bgp is None:
        module.fail_json(msg='BGP is not configured for "{0}"'.format(vr.name))

    listing = bgp.findall(BgpPeerGroup)
    spec = {
        'name': module.params['name'],
        'enable': module.params['enable'],
        'aggregated_confed_as_path': module.params['aggregated_confed_as_path'],
        'soft_reset_with_stored_info': module.params['soft_reset_with_stored_info'],
        'type': module.params['type'],
        'export_nexthop': module.params['export_nexthop'],
        'import_nexthop': module.params['import_nexthop'],
        'remove_private_as': module.params['remove_private_as'],
    }
    obj = BgpPeerGroup(**spec)
    bgp.add(obj)

    # Apply the state.
    changed, diff = helper.apply_state(obj, listing, module)

    # Optional commit.
    if changed and module.params['commit']:
        helper.commit(module)

    module.exit_json(changed=changed, diff=diff, msg='done')


if __name__ == '__main__':
    main()
