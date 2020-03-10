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
module: panos_bgp_peer
short_description: Configures a BGP Peer
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
    address_family_identifier:
        description:
            - Peer address family type.
        choices:
            - ipv4
            - ipv6
    bfd_profile:
        description:
            - BFD profile configuration.
    connection_authentication:
        description:
            - BGP auth profile name.
    connection_hold_time:
        description:
            - Hold time (in seconds).
        type: int
    connection_idle_hold_time:
        description:
            - Idle hold time (in seconds).
        type: int
    connection_incoming_allow:
        description:
            - Allow incoming connections.
        type: bool
    connection_incoming_remote_port:
        description:
            - Restrict remote port for incoming BGP connections.
        type: int
    connection_keep_alive_interval:
        description:
            - Keep-alive interval (in seconds).
        type: int
    connection_min_route_adv_interval:
        description:
            - Minimum Route Advertisement Interval (in seconds).
        type: int
    connection_multihop:
        description:
            - IP TTL value used for sending BGP packet. set to 0 means eBGP use 2, iBGP use 255.
        type: int
    connection_open_delay_time:
        description:
            - Open delay time (in seconds).
        type: int
    connection_outgoing_allow:
        description:
            - Allow outgoing connections.
        type: bool
    connection_outgoing_local_port:
        description:
            - Use specific local port for outgoing BGP connections.
        type: int
    enable:
        description:
            - Enable BGP Peer.
        default: True
        type: bool
    enable_mp_bgp:
        description:
            - Enable MP-BGP extentions.
        type: bool
    enable_sender_side_loop_detection:
        description:
            - Enable sender side loop detection.
        type: bool
    local_interface:
        description:
            - Interface to accept BGP session.
    local_interface_ip:
        description:
            - Specify exact IP address if interface has multiple addresses.
    max_prefixes:
        description:
            - Maximum of prefixes to receive from peer.
        type: int
    name:
        description:
            - Name of BGP Peer.
        required: True
    peer_address_ip:
        description:
            - IP address of peer.
    peer_as:
        description:
            - Peer AS number.
    peer_group:
        description:
            - Name of the peer group; it must already exist; see panos_bgp_peer_group.
        required: True
    peering_type:
        description:
            - Peering type.
        choices:
            - unspecified
            - bilateral
    reflector_client:
        description:
            - Reflector client type.
        choices:
            - non-client
            - client
            - meshed-client
    subsequent_address_multicast:
        description:
            - Select SAFI for this peer.
        type: bool
    subsequent_address_unicast:
        description:
            - Select SAFI for this peer.
        type: bool
    vr_name:
        description:
            - Name of the virtual router; it must already exist; see panos_virtual_router.
        default: default
'''

EXAMPLES = '''
- name: Create BGP Peer
  panos_bgp_peer:
    provider: '{{ provider }}'
    peer_group: 'peer-group-1'
    name: 'peer-1'
    enable: true
    local_interface: 'ethernet1/1'
    local_interface_ip: '192.168.1.1'
    peer_address_ip: '10.1.1.1'
    peer_as: '64512'
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
    from pandevice.network import BgpPeerGroup
    from pandevice.network import BgpPeer
except ImportError:
    pass


def setup_args():
    return dict(
        name=dict(
            type='str', required=True,
            help='Name of BGP Peer'),
        enable=dict(
            default=True, type='bool',
            help='Enable BGP Peer'),
        peer_as=dict(
            type='str',
            help='Peer AS number'),
        enable_mp_bgp=dict(
            type='bool',
            help='Enable MP-BGP extentions'),
        address_family_identifier=dict(
            type='str', choices=['ipv4', 'ipv6'],
            help='Peer address family type'),
        subsequent_address_unicast=dict(
            type='bool',
            help='Select SAFI for this peer'),
        subsequent_address_multicast=dict(
            type='bool',
            help='Select SAFI for this peer'),
        local_interface=dict(
            type='str',
            help='Interface to accept BGP session'),
        local_interface_ip=dict(
            type='str',
            help='Specify exact IP address if interface has multiple addresses'),
        peer_address_ip=dict(
            type='str',
            help='IP address of peer'),
        connection_authentication=dict(
            type='str',
            help='BGP auth profile name'),
        connection_keep_alive_interval=dict(
            type='int',
            help='Keep-alive interval (in seconds)'),
        connection_min_route_adv_interval=dict(
            type='int',
            help='Minimum Route Advertisement Interval (in seconds)'),
        connection_multihop=dict(
            type='int',
            help='IP TTL value used for sending BGP packet. set to 0 means eBGP use 2, iBGP use 255'),
        connection_open_delay_time=dict(
            type='int',
            help='Open delay time (in seconds)'),
        connection_hold_time=dict(
            type='int',
            help='Hold time (in seconds)'),
        connection_idle_hold_time=dict(
            type='int',
            help='Idle hold time (in seconds)'),
        connection_incoming_allow=dict(
            type='bool',
            help='Allow incoming connections'),
        connection_outgoing_allow=dict(
            type='bool',
            help='Allow outgoing connections'),
        connection_incoming_remote_port=dict(
            type='int',
            help='Restrict remote port for incoming BGP connections'),
        connection_outgoing_local_port=dict(
            type='int',
            help='Use specific local port for outgoing BGP connections'),
        enable_sender_side_loop_detection=dict(
            type='bool',
            help='Enable sender side loop detection'),
        reflector_client=dict(
            type='str', choices=['non-client', 'client', 'meshed-client'],
            help='Reflector client type'),
        peering_type=dict(
            type='str', choices=['unspecified', 'bilateral'],
            help='Peering type'),
        # aggregated_confed_as_path=dict(
        #     type='bool',
        #     help='This peer understands aggregated confederation AS path'),
        max_prefixes=dict(
            type='int',
            help='Maximum of prefixes to receive from peer'),
        # max_orf_entries=dict(
        #     type='int',
        #     help='Maximum of ORF entries accepted from peer'),
        # soft_reset_with_stored_info=dict(
        #     type='bool',
        #     help='Enable soft reset with stored info'),
        bfd_profile=dict(
            type='str',
            help='BFD profile configuration'),

        peer_group=dict(
            required=True,
            help='Name of the peer group; it must already exist; see panos_bgp_peer_group'),
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

    # Verify libs, setup pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    vr = VirtualRouter(module.params['vr_name'])
    parent.add(vr)
    try:
        vr.refresh()
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    bgp = vr.find('', Bgp)
    if bgp is None:
        module.fail_json(msg='BGP is not configured for "{0}".'.format(vr.name))

    group = bgp.find(module.params['peer_group'], BgpPeerGroup)
    if group is None:
        module.fail_json(msg='BGP peer group does not exist: {0}.'.format(module.params['peer_group']))

    listing = group.findall(BgpPeer)
    spec = {
        'name': module.params['name'],
        'enable': module.params['enable'],
        'peer_as': module.params['peer_as'],
        'enable_mp_bgp': module.params['enable_mp_bgp'],
        'address_family_identifier': module.params['address_family_identifier'],
        'subsequent_address_unicast': module.params['subsequent_address_unicast'],
        'subsequent_address_multicast': module.params['subsequent_address_multicast'],
        'local_interface': module.params['local_interface'],
        'local_interface_ip': module.params['local_interface_ip'],
        'peer_address_ip': module.params['peer_address_ip'],
        'connection_authentication': module.params['connection_authentication'],
        'connection_keep_alive_interval': module.params['connection_keep_alive_interval'],
        'connection_min_route_adv_interval': module.params['connection_min_route_adv_interval'],
        'connection_multihop': module.params['connection_multihop'],
        'connection_open_delay_time': module.params['connection_open_delay_time'],
        'connection_hold_time': module.params['connection_hold_time'],
        'connection_idle_hold_time': module.params['connection_idle_hold_time'],
        'connection_incoming_allow': module.params['connection_incoming_allow'],
        'connection_outgoing_allow': module.params['connection_outgoing_allow'],
        'connection_incoming_remote_port': module.params['connection_incoming_remote_port'],
        'connection_outgoing_local_port': module.params['connection_outgoing_local_port'],
        'enable_sender_side_loop_detection': module.params['enable_sender_side_loop_detection'],
        'reflector_client': module.params['reflector_client'],
        'peering_type': module.params['peering_type'],
        'max_prefixes': module.params['max_prefixes'],
        'bfd_profile': module.params['bfd_profile'],
    }
    obj = BgpPeer(**spec)
    group.add(obj)

    changed, diff = helper.apply_state(obj, listing, module)

    if changed and module.params['commit']:
        helper.commit(module)

    module.exit_json(changed=changed, diff=diff, msg='done')


if __name__ == '__main__':
    main()
