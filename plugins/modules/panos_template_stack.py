#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2021 Palo Alto Networks, Inc
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
module: panos_template_stack
short_description: Manage Panorama template stack
description:
    - Manage Panorama template stack.
author:
    - Garfield Lee Freeman (@shinmog)
version_added: '2.8.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
    - pandevice >= 1.5.1
    - PANOS >= 7.0
notes:
    - Panorama is supported.
    - This is a Panorama only module.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
    - paloaltonetworks.panos.fragments.provider
options:
    name:
        description:
            - Name of the template stack.
        type: str
    description:
        description:
            - The description.
        type: str
    templates:
        description:
            - The list of templates in this stack.
        type: list
        elements: str
    devices:
        description:
            - The list of serial numbers in this template.
        type: list
        elements: str
"""

EXAMPLES = """
# Create a template.
- name: Create template stack
  paloaltonetworks.panos.panos_template_stack:
    provider: '{{ provider }}'
    name: 'hello world'
    description: 'my description here'
    templates:
      - template1
      - template2
    devices:
      - 90123456
      - 91123456

# Delete a template stack
- name: Delete a template stack
  paloaltonetworks.panos.panos_template_stack:
    provider: '{{ provider }}'
    name: 'some stack'
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
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        firewall_error="This is a Panorama only module",
        min_panos_version=(7, 0, 0),
        min_pandevice_version=(1, 5, 1),
        with_update_in_apply_state=True,
        sdk_cls=("panorama", "TemplateStack"),
        sdk_params=dict(
            name=dict(required=True),
            description=dict(),
            templates=dict(type="list", elements="str"),
            devices=dict(type="list", elements="str"),
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
