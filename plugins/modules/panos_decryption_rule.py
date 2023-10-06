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
module: panos_decryption_rule
short_description: Manage a decryption rule on PAN-OS.
description:
    - This module works for PAN-OS 7.0 and above.
    - Allows for the management of decryption rules on PAN-OS.
author:
    - Garfield Lee Freeman (@shinmog)
version_added: '2.10.0'
requirements:
    - pan-python >= 0.17
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
            - The rule description.
        type: str
    source_zones:
        description:
            - List of source zones.
        type: list
        elements: str
    source_addresses:
        description:
            - List of source addresses.
            - This can be an IP address, an address object/group, etc.
            - When referencing predefined EDLs, use config names of the EDLS not
              their full names. The config names can be found with the CLI...
              request system external-list show type predefined-ip name <tab>
                panw-bulletproof-ip-list   panw-bulletproof-ip-list
                panw-highrisk-ip-list      panw-highrisk-ip-list
                panw-known-ip-list         panw-known-ip-list
                panw-torexit-ip-list       panw-torexit-ip-list
        type: list
        elements: str
    negate_source:
        description:
            - Negate the source addresses.
        type: bool
    source_users:
        description:
            - The source users.
        type: list
        elements: str
    source_hip:
        description:
            - The source HIP info.
        type: list
        elements: str
    destination_zones:
        description:
            - List of destination zones.
        type: list
        elements: str
    destination_addresses:
        description:
            - List of destination addresses.
            - This can be an IP address, an address object/group, etc.
            - When referencing predefined EDLs, use config names of the EDLS not
              their full names. The config names can be found with the CLI...
              request system external-list show type predefined-ip name <tab>
                panw-bulletproof-ip-list   panw-bulletproof-ip-list
                panw-highrisk-ip-list      panw-highrisk-ip-list
                panw-known-ip-list         panw-known-ip-list
                panw-torexit-ip-list       panw-torexit-ip-list
        type: list
        elements: str
    negate_destination:
        description:
            - Negate the destination addresses.
        type: bool
    destination_hip:
        description:
            - The source HIP info.
        type: list
        elements: str
    tags:
        description:
            - The administrative tags.
        type: list
        elements: str
    disabled:
        description:
            - Rule is disabled or not.
        type: bool
    services:
        description:
            - List of services.
        type: list
        elements: str
    url_categories:
        description:
            - List of URL categories.
            - When referencing predefined EDLs, use config names of the EDLS not
              their full names. The config names can be found with the CLI...
              request system external-list show type predefined-url name <tab>
                panw-auth-portal-exclude-list   panw-auth-portal-exclude-list
        type: list
        elements: str
    action:
        description:
            - The action.
        type: str
        default: 'no-decrypt'
        choices:
            - "no-decrypt"
            - "decrypt"
            - "decrypt-and-forward"
    decryption_type:
        description:
            - The decryption type.
        type: str
        choices:
            - "ssl-forward-proxy"
            - "ssh-proxy"
            - "ssl-inbound-inspection"
    ssl_certificate:
        description:
            - The SSL certificate.
        type: str
    decryption_profile:
        description:
            - The decryption profile.
        type: str
    forwarding_profile:
        description:
            - The forwarding profile.
        type: str
    group_tag:
        description:
            - PAN-OS 9.0 and above.
            - The group tag.
        type: str
    log_successful_tls_handshakes:
        description:
            - PAN-OS 10.0 and above.
            - Log successful TLS handshakes.
        type: bool
    log_failed_tls_handshakes:
        description:
            - PAN-OS 10.0 and above.
            - Log failed TLS handshakes.
        type: bool
    log_setting:
        description:
            - PAN-OS 10.0 and above.
            - The log setting.
        type: str
"""

EXAMPLES = """
- name: add SSH inbound rule to Panorama device group
  paloaltonetworks.panos.panos_decryption_rule:
    provider: '{{ provider }}'
    device_group: 'Cloud Edge'
    name: 'sampleRule'
    description: 'Made by Ansible'
    source_zones: ['any']
    source_addresses: ['192.168.10.15']
    source_users: ['any']
    source_hip: ['any']
    destination_zones: ['any']
    destination_addresses: ['10.20.30.40']
    destination_hip: ['any']
    negate_destination: true
    services: ['application-default']
    url_categories: ['adult', 'dating']
    action: 'decrypt'
    decryption_type: 'ssl-forward-proxy'
    log_successful_tls_handshakes: true
    log_failed_tls_handshakes: true
    audit_comment: 'Initial config'
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
        with_classic_provider_spec=True,
        error_on_firewall_shared=True,
        min_pandevice_version=(1, 7, 3),
        with_uuid=True,
        with_target=True,
        with_movement=True,
        with_audit_comment=True,
        with_gathered_filter=True,
        sdk_cls=("policies", "DecryptionRule"),
        sdk_params=dict(
            name=dict(required=True),
            description=dict(),
            source_zones=dict(type="list", elements="str"),
            source_addresses=dict(type="list", elements="str"),
            negate_source=dict(type="bool"),
            source_users=dict(type="list", elements="str"),
            source_hip=dict(type="list", elements="str"),
            destination_zones=dict(type="list", elements="str"),
            destination_addresses=dict(type="list", elements="str"),
            negate_destination=dict(type="bool"),
            destination_hip=dict(type="list", elements="str"),
            tags=dict(type="list", elements="str"),
            disabled=dict(type="bool"),
            services=dict(type="list", elements="str"),
            url_categories=dict(type="list", elements="str"),
            action=dict(
                type="str",
                default="no-decrypt",
                choices=["no-decrypt", "decrypt", "decrypt-and-forward"],
            ),
            decryption_type=dict(
                type="str",
                choices=["ssl-forward-proxy", "ssh-proxy", "ssl-inbound-inspection"],
            ),
            ssl_certificate=dict(),
            decryption_profile=dict(),
            forwarding_profile=dict(),
            group_tag=dict(),
            log_successful_tls_handshakes=dict(type="bool"),
            log_failed_tls_handshakes=dict(type="bool"),
            log_setting=dict(),
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
