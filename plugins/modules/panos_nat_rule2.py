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
module: panos_nat_rule2
short_description: Manage a NAT rule
description:
    - Manage a policy NAT rule.
    - NOTE Even though this module supports I(state=merged), due to the
      complexity of the XML schema for NAT rules, changing a NAT rule's types
      using I(state=merged) will likely result in an error.  Using I(state=merged)
      will work as normal for simple operations, such as adding additional IP addresses
      to any of the listings or changing simple variable types.
author:
    - Garfield Lee Freeman (@shinmog)
version_added: '2.10.0'
requirements:
    - pan-python >= 0.16
    - pan-os-python >= 1.7.3
notes:
    - Checkmode is supported.
    - Panorama is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
    - paloaltonetworks.panos.fragments.device_group
    - paloaltonetworks.panos.fragments.vsys
    - paloaltonetworks.panos.fragments.rulebase
    - paloaltonetworks.panos.fragments.uuid
    - paloaltonetworks.panos.fragments.target
    - paloaltonetworks.panos.fragments.movement
    - paloaltonetworks.panos.fragments.audit_comment
options:
    name:
        description:
            - Name of the rule.
        type: str
    description:
        description:
            - The description.
        type: str
    nat_type:
        description:
            - Type of NAT.
        type: str
        choices:
            - ipv4
            - nat64
            - nptv6
        default: ipv4
    from_zones:
        description:
            - From zones.
        type: list
        elements: str
    to_zones:
        description:
            - To zones.
            - Note that there should only be one element in this list.
        type: list
        elements: str
    to_interface:
        description:
            - Egress interface from route lookup.
        type: str
    service:
        description:
            - The service.
        type: str
    source_addresses:
        description:
            - Source addresses.
            - When referencing predefined EDLs, use config names of the EDLS not
              their full names. The config names can be found with the CLI...
              request system external-list show type predefined-ip name <tab>
                panw-bulletproof-ip-list   panw-bulletproof-ip-list
                panw-highrisk-ip-list      panw-highrisk-ip-list
                panw-known-ip-list         panw-known-ip-list
                panw-torexit-ip-list       panw-torexit-ip-list
        type: list
        elements: str
    destination_addresses:
        description:
            - Destination addresses.
            - When referencing predefined EDLs, use config names of the EDLS not
              their full names. The config names can be found with the CLI...
              request system external-list show type predefined-ip name <tab>
                panw-bulletproof-ip-list   panw-bulletproof-ip-list
                panw-highrisk-ip-list      panw-highrisk-ip-list
                panw-known-ip-list         panw-known-ip-list
                panw-torexit-ip-list       panw-torexit-ip-list
        type: list
        elements: str
    source_translation_type:
        description:
            - Type of source address translation.
        type: str
        choices:
            - 'dynamic-ip-and-port'
            - 'dynamic-ip'
            - 'static-ip'
    source_translation_address_type:
        description:
            - For I(source_translation_type=dynamic-ip-and-port) or or I(source_translation_type=dynamic-ip).
            - Address type.
        type: str
        choices:
            - interface-address
            - translated-address
    source_translation_interface:
        description:
            - For I(source_translation_address_type=interface-address).
            - Interface of the source address.
        type: str
    source_translation_ip_address:
        description:
            - For I(source_translation_address_type=interface-address).
            - IP address of the source address translation.
        type: str
    source_translation_translated_addresses:
        description:
            - For I(source_translation_address_type=translated-address).
            - Translated addresses of the source address translation.
        type: list
        elements: str
    source_translation_fallback_type:
        description:
            - For I(source_translation_type=dynamic-ip).
            - Type of fallback for dynamic IP source translation.
        type: str
        choices:
            - translated-address
            - interface-address
    source_translation_fallback_translated_addresses:
        description:
            - For I(source_translation_fallback_type=translated-address).
            - Addresses for translated address types of fallback source translation.
        type: list
        elements: str
    source_translation_fallback_interface:
        description:
            - For I(source_translation_fallback_type=interface-address).
            - The interface for the fallback source translation.
        type: str
    source_translation_fallback_ip_type:
        description:
            - For I(source_translation_fallback_type=interface-address).
            - The type of the IP address for the fallback source translation IP address.
        choices:
            - ip
            - floating-ip
        type: str
    source_translation_fallback_ip_address:
        description:
            - For I(source_translation_fallback_type=interface-address).
            - The IP address of the fallback source translation.
        type: str
    source_translation_static_translated_address:
        description:
            - For I(source_translation_type=static-ip).
            - The IP address for the static source translation.
        type: str
    source_translation_static_bi_directional:
        description:
            - For I(source_translation_type=static-ip).
            - Allow reverse translation from translated address to original address.
        type: bool
    destination_translated_address:
        description:
            - Static translated destination IP address.
        type: str
    destination_translated_port:
        description:
            - Static translated destination port number.
        type: int
    ha_binding:
        description:
            - Device binding configuration in HA Active-Active mode.
        choices:
            - primary
            - both
            - '0'
            - '1'
        type: str
    disabled:
        description:
            - Rule is disabled or not.
        type: bool
    tags:
        description:
            - Administrative tags.
        type: list
        elements: str
    destination_dynamic_translated_address:
        description:
            - For PAN-OS 8.1 and above.
            - Dynamic destination translated address.
        type: str
    destination_dynamic_translated_port:
        description:
            - For PAN-OS 8.1 and above.
            - Dynamic destination translated port.
        type: int
    destination_dynamic_translated_distribution:
        description:
            - For PAN-OS 8.1 and above.
            - Dynamic destination translated distribution.
        type: str
    group_tag:
        description:
            - For PAN-OS 9.0 and above.
            - The group tag.
        type: str
"""

EXAMPLES = """
- name: add a nat rule
  paloaltonetworks.panos.panos_nat_rule2:
    provider: '{{ provider }}'
    name: 'myRule'
    description: 'Made by Ansible'
    nat_type: 'ipv4'
    from_zones: ['Trust-L3']
    to_zones: ['Untrusted-L3']
    to_interface: 'ethernet1/1'
    service: 'any'
    source_addresses: ['any']
    destination_addresses: ['any']
    source_translation_type: 'dynamic-ip-and-port'
    source_translation_address_type: 'interface-address'
    source_translation_interface: 'ethernet1/1'
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
        vsys=True,
        device_group=True,
        rulebase=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        with_classic_provider_spec=True,
        error_on_firewall_shared=True,
        min_pandevice_version=(1, 7, 3),
        with_uuid=True,
        with_target=True,
        with_movement=True,
        with_audit_comment=True,
        sdk_cls=("policies", "NatRule"),
        sdk_params=dict(
            name=dict(required=True),
            description=dict(),
            nat_type=dict(default="ipv4", choices=["ipv4", "nat64", "nptv6"]),
            from_zones=dict(type="list", elements="str", sdk_param="fromzone"),
            to_zones=dict(type="list", elements="str", sdk_param="tozone"),
            to_interface=dict(),
            service=dict(),
            source_addresses=dict(type="list", elements="str", sdk_param="source"),
            destination_addresses=dict(
                type="list", elements="str", sdk_param="destination"
            ),
            source_translation_type=dict(
                choices=["dynamic-ip-and-port", "dynamic-ip", "static-ip"]
            ),
            source_translation_address_type=dict(
                choices=["interface-address", "translated-address"]
            ),
            source_translation_interface=dict(),
            source_translation_ip_address=dict(),
            source_translation_translated_addresses=dict(type="list", elements="str"),
            source_translation_fallback_type=dict(
                choices=["translated-address", "interface-address"]
            ),
            source_translation_fallback_translated_addresses=dict(
                type="list", elements="str"
            ),
            source_translation_fallback_interface=dict(),
            source_translation_fallback_ip_type=dict(choices=["ip", "floating-ip"]),
            source_translation_fallback_ip_address=dict(),
            source_translation_static_translated_address=dict(),
            source_translation_static_bi_directional=dict(type="bool"),
            destination_translated_address=dict(),
            destination_translated_port=dict(type="int"),
            ha_binding=dict(type="str", choices=["primary", "both", "0", "1"]),
            disabled=dict(type="bool"),
            tags=dict(type="list", elements="str", sdk_param="tag"),
            destination_dynamic_translated_address=dict(),
            destination_dynamic_translated_port=dict(type="int"),
            destination_dynamic_translated_distribution=dict(),
            group_tag=dict(),
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
