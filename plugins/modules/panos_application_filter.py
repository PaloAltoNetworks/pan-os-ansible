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

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
module: panos_application_filter
short_description: Manage application filters on PAN-OS devices.
description:
    - Manage application filters on PAN-OS devices.
author: "Michael Richardson (@mrichardson03)"
version_added: '2.1.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.vsys
    - paloaltonetworks.panos.fragments.device_group
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
options:
    name:
        description:
            - Name of the object.
        type: str
    category:
        description:
            - Application category
        type: list
        elements: str
    subcategory:
        description:
            - Application subcategory
        type: list
        elements: str
    technology:
        description:
            - Application technology
        type: list
        elements: str
    risk:
        description:
            - Risk (1-5) of the application
        type: list
        elements: str
        choices: ['1', '2', '3', '4', '5']
    evasive:
        description:
            - If the applications are evasive
        type: bool
    excessive_bandwidth_use:
        description:
            - If the applications use excessive bandwidth
        type: bool
    prone_to_misuse:
        description:
            - If the applications are prone to misuse
        type: bool
    is_saas:
        description:
            - If the applications are SaaS
        type: bool
    transfers_files:
        description:
            - If the applications transfer files
        type: bool
    tunnels_other_apps:
        description:
            - If the applications tunnel other applications
        type: bool
    used_by_malware:
        description:
            - If the applications are used by malware
        type: bool
    has_known_vulnerabilities:
        description:
            - If the applications have known vulnerabilities
        type: bool
    pervasive:
        description:
            - If the applications are used pervasively
        type: bool
    tag:
        description:
            - Administrative tags
        type: list
        elements: str
"""

EXAMPLES = """
- name: Create application filter
  paloaltonetworks.panos.panos_application_filter:
    provider: '{{ provider }}'
    name: 'custom-apps'
    category: ['business-systems']
    subcategory: ['auth-service']
    technology: ['client-server']
    risk: ['1']

- name: Remove custom application
  paloaltonetworks.panos.panos_application_filter:
    provider: '{{ provider }}'
    name: 'custom-apps'
    state: 'absent'
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
        with_classic_provider_spec=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        sdk_cls=("objects", "ApplicationFilter"),
        sdk_params=dict(
            name=dict(type="str", required=True),
            category=dict(type="list", elements="str"),
            subcategory=dict(type="list", elements="str"),
            technology=dict(type="list", elements="str"),
            risk=dict(type="list", elements="str", choices=["1", "2", "3", "4", "5"]),
            evasive=dict(type="bool"),
            excessive_bandwidth_use=dict(type="bool"),
            prone_to_misuse=dict(type="bool"),
            is_saas=dict(type="bool"),
            transfers_files=dict(type="bool"),
            tunnels_other_apps=dict(type="bool"),
            used_by_malware=dict(type="bool"),
            has_known_vulnerabilities=dict(type="bool"),
            pervasive=dict(type="bool"),
            tag=dict(type="list", elements="str"),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        required_one_of=helper.required_one_of,
        supports_check_mode=True,
    )

    helper.process(module)


if __name__ == "__main__":
    main()
