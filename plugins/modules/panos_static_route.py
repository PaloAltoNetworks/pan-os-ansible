#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
module: panos_static_route
short_description: Create static routes on PAN-OS devices.
description:
    - Create static routes on PAN-OS devices.
author:
    - Michael Richardson (@mrichardson03)
    - Garfield Lee Freeman (@shinmog)
version_added: "2.6"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is supported.
    - Panorama is supported.
    - IPv6 is not supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.state
    - paloaltonetworks.panos.fragments.full_template_support
options:
    name:
        description:
            - Name of static route.
        required: true
    destination:
        description:
            - Destination network.  Required if I(state) is I(present).
    nexthop_type:
        description:
            - Type of next hop.
        choices:
            - ip-address
            - discard
            - none
            - next-vr
        default: 'ip-address'
    nexthop:
        description:
            - Next hop IP address.  Required if I(state) is I(present).
    admin_dist:
        description:
            - Administrative distance for static route.
    metric:
        description:
            - Metric for route.
        default: '10'
    virtual_router:
        description:
            - Virtual router to use.
        default: 'default'
    interface:
        description:
            - The Interface to use.
'''

EXAMPLES = '''
- name: Create route 'Test-One'
  panos_static_route:
    provider: '{{ provider }}'
    name: 'Test-One'
    destination: '1.1.1.0/24'
    nexthop: '10.0.0.1'

- name: Create route 'Test-Two'
  panos_static_route:
    provider: '{{ provider }}'
    name: 'Test-Two'
    destination: '2.2.2.0/24'
    nexthop: '10.0.0.1'

- name: Create route 'Test-Three'
  panos_static_route:
    provider: '{{ provider }}'
    name: 'Test-Three'
    destination: '3.3.3.0/24'
    nexthop: '10.0.0.1'

- name: Delete route 'Test-Two'
  panos_static_route:
    provider: '{{ provider }}'
    name: 'Test-Two'
    state: 'absent'

- name: Create route 'Test-Four'
  panos_static_route:
    provider: '{{ provider }}'
    name: 'Test-Four'
    destination: '4.4.4.0/24'
    nexthop: '10.0.0.1'
    virtual_router: 'VR-Two'

- name: Create route 'Test-Five'
    panos_static_route:
    provider: '{{ provider }}'
    name: 'Test-Five'
    destination: '5.5.5.0/24'
    nexthop_type: 'none'
'''

RETURN = '''
# Default return values
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection


try:
    from pandevice.network import StaticRoute
    from pandevice.network import VirtualRouter
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def main():
    helper = get_connection(
        template=True,
        template_stack=True,
        with_state=True,
        with_classic_provider_spec=True,
        argument_spec=dict(
            name=dict(required=True),
            destination=dict(),
            nexthop_type=dict(
                default='ip-address',
                choices=['ip-address', 'discard', 'none', 'next-vr'],
            ),
            nexthop=dict(),
            admin_dist=dict(),
            metric=dict(type='int', default=10),
            virtual_router=dict(default='default'),
            interface=dict(),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    spec = {
        'name': module.params['name'],
        'destination': module.params['destination'],
        'nexthop_type': module.params['nexthop_type'],
        'nexthop': module.params['nexthop'],
        'interface': module.params['interface'],
        'admin_dist': module.params['admin_dist'],
        'metric': module.params['metric'],
    }

    parent = helper.get_pandevice_parent(module)
    virtual_router = module.params['virtual_router']

    # Allow None for nexthop_type.
    if spec['nexthop_type'] == 'none':
        spec['nexthop_type'] = None

    try:
        vr_list = VirtualRouter.refreshall(parent, add=False, name_only=True)
    except PanDeviceError as e:
        module.fail_json(msg='Failed vr refresh: {0}'.format(e))

    # Find the virtual router.
    for vr in vr_list:
        if vr.name == virtual_router:
            parent.add(vr)
            break
    else:
        module.fail_json(msg='Virtual router "{0}" does not exist'.format(virtual_router))

    # Get the listing.
    try:
        listing = StaticRoute.refreshall(vr, add=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    # Create the object and attach it to the object tree.
    obj = StaticRoute(**spec)
    vr.add(obj)

    # Apply the state.
    changed, diff = helper.apply_state(obj, listing, module)

    module.exit_json(changed=changed, diff=diff)


if __name__ == '__main__':
    main()
