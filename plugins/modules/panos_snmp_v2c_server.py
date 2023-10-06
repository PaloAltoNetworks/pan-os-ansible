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
module: panos_snmp_v2c_server
short_description: Manage SNMP v2c servers.
description:
    - Manages SNMP v2c servers.
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
    snmp_profile:
        description:
            - Name of the SNMP server profile.
        type: str
        required: true
    name:
        description:
            - Name of the server.
        type: str
    manager:
        description:
            - IP address or FQDN of SNMP manager to use.
        type: str
    community:
        description:
            - SNMP community
        type: str
"""

EXAMPLES = """
# Create a snmp v2 server
- name: Create snmp v2 server
  paloaltonetworks.panos.panos_snmp_v2c_server:
    provider: '{{ provider }}'
    snmp_profile: 'my-profile'
    name: 'my-v2c-server'
    manager: '192.168.55.10'
    community: 'foobar'
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
        min_panos_version=(7, 1, 0),
        parents=(("device", "SnmpServerProfile", "snmp_profile"),),
        sdk_cls=("device", "SnmpV2cServer"),
        sdk_params=dict(
            name=dict(required=True),
            manager=dict(),
            community=dict(),
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
