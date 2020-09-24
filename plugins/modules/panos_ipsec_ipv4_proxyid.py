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

DOCUMENTATION = '''
---
module: panos_ipsec_ipv4_proxyid
short_description: Configures IPv4 Proxy Id on an IPSec Tunnel
description:
    - Configures IPv4 Proxy Id on an IPSec tunnel
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
    - paloaltonetworks.panos.fragments.state
    - paloaltonetworks.panos.fragments.full_template_support
    - paloaltonetworks.panos.fragments.deprecated_commit
options:
    name:
        description:
            - The Proxy ID
        type: str
        required: true
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
            - Any protocol boolean
        type: bool
        default: True
    number_proto:
        description:
            - Numbered Protocol; protocol number (1-254)
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
'''

EXAMPLES = '''
- name: Add IPSec IPv4 Proxy ID
  panos_ipsec_ipv4_proxyid:
    provider: '{{ provider }}'
    name: 'IPSec-ProxyId'
    tunnel_name: 'Default_Tunnel'
    local: '192.168.2.0/24'
    remote: '192.168.1.0/24'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from panos.network import IpsecTunnel
    from panos.network import IpsecTunnelIpv4ProxyId
    from panos.errors import PanDeviceError
except ImportError:
    try:
        from pandevice.network import IpsecTunnel
        from pandevice.network import IpsecTunnelIpv4ProxyId
        from pandevice.errors import PanDeviceError
    except ImportError:
        pass


def main():
    helper = get_connection(
        template=True,
        template_stack=True,
        with_classic_provider_spec=True,
        with_state=True,
        argument_spec=dict(
            name=dict(type='str', required=True),
            tunnel_name=dict(default='default'),
            local=dict(default='192.168.2.0/24'),
            remote=dict(default='192.168.1.0/24'),
            any_protocol=dict(type='bool', default=True),
            number_proto=dict(type='int'),
            tcp_local_port=dict(type='int'),
            tcp_remote_port=dict(type='int'),
            udp_local_port=dict(type='int'),
            udp_remote_port=dict(type='int'),
            commit=dict(type='bool', default=False),
        )
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of
    )

    # Object specifications
    spec = {
        'name': module.params['name'],
        'local': module.params['local'],
        'remote': module.params['remote'],
        'any_protocol': module.params['any_protocol'],
        'number_protocol': module.params['number_proto'],
        'tcp_local_port': module.params['tcp_local_port'],
        'tcp_remote_port': module.params['tcp_remote_port'],
        'udp_local_port': module.params['udp_local_port'],
        'udp_remote_port': module.params['udp_remote_port'],
    }

    # Additional infos
    commit = module.params['commit']

    # Verify libs are present, get parent object.
    parent = helper.get_pandevice_parent(module)
    tunnel_name = module.params['tunnel_name']

    # get the tunnel object
    tunnel = IpsecTunnel(tunnel_name)
    parent.add(tunnel)
    try:
        tunnel.refresh()
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    # get the listing
    listing = tunnel.findall(IpsecTunnelIpv4ProxyId)
    obj = IpsecTunnelIpv4ProxyId(**spec)
    tunnel.add(obj)

    # Apply the state.
    changed, diff = helper.apply_state(obj, listing, module)

    # Commit.
    if commit and changed:
        helper.commit(module)

    # Done.
    module.exit_json(changed=changed, diff=diff)


if __name__ == '__main__':
    main()
