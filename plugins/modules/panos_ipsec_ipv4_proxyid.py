#!/usr/bin/python
# -*- coding: utf-8 -*-

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

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: panos_ipsec_ipv4_proxyid
short_description: Manage IPv4 Proxy Id on an IPSec Tunnel
description:
    - Manage IPv4 Proxy Id on an IPSec tunnel
author: "Heiko Burghardt (@odysseus107)"
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
            - The Proxy ID
        type: str
    tunnel_name:
        description:
            - IPSec Tunnel Name
        type: str
        default: 'default'
    local:
        description:
            - IP subnet or IP address represents the local network
        type: str
        default: '192.168.2.0/24'
    remote:
        description:
            - IP subnet or IP address represents the remote network
        type: str
        default: '192.168.1.0/24'
    any_protocol:
        description:
            - Any protocol boolean. If this parameter is set to `true`, the `number_proto` parameter must not be specified.
        type: bool
        default: True
    number_proto:
        description:
            - Numbered Protocol; protocol number (1-254). This parameter must be specified if `any_protocol` is set to `false`.
        type: int
    tcp_local_port:
        description:
            - (Protocol TCP) local port
        type: int
    tcp_remote_port:
        description:
            - (Protocol TCP) remote port
        type: int
    udp_local_port:
        description:
            - (Protocol UDP) local port
        type: int
    udp_remote_port:
        description:
            - (Protocol UDP) remote port
        type: int
"""

EXAMPLES = """
- name: Add IPSec IPv4 Proxy ID
  paloaltonetworks.panos.panos_ipsec_ipv4_proxyid:
    provider: '{{ provider }}'
    name: 'IPSec-ProxyId'
    tunnel_name: 'Default_Tunnel'
    local: '192.168.2.0/24'
    remote: '192.168.1.0/24'
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
        with_classic_provider_spec=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        with_commit=True,
        parents=(("network", "IpsecTunnel", "tunnel_name", "default"),),
        sdk_cls=("network", "IpsecTunnelIpv4ProxyId"),
        sdk_params=dict(
            name=dict(type="str", required=True),
            local=dict(default="192.168.2.0/24"),
            remote=dict(default="192.168.1.0/24"),
            any_protocol=dict(type="bool", default=True),
            number_proto=dict(type="int", sdk_param="number_protocol"),
            tcp_local_port=dict(type="int"),
            tcp_remote_port=dict(type="int"),
            udp_local_port=dict(type="int"),
            udp_remote_port=dict(type="int"),
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
