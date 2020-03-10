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
module: panos_bgp_aggregate
short_description: Configures a BGP Aggregation Prefix Policy
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
    - paloaltonetworks.panos.fragments.state
    - paloaltonetworks.panos.fragments.full_template_support
options:
    commit:
        description:
            - Commit configuration if changed.
        default: True
    as_set:
        description:
            - Generate AS-set attribute.
        default: False
    attr_as_path_limit:
        description:
            - Add AS path limit attribute if it does not exist.
    attr_as_path_prepend_times:
        description:
            - Prepend local AS for specified number of times.
    attr_as_path_type:
        description:
            - AS path update options.
        choices:
            - none
            - remove
            - prepend
            - remove-and-prepend
        default: none
    attr_community_argument:
        description:
            - Argument to the action community value if needed.
    attr_community_type:
        description:
            - Community update options.
        choices:
            - none
            - remove-all
            - remove-regex
            - append
            - overwrite
        default: none
    attr_extended_community_argument:
        description:
            - Argument to the action extended community value if needed.
    attr_extended_community_type:
        description:
            - Extended community update options.
        choices:
            - none
            - remove-all
            - remove-regex
            - append
            - overwrite
        default: none
    attr_local_preference:
        description:
            - New Local Preference value.
    attr_med:
        description:
            - New Multi-Exit Discriminator value.
    attr_nexthop:
        description:
            - Next-hop address.
    attr_origin:
        description:
            - New route origin.
        choices:
            - igp
            - egp
            - incomplete
        default: incomplete
    attr_weight:
        description:
            - New weight value.
    enable:
        description:
            - Enable policy.
        default: True
        type: bool
    name:
        description:
            - Name of policy.
        required: True
    prefix:
        description:
            - Aggregating address prefix.
    summary:
        description:
            - Summarize route.
    vr_name:
        description:
            - Name of the virtual router; it must already exist; see panos_virtual_router.
        default: default
'''

EXAMPLES = '''
- name: Create BGP Aggregation Rule
  panos_bgp_aggregate:
    provider: '{{ provider }}'
    vr_name: 'default'
    name: 'aggr-rule-01'
    prefix: '10.0.0.0/24'
    enable: true
    summary: true

- name: Remove BGP Aggregation Rule
  panos_bgp_aggregate:
    provider: '{{ provider }}'
    vr_name: 'default'
    name: 'aggr-rule-01'
    state: 'absent'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection


try:
    from pandevice.errors import PanDeviceError
    from pandevice.network import Bgp
    from pandevice.network import BgpPolicyAggregationAddress
    from pandevice.network import VirtualRouter
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
            help='Name of policy'),
        enable=dict(
            default=True, type='bool',
            help='Enable policy'),
        prefix=dict(
            type='str',
            help='Aggregating address prefix'),
        summary=dict(
            type='bool',
            help='Summarize route'),
        as_set=dict(
            type='bool', default=False,
            help='Generate AS-set attribute'),
        attr_local_preference=dict(
            type='int',
            help='New Local Preference value'),
        attr_med=dict(
            type='int',
            help='New Multi-Exit Discriminator value'),
        attr_weight=dict(
            type='int',
            help='New weight value'),
        attr_nexthop=dict(
            type='list',
            help='Next-hop address'),
        attr_origin=dict(
            type='str', default='incomplete', choices=['igp', 'egp', 'incomplete'],
            help='New route origin'),
        attr_as_path_limit=dict(
            type='int',
            help='Add AS path limit attribute if it does not exist'),
        attr_as_path_type=dict(
            type='str', default='none', choices=['none', 'remove', 'prepend', 'remove-and-prepend'],
            help='AS path update options'),
        attr_as_path_prepend_times=dict(
            type='int',
            help='Prepend local AS for specified number of times'),
        attr_community_type=dict(
            type='str', default='none', choices=['none', 'remove-all', 'remove-regex', 'append', 'overwrite'],
            help='Community update options'),
        attr_community_argument=dict(
            type='str',
            help='Argument to the action community value if needed'),
        attr_extended_community_type=dict(
            type='str', default='none', choices=['none', 'remove-all', 'remove-regex', 'append', 'overwrite'],
            help='Extended community update options'),
        attr_extended_community_argument=dict(
            type='str',
            help='Argument to the action extended community value if needed'),
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

    parent = helper.get_pandevice_parent(module)

    spec = {
        'name': module.params['name'],
        'enable': module.params['enable'],
        'prefix': module.params['prefix'],
        'summary': module.params['summary'],
        'as_set': module.params['as_set'],
        'attr_local_preference': module.params['attr_local_preference'],
        'attr_med': module.params['attr_med'],
        'attr_weight': module.params['attr_weight'],
        'attr_nexthop': module.params['attr_nexthop'],
        'attr_origin': module.params['attr_origin'],
        'attr_as_path_limit': module.params['attr_as_path_limit'],
        'attr_as_path_type': module.params['attr_as_path_type'],
        'attr_as_path_prepend_times': module.params['attr_as_path_prepend_times'],
        'attr_community_type': module.params['attr_community_type'],
        'attr_community_argument': module.params['attr_community_argument'],
        'attr_extended_community_type': module.params['attr_extended_community_type'],
        'attr_extended_community_argument': module.params['attr_extended_community_argument'],
    }
    obj = BgpPolicyAggregationAddress(**spec)

    vr_name = module.params['vr_name']
    commit = module.params['commit']

    vr = VirtualRouter(vr_name)
    parent.add(vr)

    try:
        vr.refresh()
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    bgp = vr.find('', Bgp)
    if bgp is None:
        module.fail_json(msg='BGP is not configured for "{0}"'.format(vr.name))

    listing = bgp.findall(BgpPolicyAggregationAddress)
    bgp.add(obj)

    # Apply the desired state.
    changed, diff = helper.apply_state(obj, listing, module)

    # Optional: commit.
    if changed and commit:
        helper.commit(module)

    module.exit_json(changed=changed, diff=diff, msg='done')


if __name__ == '__main__':
    main()
