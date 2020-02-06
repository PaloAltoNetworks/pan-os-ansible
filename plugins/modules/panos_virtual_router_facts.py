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

DOCUMENTATION = '''
---
module: panos_virtual_router_facts
short_description: Retrieves virtual router information
description:
    - Retrieves information on virtual routers from a firewall or Panorama.
author: "Garfield Lee Freeman (@shinmog)"
version_added: "2.8"
requirements:
    - pan-python
    - pandevice
notes:
    - Panorama is supported.
    - Check mode is not supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.full_template_support
options:
    name:
        description:
            - Name of the virtual router.
'''

EXAMPLES = '''
# Get information on a specific virtual router
- name: Get vr3 info
  panos_virtual_router_facts:
    provider: '{{ provider }}'
    name: 'vr3'
  register: ans

# Get the config of all virtual routers
- name: Get all virtual routers
  panos_virtual_router_facts:
    provider: '{{ provider }}'
  register: vrlist
'''

RETURN = '''
spec:
    description: The spec of the specified virtual router.
    returned: When I(name) is specified.
    type: complex
    contains:
        name:
            description: Virtual router name.
        interface:
            description: List of interfaces
            type: list
        ad_static:
            description: Admin distance for this protocol.
            type: int
        ad_static_ipv6:
            description: Admin distance for this protocol.
            type: int
        ad_ospf_int:
            description: Admin distance for this protocol.
            type: int
        ad_ospf_ext:
            description: Admin distance for this protocol.
            type: int
        ad_ospfv3_int:
            description: Admin distance for this protocol.
            type: int
        ad_ospfv3_ext:
            description: Admin distance for this protocol.
            type: int
        ad_ibgp:
            description: Admin distance for this protocol.
            type: int
        ad_ebgp:
            description: Admin distance for this protocol.
            type: int
        ad_rip:
            description: Admin distance for this protocol.
            type: int
vrlist:
    description: List of virtual router specs.
    returned: When I(name) is not specified.
    type: list
'''

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection


try:
    from pandevice.network import VirtualRouter
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def main():
    helper = get_connection(
        template=True,
        template_stack=True,
        with_classic_provider_spec=True,
        argument_spec=dict(
            name=dict(),
        ),
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=False,
        required_one_of=helper.required_one_of,
    )

    # Verify imports, build pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    name = module.params['name']
    if name is None:
        try:
            listing = VirtualRouter.refreshall(parent)
        except PanDeviceError as e:
            module.fail_json(msg='Failed refreshall: {0}'.format(e))

        vrlist = helper.to_module_dict(listing)
        module.exit_json(changed=False, vrlist=vrlist)

    vr = VirtualRouter(name)
    parent.add(vr)
    try:
        vr.refresh()
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    spec = helper.to_module_dict(vr)
    module.exit_json(changed=False, spec=spec)


if __name__ == '__main__':
    main()
