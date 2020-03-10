#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright 2020 Palo Alto Networks, Inc
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
module: panos_ipv6_address
short_description: Manage IPv6 addresses on an interface.
description:
    - Manage IPv6 addresses on an interface.
author: "Garfield Lee Freeman (@shinmog)"
version_added: "2.9"
requirements:
    - pan-python
    - pandevice >= 0.14.0
notes:
    - Panorama is supported.
    - Checkmode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.state
    - paloaltonetworks.panos.fragments.template_only
options:
    iface_name:
        description:
            - The parent interface that this IPv6 address is attached to.
        required: true
    address:
        description:
            - IPv6 address.
        required: true
    enable_on_interface:
        description:
            - Enable address on interface.
        default: true
        type: bool
    prefix:
        description:
            - Use interface ID as host portion.
        type: bool
    anycast:
        description:
            - Enable anycast.
        type: bool
    advertise_enabled:
        description:
            - Enabled router advertisements.
        type: bool
    valid_lifetime:
        description:
            - Valid lifetime.
        default: 2592000
        type: int
    preferred_lifetime:
        description:
            - Preferred lifetime.
        default: 604800
        type: int
    onlink_flag:
        description:
            - Onlink flag.
        default: true
        type: bool
    auto_config_flag:
        description:
            - Set the auto address configuration flag.
        default: true
        type: bool
'''

EXAMPLES = '''
# Have an IPv6 address on ethernet1/6.2
- name: Assert the given IPv6 address
  panos_ipv6_address:
    provider: '{{ provider }}'
    iface_name: 'ethernet1/6.2'
    address: '2001:db8:123:1::1'
'''

RETURN = '''
# Default return values
'''

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection


try:
    from pandevice.network import AggregateInterface
    from pandevice.network import EthernetInterface
    from pandevice.network import IPv6Address
    from pandevice.network import LoopbackInterface
    from pandevice.network import TunnelInterface
    from pandevice.network import VlanInterface
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def main():
    helper = get_connection(
        template=True,
        with_classic_provider_spec=True,
        with_state=True,
        min_pandevice_version=(0, 14, 0),
        argument_spec=dict(
            iface_name=dict(required=True),
            address=dict(required=True),
            enable_on_interface=dict(type='bool', default=True),
            prefix=dict(type='bool'),
            anycast=dict(type='bool'),
            advertise_enabled=dict(type='bool'),
            valid_lifetime=dict(type='int', default=2592000),
            preferred_lifetime=dict(type='int', default=604800),
            onlink_flag=dict(type='bool', default=True),
            auto_config_flag=dict(type='bool', default=True),
        ),
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # Verify libs are present, get the parent object.
    parent = helper.get_pandevice_parent(module)

    # Get the object params.
    spec = {
        'address': module.params['address'],
        'enable_on_interface': module.params['enable_on_interface'],
        'prefix': module.params['prefix'],
        'anycast': module.params['anycast'],
        'advertise_enabled': module.params['advertise_enabled'],
        'valid_lifetime': module.params['valid_lifetime'],
        'preferred_lifetime': module.params['preferred_lifetime'],
        'onlink_flag': module.params['onlink_flag'],
        'auto_config_flag': module.params['auto_config_flag'],
    }

    # Get other info.
    iname = module.params['iface_name']

    # Determine parent interface.
    eth = None
    part = iname
    if iname.startswith('ethernet') or iname.startswith('ae'):
        part = iname.split('.')[0]
        if iname.startswith('ethernet'):
            eth = EthernetInterface(part)
        else:
            eth = AggregateInterface(part)
    else:
        if iname.startswith('loopback'):
            eth = LoopbackInterface(iname)
        elif iname.startswith('tunnel'):
            eth = TunnelInterface(iname)
        elif iname.startswith('vlan'):
            eth = VlanInterface(iname)
        else:
            module.fail_json(msg='Unknown interface style: {0}'.format(iface))

    parent.add(eth)
    try:
        eth.refresh()
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))
    if iname != part:
        for child in eth.children:
            if child.uid == iname:
                eth = child
                break
        else:
            module.fail_json(msg='Could not find parent interface')

    listing = eth.findall(IPv6Address)

    # Build the object based on the user spec.
    obj = IPv6Address(**spec)
    eth.add(obj)

    # Apply the state
    changed, diff = helper.apply_state(obj, listing, module)

    # Done.
    module.exit_json(changed=changed, diff=diff)


if __name__ == '__main__':
    main()
