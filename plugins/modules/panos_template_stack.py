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
short_description: configure Panorama template stack
description:
    - Configure Panorama template stack.
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
    - paloaltonetworks.panos.fragments.state
    - paloaltonetworks.panos.fragments.provider
options:
    name:
        description:
            - Name of the template stack.
        type: str
        required: true
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
  panos_template_stack:
    provider: '{{ provider }}'
    name: 'hello world'
    description: 'my description here'
    templates:
        - template1
        - template2
    devices:
      - 0123456
      - 1123456

# Delete a template stack
- name: Delete a template stack
  panos_template_stack:
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

try:
    from panos.errors import PanDeviceError, PanObjectMissing
    from panos.panorama import TemplateStack
except ImportError:
    try:
        from pandevice.errors import PanDeviceError, PanObjectMissing
        from pandevice.panorama import TemplateStack
    except ImportError:
        pass


def main():
    helper = get_connection(
        with_state=True,
        firewall_error="This is a Panorama only module",
        min_panos_version=(7, 0, 0),
        min_pandevice_version=(1, 5, 1),
        argument_spec=dict(
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

    # Verify imports, build pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    # Object params.
    spec = {
        "name": module.params["name"],
        "description": module.params["description"],
        "templates": module.params["templates"],
        "devices": module.params["devices"],
    }

    # Check for current object.
    live_obj = TemplateStack(spec["name"])
    parent.add(live_obj)
    try:
        live_obj.refresh()
    except PanObjectMissing:
        live_obj = None
    except PanDeviceError as e:
        module.fail_json(msg="Failed refresh: {0}".format(e))

    # Build the object and attach to the parent.
    obj = TemplateStack(**spec)
    parent.add(obj)

    # Perform the requeseted action.
    changed, diff = helper.apply_state_using_update(obj, live_obj, module)

    # Done!
    module.exit_json(changed=changed, diff=diff, msg="Done!")


if __name__ == "__main__":
    main()
