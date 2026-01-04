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
module: panos_ldap_server
short_description: Manage LDAP servers in an LDAP profile.
description:
    - Manages LDAP servers in an LDAP server profile.
author: "Garfield Lee Freeman (@shinmog)"
version_added: '1.0.0'
requirements:
    - pan-python
    - pandevice >= 0.11.1
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.vsys_shared
    - paloaltonetworks.panos.fragments.device_group
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
options:
    ldap_profile:
        description:
            - Name of the LDAP server profile.
        type: str
        required: True
    name:
        description:
            - Name of the LDAP server profile.
        type: str
    ldap_server_address:
        description:
            - IP address or FQDN of ldap server to use.
        type: str
    ldap_port:
        description:
            - Port number
        type: str
"""

EXAMPLES = """
# Create an LDAP server and assign to 'my-profile' LDAP Server Profile
- name: Create LDAP server in an LDAP profile
  paloaltonetworks.panos.panos_ldap_server:
    provider: '{{ provider }}'
    ldap_profile: 'my-profile'
    name: 'my-ldap-server'
    ldap_server_address: 'lldap.example.com'
    port: '637'
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
        vsys_shared=True,
        device_group=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        with_classic_provider_spec=True,
        min_pandevice_version=(0, 11, 1),
        min_panos_version=(7, 0, 0),
        parents=(("device", "LdapServerProfile", "ldap_profile"),),
        sdk_cls=("device", "LdapServer"),
        sdk_params=dict(
            name=dict(),
            ldap_server_address=dict(type="str", sdk_param="address"),
            ldap_port=dict(type="str", sdk_param="port"),
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
