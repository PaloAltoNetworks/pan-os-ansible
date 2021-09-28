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
module: panos_device_group
short_description: configure Panorama device group
description:
    - Configure Panorama device group.
author:
    - Garfield Lee Freeman (@shinmog)
version_added: '2.8.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
    - pandevice >= 1.5.1
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
            - Name of the device group.
        type: str
        required: true
    tag:
        description:
            - List of tags
        type: list
        elements: str
    parent:
        description:
            - Name of the device group parent.
            - An empty parent means the parent device group should be "shared".
        type: str
"""

EXAMPLES = """
# Create a device group under shared.
- name: Create device group
  panos_device_group:
    provider: '{{ provider }}'
    name: 'hello world'

# Create a device group under "hello world"
- name: Create device group under hello world
  panos_device_group:
    provider: '{{ provider }}'
    name: 'child'
    parent: 'hello world'

# Delete the child device group
- name: Delete a device group.
  panos_device_group:
    provider: '{{ provider }}'
    name: 'some device group'
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
    from panos.panorama import DeviceGroup
except ImportError:
    try:
        from pandevice.errors import PanDeviceError, PanObjectMissing
        from pandevice.panorama import DeviceGroup
    except ImportError:
        pass


def main():
    helper = get_connection(
        with_state=True,
        firewall_error="This is a Panorama only module",
        min_pandevice_version=(1, 5, 1),
        argument_spec=dict(
            name=dict(required=True),
            tag=dict(type="list", elements="str"),
            parent=dict(),
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
        "tag": module.params["tag"],
    }

    # Check for current object.
    live_obj = DeviceGroup(spec["name"])
    parent.add(live_obj)
    try:
        live_obj.refresh()
    except PanObjectMissing:
        live_obj = None
    except PanDeviceError as e:
        module.fail_json(msg="Failed refresh: {0}".format(e))

    # Build the object and attach to the parent.
    obj = DeviceGroup(**spec)
    parent.add(obj)

    # Opstate: get the current device group parent.
    try:
        obj.opstate.dg_hierarchy.refresh()
    except PanDeviceError as e:
        module.fail_json(msg="Failed dg hierarchy refresh: {0}".format(e))

    # Perform the requeseted action.
    changed, diff = helper.apply_state_using_update(obj, live_obj, module)

    # Opstate handling: device group parent.
    diff["before_parent"] = obj.opstate.dg_hierarchy.parent
    parent = module.params["parent"] or None
    if module.params["state"] == "absent":
        diff["after_parent"] = None
    else:
        diff["after_parent"] = parent
        if obj.opstate.dg_hierarchy.parent != parent:
            obj.opstate.dg_hierarchy.parent = parent
            changed = True
            if not module.check_mode:
                try:
                    obj.opstate.dg_hierarchy.update()
                except PanDeviceError as e:
                    module.fail_json(msg="Failed to set dg parent: {0}".format(e))

    # Done!
    module.exit_json(changed=changed, diff=diff, msg="Done!")


if __name__ == "__main__":
    main()
