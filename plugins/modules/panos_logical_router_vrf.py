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
module: panos_logical_router_vrf
short_description: Manage Logical Router VRFs
description:
    - Manage PANOS Logical Router VRFs.
author:
    - Joshua Colson (@freakinhippie)
    - Garfield Lee Freeman (@shinmog)
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
    - paloaltonetworks.panos.fragments.vsys_import
    - paloaltonetworks.panos.fragments.full_template_support
    - paloaltonetworks.panos.fragments.deprecated_commit
notes:
    - Checkmode is supported.
    - Panorama is supported.
options:
    name:
        description:
            -  Name of virtual router
        type: str
        default: 'default'
    logical_router:
        description:
            - Name of the logical router to add this interface to
        type: str
        default: 'default'
    vrf:
        description:
            - Name of the VRF to add this interface to
        default: 'default' 
    interfaces:
        description:
            -  List of interfaces to associate with the logical router
        type: list
"""

EXAMPLES = """
- name: Add ethernet1/1 to VRF "default" on logical router "default"
  paloaltonetworks.panos.panos_logical_router_vrf:
    provider: '{{ provider }}'
    logical_router: default
    name: default
    interfaces:
      - ethernet1/1
"""

RETURN = """
# Default return values
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    get_connection,
)

from panos.network import Vrf

def main():
    helper = get_connection(
        template=True,
        template_stack=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        with_classic_provider_spec=True,
        with_commit=True,
        sdk_cls=("network", "Vrf"),
        parents=(("network", "LogicalRouter", "logical_router", "default"),),
        sdk_params=dict(
            name=dict(required=True),
            interface=dict(type="list", elements="str"),
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
