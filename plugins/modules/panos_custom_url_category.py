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
module: panos_custom_url_category
short_description: Manage custom url category objects on PAN-OS devices.
description:
    - Manage custom url category objects on PAN-OS devices.
author: "Borislav Varadinov (@bvaradinov-c)"
version_added: '2.0.0'
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
            - Name of the url category.
        type: str
    description:
        description:
            - Descriptive name for this custom url category.
        type: str
    url_value:
        description:
            - List with urls
        type: list
        elements: str
    type:
        description:
            - Custom category type (currently unused)
        type: str
        choices: ['URL List', 'Category Match']
        default: 'URL List'
"""

EXAMPLES = """
- name: Create Custom Url Category 'Internet Access List'
  paloaltonetworks.panos.panos_custom_url_category:
    provider: '{{ provider }}'
    name: 'Internet Access List'
    description: 'Description One'
    url_value:
      - microsoft.com
      - redhat.com

- name: Remove Custom Url Category 'Internet Access List'
  paloaltonetworks.panos.panos_custom_url_category:
    provider: '{{ provider }}'
    name: 'Internet Access List'
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
        min_pandevice_version=(1, 5, 0),
        with_classic_provider_spec=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        sdk_cls=("objects", "CustomUrlCategory"),
        sdk_params=dict(
            name=dict(required=True),
            description=dict(),
            url_value=dict(type="list", elements="str"),
            type=dict(default="URL List", choices=["URL List", "Category Match"]),
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
