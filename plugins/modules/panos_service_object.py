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
short_description: Create service objects on PAN-OS devices.
description:
    - Create service objects on PAN-OS devices.
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
            - Name of service object.
        type: str
        required: true
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
"""

EXAMPLES = """
- name: Create service object 'ssh-tcp-22'
  panos_service_object:
    provider: '{{ provider }}'
    name: 'ssh-tcp-22'
    destination_port: '22'
    description: 'SSH on tcp/22'
    tag: ['Prod']

- name: Create service object 'mysql-tcp-3306'
  panos_service_object:
    provider: '{{ provider }}'
    name: 'mysql-tcp-3306'
    destination_port: '3306'
    description: 'MySQL on tcp/3306'

- name: Delete service object 'mysql-tcp-3306'
  panos_service_object:
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

try:
    from panos.errors import PanDeviceError
    from panos.objects import ServiceObject
except ImportError:
    try:
        from pandevice.errors import PanDeviceError
        from pandevice.objects import ServiceObject
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
            protocol=dict(default="tcp", choices=["tcp", "udp"]),
            source_port=dict(type="str"),
            destination_port=dict(type="str"),
            description=dict(type="str"),
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
        "protocol": module.params["protocol"],
        "source_port": module.params["source_port"],
        "destination_port": module.params["destination_port"],
        "description": module.params["description"],
        "tag": module.params["tag"],
    }

    # Other info.
    commit = module.params["commit"]

    # Retrieve current info.
    try:
        listing = ServiceObject.refreshall(parent, add=False)
    except PanDeviceError as e:
        module.fail_json(msg="Failed refresh: {0}".format(e))

    # Build the object based on the user spec.
    obj = ServiceObject(**spec)
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
