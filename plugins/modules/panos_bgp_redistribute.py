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
module: panos_bgp_redistribute
short_description: Manage a BGP Redistribution Rule
description:
    - Use BGP to publish and consume routes from disparate networks.
author:
    - Joshua Colson (@freakinhippie)
    - Garfield Lee Freeman (@shinmog)
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is supported.
    - Panorama is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
    - paloaltonetworks.panos.fragments.full_template_support
    - paloaltonetworks.panos.fragments.deprecated_commit
options:
    address_family_identifier:
        description:
            - Address Family Identifier.
        type: str
        choices:
            - ipv4
            - ipv6
        default: 'ipv4'
    enable:
        description:
            - Enable rule.
        type: bool
        default: True
    metric:
        description:
            - Metric value.
        type: int
    name:
        description:
            - An IPv4 subnet or a defined Redistribution Profile in the virtual router.
        type: str
    route_table:
        description:
            - Summarize route.
        type: str
        choices:
            - unicast
            - multicast
            - both
        default: 'unicast'
    set_as_path_limit:
        description:
            - Add the AS_PATHLIMIT path attribute.
        type: int
    set_community:
        description:
            - Add the COMMUNITY path attribute.
        type: list
        elements: str
    set_extended_community:
        description:
            - Add the EXTENDED COMMUNITY path attribute.
        type: list
        elements: str
    set_local_preference:
        description:
            - Add the LOCAL_PREF path attribute.
        type: int
    set_med:
        description:
            - Add the MULTI_EXIT_DISC path attribute.
        type: int
    set_origin:
        description:
            - New route origin.
        type: str
        choices:
            - igp
            - egp
            - incomplete
        default: 'incomplete'
    vr_name:
        description:
            - Name of the virtual router; it must already exist.
            - See M(paloaltonetworks.panos.panos_virtual_router)
        type: str
        default: 'default'
"""

EXAMPLES = """
- name: BGP use Redistribution Policy 1
  paloaltonetworks.panos.panos_bgp_redistribute:
    provider: '{{ provider }}'
    name: '10.2.3.0/24'
    enable: true
    address_family_identifier: ipv4
    set_origin: incomplete
    vr_name: default
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
        with_classic_provider_spec=True,
        with_commit=True,
        with_gathered_filter=True,
        parents=(
            ("network", "VirtualRouter", "vr_name", "default"),
            ("network", "Bgp", None),
        ),
        sdk_cls=("network", "BgpRedistributionRule"),
        sdk_params=dict(
            name=dict(required=True),
            enable=dict(default=True, type="bool"),
            address_family_identifier=dict(default="ipv4", choices=["ipv4", "ipv6"]),
            route_table=dict(
                default="unicast",
                choices=["unicast", "multicast", "both"],
            ),
            set_origin=dict(
                default="incomplete",
                choices=["igp", "egp", "incomplete"],
            ),
            set_med=dict(type="int"),
            set_local_preference=dict(type="int"),
            set_as_path_limit=dict(type="int"),
            set_community=dict(type="list", elements="str"),
            set_extended_community=dict(type="list", elements="str"),
            metric=dict(type="int"),
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
