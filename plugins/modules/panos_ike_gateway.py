#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2017 Palo Alto Networks, Inc
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
module: panos_ike_gateway
short_description: Manage IKE gateway on the firewall with subset of settings.
description:
    - Use this to manage or define a gateway, including the configuration information
      necessary to perform Internet Key Exchange (IKE) protocol negotiation with a
      peer gateway. This is the Phase 1 portion of the IKE/IPSec VPN setup.
author: "Ivan Bojer (@ivanbojer)"
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
    - paloaltonetworks.panos.fragments.full_template_support
    - paloaltonetworks.panos.fragments.deprecated_commit
options:
    name:
        description:
            - Name for the profile.
        type: str
    version:
        description:
            - Specify the priority for Diffie-Hellman (DH) groups.
        type: str
        default: 'ikev2'
        choices:
            - ikev1
            - ikev2
            - ikev2-preferred
        aliases:
            - protocol_version
    interface:
        description:
            - Specify the outgoing firewall interface to the VPN tunnel.
        type: str
        default: 'ethernet1/1'
    enable_passive_mode:
        description:
            - True to have the firewall only respond to IKE connections and never initiate them.
        type: bool
        default: True
        aliases:
            - passive_mode
    enable_nat_traversal:
        description:
            - True to NAT Traversal mode
        type: bool
        default: False
        aliases:
            - nat_traversal
    enable_fragmentation:
        description:
            - True to enable IKE fragmentation
            - Incompatible with pre-shared keys, or 'aggressive' exchange mode
        type: bool
        default: False
        aliases:
            - fragmentation
    enable_liveness_check:
        description:
            - Enable sending empty information liveness check message.
        type: bool
        default: True
    liveness_check_interval:
        description:
            - Delay interval before sending probing packets (in seconds).
        type: int
        default: 5
        aliases:
            - liveness_check
    peer_ip_type:
        description:
            - IP or dynamic.
        type: str
        default: ip
        choices: ['ip', 'dynamic', 'fqdn']
    peer_ip_value:
        description:
            - IPv4 address of the peer gateway.
        type: str
        default: '127.0.0.1'
    enable_dead_peer_detection:
        description:
            - True to enable Dead Peer Detection on the gateway.
        type: bool
        default: false
        aliases:
            - dead_peer_detection
    dead_peer_detection_interval:
        description:
            - Time in seconds to check for a dead peer.
        type: int
        default: 99
    dead_peer_detection_retry:
        description:
            - Retry attempts before peer is marked dead.
        type: int
        default: 10
    local_ip_address:
        description:
            - Bind IKE gateway to the specified interface IP address.  Only needed if
              'interface' has multiple IP addresses associated with it.
            - It should include the mask, such as '192.168.1.1/24'
        type: str
    local_ip_address_type:
        description:
            - The type of the bound interface IP address.
            - "ip: Specify exact IP address if interface has multiple addresses."
            - "floating-ip: Floating IP address in HA Active-Active configuration."
            - Required when 'local_ip_address' is set.
        type: str
        choices: ['ip', 'floating-ip']
    pre_shared_key:
        description:
            - Specify pre-shared key.
        type: str
        default: 'CHANGEME'
        aliases:
            - psk
    local_id_type:
        description:
            - Define the format of the identification of the local gateway.
            - "ipaddr: IP address"
            - "fqdn: FQDN (hostname)"
            - "ufqdn: User FQDN (email address)"
            - "keyid: Key ID (binary format ID string in hex)"
        type: str
        choices: ['ipaddr', 'fqdn', 'ufqdn', 'keyid', 'dn']
    local_id_value:
        description:
            - Define the value for the identification of the local gateway.
            - Required when I(local_id_type) is set.
        type: str
    peer_id_type:
        description:
            - Define the format of the identification of the peer gateway.
            - "ipaddr: IP address"
            - "fqdn: FQDN (hostname)"
            - "ufqdn: User FQDN (email address)"
            - "keyid: Key ID (binary format ID string in hex)"
        type: str
        choices: ['ipaddr', 'fqdn', 'ufqdn', 'keyid', 'dn']
    peer_id_value:
        description:
            - Define the value for the identification of the peer gateway.
            - Required when I(peer_id_type) is set.
        type: str
    peer_id_check:
        description:
            - Type of checking to do on peer_id.
        type: str
        choices: ['exact', 'wildcard']
    ikev1_crypto_profile:
        description:
            - Crypto profile for IKEv1.
        type: str
        default: 'default'
    ikev1_exchange_mode:
        description:
            - The IKE exchange mode to use
        type: str
        choices:
            - auto
            - main
            - aggressive
    ikev2_crypto_profile:
        description:
            - Crypto profile for IKEv2.
        type: str
        default: 'default'
"""

EXAMPLES = """
- name: Add IKE gateway config to the firewall
  paloaltonetworks.panos.panos_ike_gateway:
    provider: '{{ provider }}'
    state: 'present'
    name: 'IKEGW-Ansible'
    version: 'ikev2'
    interface: 'ethernet1/1'
    enable_passive_mode: true
    enable_liveness_check: true
    liveness_check_interval: '5'
    peer_ip_value: '1.2.3.4'
    pre_shared_key: 'CHANGEME'
    ikev2_crypto_profile: 'IKE-Ansible'
    commit: false

- name: Create IKE gateway (dynamic)
  paloaltonetworks.panos.panos_ike_gateway:
    provider: '{{ device }}'
    name: 'test-dynamic'
    interface: 'ethernet1/1'
    peer_ip_type: dynamic
    pre_shared_key: 'CHANGEME'
    commit: false
"""

RETURN = """
# Default return values
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    ConnectionHelper,
    get_connection,
)


class Helper(ConnectionHelper):
    def spec_handling(self, spec, module):
        spec["auth_type"] = "pre-shared-key"

        # Remove the IKEv1 crypto profile if we're doing IKEv2.
        if spec["version"] == "ikev2":
            spec["ikev1_crypto_profile"] = None

        # Remove the IKEv2 crypto profile if we're doing IKEv1.
        if spec["version"] == "ikev1":
            spec["ikev2_crypto_profile"] = None


def main():
    helper = get_connection(
        helper_cls=Helper,
        template=True,
        template_stack=True,
        with_classic_provider_spec=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        with_commit=True,
        sdk_cls=("network", "IkeGateway"),
        sdk_params=dict(
            name=dict(required=True),
            version=dict(
                default="ikev2",
                choices=["ikev1", "ikev2", "ikev2-preferred"],
                aliases=["protocol_version"],
            ),
            interface=dict(default="ethernet1/1"),
            local_ip_address_type=dict(default=None, choices=["ip", "floating-ip"]),
            local_ip_address=dict(default=None),
            enable_passive_mode=dict(
                type="bool", default=True, aliases=["passive_mode"]
            ),
            enable_nat_traversal=dict(
                type="bool", default=False, aliases=["nat_traversal"]
            ),
            enable_fragmentation=dict(
                type="bool", default=False, aliases=["fragmentation"]
            ),
            enable_liveness_check=dict(type="bool", default=True),
            liveness_check_interval=dict(
                type="int", default=5, aliases=["liveness_check"]
            ),
            peer_ip_type=dict(default="ip", choices=["ip", "dynamic", "fqdn"]),
            peer_ip_value=dict(default="127.0.0.1"),
            enable_dead_peer_detection=dict(
                type="bool", default=False, aliases=["dead_peer_detection"]
            ),
            dead_peer_detection_interval=dict(type="int", default=99),
            dead_peer_detection_retry=dict(type="int", default=10),
            pre_shared_key=dict(no_log=True, default="CHANGEME", aliases=["psk"]),
            local_id_type=dict(
                default=None, choices=["ipaddr", "fqdn", "ufqdn", "keyid", "dn"]
            ),
            local_id_value=dict(default=None),
            peer_id_type=dict(
                default=None, choices=["ipaddr", "fqdn", "ufqdn", "keyid", "dn"]
            ),
            peer_id_value=dict(default=None),
            peer_id_check=dict(choices=["exact", "wildcard"]),
            ikev1_crypto_profile=dict(default="default"),
            ikev1_exchange_mode=dict(
                default=None, choices=["auto", "main", "aggressive"]
            ),
            ikev2_crypto_profile=dict(default="default"),
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
