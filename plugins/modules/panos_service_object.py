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
module: panos_service_object
short_description: Manage service objects on PAN-OS devices.
description:
    - Manage service objects on PAN-OS devices.
author: "Michael Richardson (@mrichardson03)"
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
    - paloaltonetworks.panos.fragments.gathered_filter
    - paloaltonetworks.panos.fragments.deprecated_commit
options:
    name:
        description:
            - Name of service object.
        type: str
    protocol:
        description:
            - Protocol of the service.
        type: str
        choices: ['tcp', 'udp']
        default: 'tcp'
    source_port:
        description:
            - Source port of the service object.
        type: str
    destination_port:
        description:
            - Destination port of the service object.  Required if state is I(present).
        type: str
    description:
        description:
            - Descriptive name for this service object.
        type: str
    tag:
        description:
            - List of tags for this service object.
        type: list
        elements: str
    enable_override_timeout:
        description:
            - PAN-OS 8.1 and above.
            - Override session timeout value.
        type: str
        choices: ["no", "yes"]
    override_timeout:
        description:
            - PAN-OS 8.1 and above.
            - The TCP or UDP session timeout value (in seconds).
        type: int
    override_half_close_timeout:
        description:
            - PAN-OS 8.1 and above.
            - Applicable for I(protocol=tcp) only.
            - TCP session half-close tieout value (in seconds).
        type: int
    override_time_wait_timeout:
        description:
            - PAN-OS 8.1 and above.
            - Applicable for I(protocol=tcp) only.
            - TCP session time-wait timeout value (in seconds).
        type: int
"""

EXAMPLES = """
- name: Create service object 'ssh-tcp-22'
  paloaltonetworks.panos.panos_service_object:
    provider: '{{ provider }}'
    name: 'ssh-tcp-22'
    destination_port: '22'
    description: 'SSH on tcp/22'
    tag: ['Prod']

- name: Create service object 'mysql-tcp-3306'
  paloaltonetworks.panos.panos_service_object:
    provider: '{{ provider }}'
    name: 'mysql-tcp-3306'
    destination_port: '3306'
    description: 'MySQL on tcp/3306'

- name: Delete service object 'mysql-tcp-3306'
  paloaltonetworks.panos.panos_service_object:
    provider: '{{ provider }}'
    name: 'mysql-tcp-3306'
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
        with_commit=True,
        min_pandevice_version=(1, 7, 3),
        sdk_cls=("objects", "ServiceObject"),
        sdk_params=dict(
            name=dict(type="str", required=True),
            protocol=dict(default="tcp", choices=["tcp", "udp"]),
            source_port=dict(type="str"),
            destination_port=dict(type="str"),
            description=dict(type="str"),
            tag=dict(type="list", elements="str"),
            enable_override_timeout=dict(choices=["no", "yes"]),
            override_timeout=dict(type="int"),
            override_half_close_timeout=dict(type="int"),
            override_time_wait_timeout=dict(type="int"),
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
