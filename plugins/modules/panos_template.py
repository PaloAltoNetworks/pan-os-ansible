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
module: panos_template
short_description: Manage Panorama template
description:
    - Manage Panorama template.
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
            - Name of the template.
        type: str
    description:
        description:
            - The description.
        type: str
    devices:
        description:
            - The list of serial numbers in this template.
        type: list
        elements: str
    default_vsys:
        description:
            - The default vsys in case of a single vsys firewall.
        type: str
        default: vsys1
    mode:
        description:
            - Mode for template.
        type: str
"""

EXAMPLES = """
# Create a template.
- name: Create template
  paloaltonetworks.panos.panos_template:
    provider: '{{ provider }}'
    name: 'hello world'
    description: 'my description here'
    devices:
      - 90123456
      - 91123456

# Delete a template
- name: Delete a template
  paloaltonetworks.panos.panos_template:
    provider: '{{ provider }}'
    name: 'some template'
    state: 'absent'
"""

RETURN = """
# Default return values
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    ConnectionHelper,
    get_connection,
    to_sdk_cls,
)


class Helper(ConnectionHelper):
    def pre_state_handling(self, obj, result, module):
        # Templates need a vsys child, this only matters if we're creating the
        # template, otherwise this should work because the sub-config should already
        # exist.
        vsys = to_sdk_cls("device", "Vsys")(module.params["default_vsys"])
        obj.add(vsys)

    def object_handling(self, obj, module):
        super().object_handling(obj, module)
        # override 'mode' param sdk default to None if it's not set explicitly in invocation.
        # SDK has `mode` attribute set to "normal" by default, but there is no xpath for this
        # resulting in xpath schema error if default is used.
        if module.params.get("mode") is None:
            setattr(obj, "mode", None)


def main():
    helper = get_connection(
        helper_cls=Helper,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        firewall_error="This is a Panorama only module",
        min_panos_version=(7, 0, 0),
        min_pandevice_version=(1, 5, 1),
        with_update_in_apply_state=True,
        sdk_cls=("panorama", "Template"),
        sdk_params=dict(
            name=dict(required=True),
            description=dict(),
            devices=dict(type="list", elements="str"),
            default_vsys=dict(default="vsys1"),
            mode=dict(),
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
