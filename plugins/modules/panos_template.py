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
short_description: configure Panorama template
description:
    - Configure Panorama template.
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
            - Name of the template.
        type: str
        required: true
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
"""

EXAMPLES = """
# Create a template.
- name: Create template
  panos_template:
    provider: '{{ provider }}'
    name: 'hello world'
    description: 'my description here'
    devices:
      - 0123456
      - 1123456

# Delete a template
- name: Delete a template
  panos_template:
    provider: '{{ provider }}'
    name: 'some template'
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
    from panos.device import Vsys
    from panos.panorama import Template
except ImportError:
    try:
        from pandevice.errors import PanDeviceError, PanObjectMissing
        from pandevice.device import Vsys
        from pandevice.panorama import Template
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
            devices=dict(type="list", elements="str"),
            default_vsys=dict(default="vsys1"),
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
        "devices": module.params["devices"],
        "default_vsys": module.params["default_vsys"],
        "mode": None,
    }

    # Check for current object.
    live_obj = Template(spec["name"])
    parent.add(live_obj)
    try:
        live_obj.refresh()
    except PanObjectMissing:
        live_obj = None
    except PanDeviceError as e:
        module.fail_json(msg="Failed refresh: {0}".format(e))

    # Build the object and attach to the parent.
    obj = Template(**spec)
    parent.add(obj)

    # Templates need a vsys child, this only matters if we're creating the
    # template, otherwise this should work because the sub-config should already
    # exist.
    vsys = Vsys(module.params["default_vsys"])
    obj.add(vsys)

    # Perform the requeseted action.
    changed, diff = helper.apply_state_using_update(obj, live_obj, module)

    # Done!
    module.exit_json(changed=changed, diff=diff, msg="Done!")


if __name__ == "__main__":
    main()
