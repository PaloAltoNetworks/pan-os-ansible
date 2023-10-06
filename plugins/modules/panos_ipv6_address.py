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

DOCUMENTATION = """
---
module: panos_ipv6_address
short_description: Manage IPv6 addresses on an interface.
description:
    - Manage IPv6 addresses on an interface.
author: "Garfield Lee Freeman (@shinmog)"
version_added: '1.1.0'
requirements:
    - pan-python
    - pandevice >= 0.14.0
notes:
    - Panorama is supported.
    - Checkmode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
    - paloaltonetworks.panos.fragments.template_only
options:
    iface_name:
        description:
            - The parent interface that this IPv6 address is attached to.
        type: str
        required: true
    address:
        description:
            - IPv6 address.
        type: str
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
"""

EXAMPLES = """
# Have an IPv6 address on ethernet1/6.2
- name: Assert the given IPv6 address
  paloaltonetworks.panos.panos_ipv6_address:
    provider: '{{ provider }}'
    iface_name: 'ethernet1/6.2'
    address: '2001:db8:123:1::1'
"""

RETURN = """
# Default return values
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    ConnectionHelper,
    get_connection,
    to_sdk_cls,
)


class Helper(ConnectionHelper):
    def parent_handling(self, parent, module):
        iname = module.params["iface_name"]
        part = iname.split(".")[0]

        checks = (
            ("EthernetInterface", "ethernet", True),
            ("AggregateInterface", "ae", True),
            ("LoopbackInterface", "loopback", False),
            ("TunnelInterface", "tunnel", False),
            ("VlanInterface", "vlan", False),
        )

        for cls_name, prefix, should_check_name in checks:
            if part.startswith(prefix):
                eth = to_sdk_cls("network", cls_name)(part)
                parent.add(eth)
                if not should_check_name or "." not in iname:
                    return eth

                sub = to_sdk_cls("network", "Layer3Subinterface")(iname)
                eth.add(sub)
                return sub

        module.fail_json(msg="Unknown interface style: {0}".format(iname))


def main():
    helper = get_connection(
        helper_cls=Helper,
        template=True,
        with_classic_provider_spec=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        min_pandevice_version=(0, 14, 0),
        sdk_cls=("network", "IPv6Address"),
        sdk_params=dict(
            address=dict(required=True),
            enable_on_interface=dict(type="bool", default=True),
            prefix=dict(type="bool"),
            anycast=dict(type="bool"),
            advertise_enabled=dict(type="bool"),
            valid_lifetime=dict(type="int", default=2592000),
            preferred_lifetime=dict(type="int", default=604800),
            onlink_flag=dict(type="bool", default=True),
            auto_config_flag=dict(type="bool", default=True),
        ),
        extra_params=dict(
            iface_name=dict(required=True),
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
