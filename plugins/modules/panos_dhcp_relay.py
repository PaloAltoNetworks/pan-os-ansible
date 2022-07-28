#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2022 Palo Alto Networks, Inc
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
module: panos_dhcp_relay
short_description: Configure dhcp relay
description:
    - Configure dhcp relay on PAN-OS firewall or in Panorama template.
author:
    - Sean O'Brien (@undodelete)
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
    - pandevice >= 0.8.0
notes:
    - Panorama is not supported.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.state
    - paloaltonetworks.panos.fragments.vsys
options:
    interface:
        description: Name of the security zone to configure.
        type: str
        required: true
    ipv4_servers:
        description:
            - List of IPv6 DHCP Servers
        type: list
        elements: str
    ipv4_enabled:
        description:
            - Enabled IPv4 on DHCP Relay
        type: str
        choices: ['yes', 'no']
        default: 'yes'
    ipv6_servers:
        description:
            - List of IPv6 DHCP Servers
        type: list
        elements: str
    ipv6_enabled:
        description:
            - Enabled IPv6 on DHCP Relay
        type: str
        choices: ['yes', 'no']
"""

EXAMPLES = """
# Create IPv4 DHCP Relay
- panos_dhcp_relay:
    provider: '{{ provider }}'
    interface: 'ethernet1/1'
    ipv4_servers:
      - '1.1.1.1'
      - '2.2.2.2'

# Create IPv6 DHCP Relay
- panos_dhcp_relay:
    provider: '{{ provider }}'
    interface: 'ethernet1/1'
    ipv4_enabled: 'no'
    ipv6_enabled: 'yes'
    ipv6_servers:
      - 2001:0db8:85a3:0000:0000:8a2e:0370:7334
      - 2001:0db8:85a3:0000:0000:8a2e:0370:7331

# Delete DHCP Relay
- panos_dhcp_relay:
    provider: '{{ provider }}'
    interface: 'ethernet1/1'
    state: absent
"""

RETURN = """
# Default return values
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    get_connection,
)

try:
    from panos.errors import PanDeviceError
    from panos.network import Dhcp, DhcpRelay, DhcpRelayIpv6Address
except ImportError:
    try:
        from pandevice.errors import PanDeviceError
        from pandevice.network import Dhcp, DhcpRelay, DhcpRelayIpv6Address
    except ImportError:
        pass


def main():
    helper = get_connection(
        vsys=True,
        with_state=True,
        with_classic_provider_spec=True,
        argument_spec=dict(
            interface=dict(type="str", required=True),
            ipv4_servers=dict(type="list", elements="str"),
            ipv4_enabled=dict(type="str", default="yes", choices=['yes', 'no']),
            ipv6_servers=dict(type="list", elements="str"),
            ipv6_enabled=dict(type="str", choices=['yes', 'no']),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    parent = helper.get_pandevice_parent(module)

    state = module.params["state"]
    interface = module.params["interface"]
    ipv4_servers = module.params["ipv4_servers"]
    ipv4_enabled = module.params["ipv4_enabled"]
    ipv6_servers = module.params["ipv6_servers"]
    ipv6_enabled = module.params["ipv6_enabled"]

    if ipv6_enabled and ipv6_servers is None:
        module.fail_json(msg="Ipv6 constraint failed : at least one server needs to be configured to use 'ipv6_enabled'")
    if state == "present" and ipv4_servers is None:
        module.fail_json(msg="Create server constraint failed : at least one server needs to be configured in 'ipv4_servers'")

    try:
        existing_dhcp_relay = Dhcp.refreshall(parent)
    except PanDeviceError as e:
        module.fail_json(msg="Failed refresh: {0}".format(e))

    dhcp_object = Dhcp(interface)

    if state == "present":
        relay_object = DhcpRelay(
            name=interface,
            servers=ipv4_servers,
            enabled=ipv4_enabled,
            ipv6_enabled=ipv6_enabled
        )

        if ipv6_servers:
            for ipv6_server in ipv6_servers:
                relay_ipv6_object = DhcpRelayIpv6Address(name=ipv6_server, interface=interface)
                relay_object.add(relay_ipv6_object)

        dhcp_object.add(relay_object)

    parent.add(dhcp_object)

    changed, diff = helper.apply_state(dhcp_object, existing_dhcp_relay, module)

    module.exit_json(changed=changed, diff=diff)


if __name__ == "__main__":
    main()
