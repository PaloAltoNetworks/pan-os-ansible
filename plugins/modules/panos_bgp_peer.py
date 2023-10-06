#!/usr/bin/python
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

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: panos_bgp_peer
short_description: Manage a BGP Peer
description:
    - Use BGP to publish and consume routes from disparate networks.
author:
    - Joshua Colson (@freakinhippie)
    - Garfield Lee Freeman (@shinmog)
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is supported.
    - Panorama is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.full_template_support
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.deprecated_commit
    - paloaltonetworks.panos.fragments.gathered_filter
options:
    address_family_identifier:
        description:
            - Peer address family type.
        type: str
        choices:
            - ipv4
            - ipv6
    bfd_profile:
        description:
            - BFD profile configuration.
        type: str
    connection_authentication:
        description:
            - BGP auth profile name.
        type: str
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
        type: str
    local_interface_ip:
        description:
            - Specify exact IP address if interface has multiple addresses.
        type: str
    max_prefixes:
        description:
            - Maximum of prefixes to receive from peer.
        type: int
    name:
        description:
            - Name of BGP Peer.
        type: str
    peer_address_ip:
        description:
            - IP address of peer.
        type: str
    peer_as:
        description:
            - Peer AS number.
        type: str
    peer_group:
        description:
            - Name of the peer group; it must already exist; see M(paloaltonetworks.panos.panos_bgp_peer_group).
        type: str
        required: true
    peering_type:
        description:
            - Peering type.
        type: str
        choices:
            - unspecified
            - bilateral
    reflector_client:
        description:
            - Reflector client type.
        type: str
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
            - Name of the virtual router; it must already exist; see M(paloaltonetworks.panos.panos_virtual_router).
        type: str
        default: default
"""

EXAMPLES = """
- name: Create BGP Peer
  paloaltonetworks.panos.panos_bgp_peer:
    provider: '{{ provider }}'
    peer_group: 'peer-group-1'
    name: 'peer-1'
    enable: true
    local_interface: 'ethernet1/1'
    local_interface_ip: '192.168.1.1'
    peer_address_ip: '10.1.1.1'
    peer_as: '64512'
    commit: true
"""

RETURN = """
# Default return values
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    get_connection,
)


def main():
    helper = get_connection(
        template=True,
        template_stack=True,
        with_network_resource_module_state=True,
        with_classic_provider_spec=True,
        with_commit=True,
        with_gathered_filter=True,
        parents=(
            ("network", "VirtualRouter", "vr_name", "default"),
            ("network", "Bgp", None),
            ("network", "BgpPeerGroup", "peer_group"),
        ),
        sdk_cls=("network", "BgpPeer"),
        sdk_params=dict(
            name=dict(required=True),
            enable=dict(default=True, type="bool"),
            peer_as=dict(),
            enable_mp_bgp=dict(type="bool"),
            address_family_identifier=dict(choices=["ipv4", "ipv6"]),
            subsequent_address_unicast=dict(type="bool"),
            subsequent_address_multicast=dict(type="bool"),
            local_interface=dict(),
            local_interface_ip=dict(),
            peer_address_ip=dict(),
            connection_authentication=dict(),
            connection_keep_alive_interval=dict(type="int"),
            connection_min_route_adv_interval=dict(type="int"),
            connection_multihop=dict(type="int"),
            connection_open_delay_time=dict(type="int"),
            connection_hold_time=dict(type="int"),
            connection_idle_hold_time=dict(type="int"),
            connection_incoming_allow=dict(type="bool"),
            connection_outgoing_allow=dict(type="bool"),
            connection_incoming_remote_port=dict(type="int"),
            connection_outgoing_local_port=dict(type="int"),
            enable_sender_side_loop_detection=dict(type="bool"),
            reflector_client=dict(choices=["non-client", "client", "meshed-client"]),
            peering_type=dict(choices=["unspecified", "bilateral"]),
            max_prefixes=dict(type="int"),
            bfd_profile=dict(),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    helper.process(module)


if __name__ == "__main__":
    main()
