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
module: panos_logical_router_vrf_ospf_area_interface
short_description: Manage logical router OSPF interface configuration within an area
description:
    - Manage PANOS Logical Router OSPF
author:
    - Adam Baumeister (@abaumeister)
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
    - paloaltonetworks.panos.fragments.full_template_support
    - paloaltonetworks.panos.fragments.deprecated_commit
notes:
    - Checkmode is supported.
    - Panorama is supported.
options:
    logical_router:
        description:
            - The parent logical router
        type: str
        required: true
    vrf_name:
        description:
            - The parent VRF to insert the route into
        type: str
        required: true
    area_name:
        description:
            - The parent area to attach the interface to
        type: str
        required: true
    name:
        description:
            - Interface name
        type: str
    enable:
        description:
            - Enable OSPF on this interface
        type: bool
    mtu_ignore:
        description:
            - Ignore mtu when try to establish adjacency
        type: bool
    passive:
        description:
            - Suppress the sending of hello packets in this interface
        type: bool
    priority:
        description:
            - Priority for OSPF designated router selection
        type: int
    link_type:
        description:
            - Link Type
        type: str
    metric:
        description:
            - Cost of OSPF interface
        type: int
    authentication:
        description:
            - Authentication options
        type: str
    bfd_profile:
        description:
            - BFD profile
        type: str
    timing:
        description:
            - Protocol timer setting
        type: str
"""

EXAMPLES = """
- name: test_panos_logical_router_vrf_ospf_area_interface - Configure an OSPF Interface within an rea
  paloaltonetworks.panos.panos_logical_router_vrf_ospf_area:
    provider: '{{ device }}'
    logical_router: 'default'
    vrf_name: "default"
    area_name: "0.0.0.0"
    name: "ethernet1/1"
    template: '{{ template | default(omit) }}'
  register: result
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
        template=True,
        template_stack=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        with_classic_provider_spec=True,
        with_commit=True,
        sdk_cls=("network", "VrfOspfAreaInterface"),
        parents=(
            ("network", "LogicalRouter", "logical_router"),
            ("network", "Vrf", "vrf_name"),
            ("network", "VrfOspfArea", "area_name"),
        ),
        sdk_params=dict(
            name=dict(required=True, type="str"),
            enable=dict(type="bool"),
            mtu_ignore=dict(type="bool"),
            passive=dict(type="bool"),
            priority=dict(type="int"),
            link_type=dict(type="str"),
            metric=dict(type="int"),
            authentication=dict(type="str"),
            bfd_profile=dict(type="str"),
            timing=dict(type="str"),
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
