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
module: panos_virtual_router
short_description: Configures a Virtual Router
description:
    - Manage PANOS Virtual Router
author:
    - Joshua Colson (@freakinhippie)
    - Garfield Lee Freeman (@shinmog)
version_added: "2.9"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.state
    - paloaltonetworks.panos.fragments.vsys_import
    - paloaltonetworks.panos.fragments.full_template_support
notes:
    - Checkmode is supported.
    - Panorama is supported.
options:
    commit:
        description:
            - Commit configuration if changed.
        default: true
        type: bool
    name:
        description:
            -  Name of virtual router
        default: 'default'
    interface:
        description:
            -  List of interface names
        type: list
    ad_static:
        description:
            -  Administrative distance for this protocol
        type: int
    ad_static_ipv6:
        description:
            -  Administrative distance for this protocol
        type: int
    ad_ospf_int:
        description:
            -  Administrative distance for this protocol
        type: int
    ad_ospf_ext:
        description:
            -  Administrative distance for this protocol
        type: int
    ad_ospfv3_int:
        description:
            -  Administrative distance for this protocol
        type: int
    ad_ospfv3_ext:
        description:
            -  Administrative distance for this protocol
        type: int
    ad_ibgp:
        description:
            -  Administrative distance for this protocol
        type: int
    ad_ebgp:
        description:
            -  Administrative distance for this protocol
        type: int
    ad_rip:
        description:
            -  Administrative distance for this protocol
        type: int
'''

EXAMPLES = '''
- name: Create Virtual Router
    panos_virtual_router:
      provider: '{{ provider }}'
      name: vr-1
      commit: true
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection


try:
    from pandevice.network import VirtualRouter
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def setup_args():
    return dict(
        commit=dict(
            type='bool', default=True,
            help='Commit configuration if changed'),

        name=dict(
            type='str', default='default',
            help='Name of virtual router'),
        interface=dict(
            type='list',
            help='List of interface names'),
        ad_static=dict(
            type='int',
            help='Administrative distance for this protocol'),
        ad_static_ipv6=dict(
            type='int',
            help='Administrative distance for this protocol'),
        ad_ospf_int=dict(
            type='int',
            help='Administrative distance for this protocol'),
        ad_ospf_ext=dict(
            type='int',
            help='Administrative distance for this protocol'),
        ad_ospfv3_int=dict(
            type='int',
            help='Administrative distance for this protocol'),
        ad_ospfv3_ext=dict(
            type='int',
            help='Administrative distance for this protocol'),
        ad_ibgp=dict(
            type='int',
            help='Administrative distance for this protocol'),
        ad_ebgp=dict(
            type='int',
            help='Administrative distance for this protocol'),
        ad_rip=dict(
            type='int',
            help='Administrative distance for this protocol'),
    )


def main():
    helper = get_connection(
        vsys_importable=True,
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

    # Verify imports, build pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    # Exclude non-object items from kwargs passed to the object.
    exclude_list = [
        'ip_address', 'username', 'password', 'api_key', 'state', 'commit',
        'provider', 'template', 'template_stack', 'vsys', 'port',
    ]

    # Generate the kwargs for network.VirtualRouter.
    obj_spec = dict((k, module.params[k]) for k in helper.argument_spec.keys() if k not in exclude_list)

    name = module.params['name']
    state = module.params['state']
    commit = module.params['commit']

    # Retrieve current virtual routers.
    try:
        vr_list = VirtualRouter.refreshall(parent, add=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    # Create the new state object.
    virtual_router = VirtualRouter(**obj_spec)
    parent.add(virtual_router)

    reference_params = {
        'refresh': True,
        'update': not module.check_mode,
        'return_type': 'bool',
    }
    changed = False
    if state == 'present':
        for item in vr_list:
            if item.name != name:
                continue
            if not item.equal(virtual_router, compare_children=False):
                changed = True
                virtual_router.extend(item.children)
                if not module.check_mode:
                    try:
                        virtual_router.apply()
                    except PanDeviceError as e:
                        module.fail_json(msg='Failed apply: {0}'.format(e))
            break
        else:
            changed = True
            if not module.check_mode:
                try:
                    virtual_router.create()
                except PanDeviceError as e:
                    module.fail_json(msg='Failed apply: {0}'.format(e))

        changed |= virtual_router.set_vsys(
            module.params['vsys'], **reference_params)
    else:
        changed |= virtual_router.set_vsys(
            None, **reference_params)
        if name in [x.name for x in vr_list]:
            changed = True
            if not module.check_mode:
                try:
                    virtual_router.delete()
                except PanDeviceError as e:
                    module.fail_json(msg='Failed delete: {0}'.format(e))

    if commit and changed:
        helper.commit(module)

    if not changed:
        msg = 'no changes required.'
    elif module.check_mode:
        msg = 'Changes are required.'
    else:
        msg = 'Virtual router update successful.'

    module.exit_json(msg=msg, changed=changed)


if __name__ == '__main__':
    main()
