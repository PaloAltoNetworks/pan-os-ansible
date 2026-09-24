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
module: panos_ldap_profile
short_description: Manage LDAP server profiles.
description:
    - Manages LDAP server profiles.
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
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
    - paloaltonetworks.panos.fragments.vsys_shared
    - paloaltonetworks.panos.fragments.device_group
options:
    name:
        description:
            - Name of the LDAP server profile.
        type: str
    ldap_type:
        description:
            - Ldap profile type.
        type: str
        choices:
            - other
            - active-directory
            - e-directory
            - sun
        default: other
    base_dn:
        description:
            - Base DN.
        type: str
    bind_dn:
        description:
            - Bind DN.
        type: str
    bind_password:
        description:
            - Bind password.
        type: str
    bind_timelimit:
        description:
            - Bind timeout.
        type: int
    timelimit:
        description:
            - Search timeout.
        type: int
    retry_interval :
        description:
            - Retry interval.
        type: int
    require_ssl:
        description:
            - Require ssl/ttls secured connection.
        type: bool
    verify_server_certificate:
        description:
            - Verify server certificate for ssl sessions.
        type: bool
    disabled:
        description:
            - Disabled or not.
        type: bool
"""

EXAMPLES = """
# Create an LDAP profile
- name: Create LDAP profile
  paloaltonetworks.panos.panos_ldap_profile:
    provider: '{{ provider }}'
    name: 'my-profile'
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
        sdk_cls=("device", "LdapServerProfile"),
        sdk_params=dict(
            name=dict(),
            ldap_type=dict(choices=["other", "active-directory", "e-directory", "sun"], default="other"),
            base_dn=dict(sdk_param="base"),
            bind_dn=dict(),
            bind_password=dict(no_log=True),
            bind_timelimit=dict(type="int"),
            timelimit=dict(type="int"),
            retry_interval=dict(type="int"),
            require_ssl=dict(type="bool", sdk_param="ssl"),
            verify_server_certificate=dict(type="bool"),
            disabled=dict(type="bool")

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
