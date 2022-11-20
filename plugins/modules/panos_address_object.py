#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2018 Palo Alto Networks, Inc
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
module: panos_address_object
short_description: Manage address objects on PAN-OS devices.
description:
    - Manage address objects on PAN-OS devices.
author:
    - Michael Richardson (@mrichardson03)
    - Garfield Lee Freeman (@shinmog)
version_added: '1.0.0'
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
    - paloaltonetworks.panos.fragments.deprecated_commit
    - paloaltonetworks.panos.fragments.gathered_filter
options:
    name:
        description:
            - Name of object to create.
        type: str
    value:
        description:
            - IP address, IP range, or FQDN for the object.  Must specify if state is I(present).
        type: str
    address_type:
        description:
            - Type of address object.
        choices: ['ip-netmask', 'ip-range', 'fqdn', 'ip-wildcard']
        type: str
        default: 'ip-netmask'
    description:
        description:
            - Descriptive name for this address object.
        type: str
    tag:
        description:
            - List of tags to add to this address object.
        type: list
        elements: str
"""

EXAMPLES = """
- name: Create object 'Test-One'
  panos_address_object:
    provider: '{{ provider }}'
    name: 'Test-One'
    value: '1.1.1.1'
    description: 'Description One'
    tag: ['Prod']

- name: Create object 'Test-Two'
  panos_address_object:
    provider: '{{ provider }}'
    name: 'Test-Two'
    address_type: 'ip-range'
    value: '1.1.1.1-2.2.2.2'
    description: 'Description Two'
    tag: ['SI']

- name: Create object 'Test-Three'
  panos_address_object:
    provider: '{{ provider }}'
    name: 'Test-Three'
    address_type: 'fqdn'
    value: 'foo.bar.baz'
    description: 'Description Three'

- name: Delete object 'Test-Two'
  panos_address_object:
    provider: '{{ provider }}'
    name: 'Test-Two'
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
        with_commit=True,
        with_gathered_filter=True,
        sdk_cls=("objects", "AddressObject"),
        sdk_params=dict(
            name=dict(required=True),
            value=dict(),
            address_type=dict(
                default="ip-netmask",
                choices=["ip-netmask", "ip-range", "fqdn", "ip-wildcard"],
                sdk_param="type",
            ),
            description=dict(),
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
