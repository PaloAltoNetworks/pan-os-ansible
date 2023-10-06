#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2019 Palo Alto Networks, Inc
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
module: panos_virtual_wire
short_description: Manage Virtual Wires (vwire).
description:
    - Manage PAN-OS Virtual Wires (vwire).
author: "Patrick Avery (@unknown)"
version_added: '1.0.0'
requirements:
    - pan-python
    - pandevice
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
    - paloaltonetworks.panos.fragments.vsys_import
    - paloaltonetworks.panos.fragments.full_template_support
notes:
    - Checkmode is supported.
    - Panorama is supported.
options:
    name:
        description:
            -  Name of the Virtual Wire
        type: str
    interface1:
        description:
            - First interface of Virtual Wire
        type: str
    interface2:
        description:
            - Second interface of Virtual Wire
        type: str
    tag:
        description:
            - Set tag that is allowed over Virtual Wire.  Currently
              pandevice only supports all (default) or 1 tag.
        type: int
    multicast:
        description:
            - Enable multicast firewalling
        type: bool
    pass_through:
        description:
            - Enable link state pass through
        type: bool
"""

EXAMPLES = """
- name: Create Vwire
  paloaltonetworks.panos.panos_virtual_wire:
    provider: '{{ provider }}'
    name: 'vwire1'
    interface1: 'ethernet1/1'
    interface2: 'ethernet1/2'
    tag: 100
    multicast: 'true'
    pass_through: 'true'
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
        vsys_importable=True,
        template=True,
        template_stack=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        with_classic_provider_spec=True,
        with_set_vsys_reference=True,
        sdk_cls=("network", "VirtualWire"),
        sdk_params=dict(
            name=dict(
                type="str",
                required=True,
            ),
            interface1=dict(),
            interface2=dict(),
            tag=dict(type="int"),
            multicast=dict(type="bool"),
            pass_through=dict(type="bool"),
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
