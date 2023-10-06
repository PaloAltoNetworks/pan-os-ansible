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
module: panos_redistribution
short_description: Manage a Redistribution Profile on a virtual router
description:
    - Manage a Redistribution Profile on a virtual router
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
    name:
        description:
            - Name of rule.
        type: str
    priority:
        description:
            - Priority ID.
        type: int
    action:
        description:
            - Rule action.
        type: str
        choices:
            - no-redist
            - redist
        default: 'no-redist'
    filter_type:
        description:
            - Any of 'static', 'connect', 'rip', 'ospf', or 'bgp'.
        type: list
        elements: str
    filter_interface:
        description:
            - Filter interface.
        type: list
        elements: str
    filter_destination:
        description:
            - Filter destination.
        type: list
        elements: str
    filter_nexthop:
        description:
            - Filter nexthop.
        type: list
        elements: str
    ospf_filter_pathtype:
        description:
            - Any of 'intra-area', 'inter-area', 'ext-1', or 'ext-2'.
        type: list
        elements: str
    ospf_filter_area:
        description:
            - OSPF filter on area.
        type: list
        elements: str
    ospf_filter_tag:
        description:
            - OSPF filter on tag.
        type: list
        elements: str
    bgp_filter_community:
        description:
            - BGP filter on community.
        type: list
        elements: str
    bgp_filter_extended_community:
        description:
            - BGP filter on extended community.
        type: list
        elements: str
    type:
        description:
            - Name of rule.
        type: str
        choices:
            - ipv4
            - ipv6
        default: 'ipv4'
    vr_name:
        description:
            - Name of the virtual router; it must already exist; see M(paloaltonetworks.panos.panos_virtual_router).
        type: str
        default: 'default'
"""

EXAMPLES = """
- name: Create Redistribution Profile
  paloaltonetworks.panos.panos_redistribution:
    provider: '{{ provider }}'
    name: 'my-profile'
    priority: 42
"""

RETURN = """
# Default return values
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    ConnectionHelper,
    get_connection,
)


class Helper(ConnectionHelper):
    def spec_handling(self, spec, module):
        if module.params["type"] == "ipv4":
            self.sdk_cls = ("network", "RedistributionProfile")
        else:
            self.sdk_cls = ("network", "RedistributionProfileIPv6")


def main():
    helper = get_connection(
        helper_cls=Helper,
        template=True,
        template_stack=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        with_classic_provider_spec=True,
        with_commit=True,
        parents=(("network", "VirtualRouter", "vr_name", "default"),),
        sdk_params=dict(
            name=dict(type="str", required=True),
            priority=dict(type="int"),
            action=dict(
                type="str", default="no-redist", choices=["no-redist", "redist"]
            ),
            filter_type=dict(type="list", elements="str"),
            filter_interface=dict(type="list", elements="str"),
            filter_destination=dict(type="list", elements="str"),
            filter_nexthop=dict(type="list", elements="str"),
            ospf_filter_pathtype=dict(type="list", elements="str"),
            ospf_filter_area=dict(type="list", elements="str"),
            ospf_filter_tag=dict(type="list", elements="str"),
            bgp_filter_community=dict(type="list", elements="str"),
            bgp_filter_extended_community=dict(type="list", elements="str"),
        ),
        extra_params=dict(
            type=dict(type="str", default="ipv4", choices=["ipv4", "ipv6"]),
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
