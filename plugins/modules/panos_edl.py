#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2023 Palo Alto Networks, Inc
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
module: panos_edl
short_description: Manage external dynamic lists on PAN-OS devices.
description:
    - Manage external dynamic lists on PAN-OS devices.
author:
    - Sebastian Czech (@sebastianczech)
version_added: '2.18.1'
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
            - Name of External Dynamic List to create.
        type: str
    description:
        description:
            - Descriptive name for this EDL.
        type: str
"""

EXAMPLES = """
- name: Create EDL 'test-edl'
  paloaltonetworks.panos.panos_edl:
    provider: '{{ provider }}'
    name: 'test-edl'
    description: 'EDL description'

- name: Delete EDL 'test-edl'
  paloaltonetworks.panos.panos_edl:
    provider: '{{ provider }}'
    name: 'test-edl'
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
        sdk_cls=("objects", "Edl"),
        sdk_params=dict(
            name=dict(required=True),
            description=dict(),
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
