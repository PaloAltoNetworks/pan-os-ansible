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
module: panos_service_group
short_description: Create service group objects on PAN-OS devices.
description:
    - Create service group objects on PAN-OS devices.
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
    - paloaltonetworks.panos.fragments.state
    - paloaltonetworks.panos.fragments.deprecated_commit
options:
    name:
        description:
            - Name of service group.
        type: str
        required: true
    value:
        description:
            - List of service objects to be included in the group.  Must specify if state is
              present.
        type: list
        elements: str
    tag:
        description:
            - List of tags for this service group.
        type: list
        elements: str
"""

EXAMPLES = """
- name: Create service group 'Prod-Services'
  panos_service_group:
    provider: '{{ provider }}'
    name: 'Prod-Services'
    value: ['ssh-tcp-22', 'mysql-tcp-3306']

- name: Delete service group 'Prod-Services'
  panos_service_group:
    provider: '{{ provider }}'
    name: 'Prod-Services'
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
    from panos.errors import PanDeviceError
    from panos.objects import ServiceGroup
except ImportError:
    try:
        from pandevice.errors import PanDeviceError
        from pandevice.objects import ServiceGroup
    except ImportError:
        pass


def main():
    helper = get_connection(
        vsys=True,
        device_group=True,
        with_classic_provider_spec=True,
        with_state=True,
        argument_spec=dict(
            name=dict(type="str", required=True),
            value=dict(type="list", elements="str"),
            tag=dict(type="list", elements="str"),
            commit=dict(type="bool", default=False),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        required_one_of=helper.required_one_of,
        supports_check_mode=True,
    )

    # Verify libs are present, get parent object.
    parent = helper.get_pandevice_parent(module)

    # Object params.
    spec = {
        "name": module.params["name"],
        "value": module.params["value"],
        "tag": module.params["tag"],
    }

    # Other info.
    commit = module.params["commit"]

    # Retrieve current info.
    try:
        listing = ServiceGroup.refreshall(parent, add=False)
    except PanDeviceError as e:
        module.fail_json(msg="Failed refresh: {0}".format(e))

    # Build the object based on the user spec.
    obj = ServiceGroup(**spec)
    parent.add(obj)

    # Apply the state.
    changed, diff = helper.apply_state(obj, listing, module)

    # Commit.
    if commit and changed:
        helper.commit(module)

    # Done.
    module.exit_json(changed=changed, diff=diff)


if __name__ == "__main__":
    main()
