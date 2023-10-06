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
short_description: Manage Panorama device group
description:
    - Manage Panorama device group.
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
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
    - paloaltonetworks.panos.fragments.provider
options:
    name:
        description:
            - Name of the device group.
        type: str
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
  paloaltonetworks.panos.panos_device_group:
    provider: '{{ provider }}'
    name: 'hello world'

# Create a device group under "hello world"
- name: Create device group under hello world
  paloaltonetworks.panos.panos_device_group:
    provider: '{{ provider }}'
    name: 'child'
    parent: 'hello world'

# Delete the child device group
- name: Delete a device group.
  paloaltonetworks.panos.panos_device_group:
    provider: '{{ provider }}'
    name: 'some device group'
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
        PanDeviceError = to_sdk_cls("errors", "PanDeviceError")

        # Opstate: get the current device group parent.
        try:
            obj.opstate.dg_hierarchy.refresh()
        except PanDeviceError as e:
            module.fail_json(msg="Failed dg hierarchy refresh: {0}".format(e))

    def post_state_handling(self, obj, result, module):
        PanDeviceError = to_sdk_cls("errors", "PanDeviceError")

        result.setdefault("diff", {})
        result["diff"]["before_parent"] = obj.opstate.dg_hierarchy.parent

        if module.params["state"] in ("absent", "deleted"):
            result["diff"]["after_parent"] = None
        else:
            parent = module.params["parent"]
            result["diff"]["after_parent"] = parent
            if obj.opstate.dg_hierarchy.parent != parent and module.params["state"] in (
                "present",
                "replaced",
                "merged",
            ):
                result["changed"] = True
                obj.opstate.dg_hierarchy.parent = parent
                if not module.check_mode:
                    try:
                        obj.opstate.dg_hierarchy.update()
                    except PanDeviceError as e:
                        module.fail_json(msg="Failed to set dg parent: {0}".format(e))


def main():
    helper = get_connection(
        helper_cls=Helper,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        firewall_error="This is a Panorama only module",
        min_pandevice_version=(1, 5, 1),
        with_update_in_apply_state=True,
        sdk_cls=("panorama", "DeviceGroup"),
        sdk_params=dict(
            name=dict(required=True),
            tag=dict(type="list", elements="str"),
        ),
        extra_params=dict(
            parent=dict(),
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
