#!/usr/bin/python
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

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: panos_gre_tunnel
short_description: Create GRE tunnels on PAN-OS devices.
description:
    - Create GRE tunnel objects on PAN-OS devices.
author:
    - Garfield Lee Freeman (@shinmog)
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - 'Minimum PAN-OS version: 9.0'
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.full_template_support
    - paloaltonetworks.panos.fragments.state
options:
    name:
        description:
            - Name of object to create.
        type: str
        required: true
    interface:
        description:
            - Interface to terminate the tunnel.
        type: str
    local_address_type:
        description:
            Type of local address.
        type: str
        choices:
            - ip
            - floating-ip
        default: ip
    local_address_value:
        description:
            - IP address value.
        type: str
    peer_address:
        description:
            - Peer IP address.
        type: str
    tunnel_interface:
        description:
            - To apply GRE tunnels to tunnel interface.
        type: str
    ttl:
        description:
            - TTL.
        type: int
        default: 64
    copy_tos:
        description:
            - Copy IP TOS bits from inner packet to GRE packet.
        type: bool
    enable_keep_alive:
        description:
            - Enable tunnel monitoring.
        type: bool
    keep_alive_interval:
        description:
            - Keep alive interval.
        type: int
        default: 10
    keep_alive_retry:
        description:
            - Keep alive retry time.
        type: int
        default: 3
    keep_alive_hold_timer:
        description:
            - Keep alive hold timer.
        type: int
        default: 5
    disabled:
        description:
            - Disable the GRE tunnel.
        type: bool
'''

EXAMPLES = '''
- name: Create GRE tunnel
  panos_gre_tunnel:
    provider: '{{ provider }}'
    name: 'myGreTunnel'
    interface: 'ethernet1/5'
    local_address_value: '10.1.1.1/24'
    peer_address: '192.168.1.1'
    tunnel_interface: 'tunnel.7'
    ttl: 42
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from panos.network import GreTunnel
    from panos.errors import PanDeviceError
except ImportError:
    try:
        from pandevice.network import GreTunnel
        from pandevice.errors import PanDeviceError
    except ImportError:
        pass


def main():
    helper = get_connection(
        template=True,
        template_stack=True,
        with_classic_provider_spec=True,
        with_state=True,
        min_pandevice_version=(0, 13, 0),
        min_panos_version=(9, 0, 0),
        argument_spec=dict(
            name=dict(required=True),
            interface=dict(),
            local_address_type=dict(default='ip', choices=['ip', 'floating-ip']),
            local_address_value=dict(),
            peer_address=dict(),
            tunnel_interface=dict(),
            ttl=dict(type='int', default=64),
            copy_tos=dict(type='bool'),
            enable_keep_alive=dict(type='bool'),
            keep_alive_interval=dict(type='int', default=10),
            keep_alive_retry=dict(type='int', default=3),
            keep_alive_hold_timer=dict(type='int', default=5),
            disabled=dict(type='bool'),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        required_one_of=helper.required_one_of,
        supports_check_mode=True,
    )

    # Verify libs are present, get parent object.
    parent = helper.get_pandevice_parent(module)

    # Object params.
    spec = {
        'name': module.params['name'],
        'interface': module.params['interface'],
        'local_address_type': module.params['local_address_type'],
        'local_address_value': module.params['local_address_value'],
        'peer_address': module.params['peer_address'],
        'tunnel_interface': module.params['tunnel_interface'],
        'ttl': module.params['ttl'],
        'copy_tos': module.params['copy_tos'],
        'enable_keep_alive': module.params['enable_keep_alive'],
        'keep_alive_interval': module.params['keep_alive_interval'],
        'keep_alive_retry': module.params['keep_alive_retry'],
        'keep_alive_hold_timer': module.params['keep_alive_hold_timer'],
        'disabled': module.params['disabled'],
    }

    # Retrieve current info.
    try:
        listing = GreTunnel.refreshall(parent, add=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    # Build the object based on the user spec.
    obj = GreTunnel(**spec)
    parent.add(obj)

    # Apply the state.
    changed, diff = helper.apply_state(obj, listing, module)

    # Done.
    module.exit_json(changed=changed, diff=diff)


if __name__ == '__main__':
    main()
