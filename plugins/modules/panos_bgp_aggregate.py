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
module: panos_bgp_aggregate
short_description: Manage a BGP Aggregation Prefix Policy
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
    - paloaltonetworks.panos.fragments.full_template_support
    - paloaltonetworks.panos.fragments.deprecated_commit
    - paloaltonetworks.panos.fragments.gathered_filter
options:
    as_set:
        description:
            - Generate AS-set attribute.
        type: bool
        default: False
    attr_as_path_limit:
        description:
            - Add AS path limit attribute if it does not exist.
        type: int
    attr_as_path_prepend_times:
        description:
            - Prepend local AS for specified number of times.
        type: int
    attr_as_path_type:
        description:
            - AS path update options.
        type: str
        choices:
            - none
            - remove
            - prepend
            - remove-and-prepend
        default: none
    attr_community_argument:
        description:
            - Argument to the action community value if needed.
        type: str
    attr_community_type:
        description:
            - Community update options.
        type: str
        choices:
            - none
            - remove-all
            - remove-regex
            - append
            - overwrite
        default: none
    attr_extended_community_argument:
        description:
            - Argument to the action extended community value if needed.
        type: str
    attr_extended_community_type:
        description:
            - Extended community update options.
        type: str
        choices:
            - none
            - remove-all
            - remove-regex
            - append
            - overwrite
        default: none
    attr_local_preference:
        description:
            - New Local Preference value.
        type: int
    attr_med:
        description:
            - New Multi-Exit Discriminator value.
        type: int
    attr_nexthop:
        description:
            - Next-hop address.
        type: list
        elements: str
    attr_origin:
        description:
            - New route origin.
        type: str
        choices:
            - igp
            - egp
            - incomplete
        default: incomplete
    attr_weight:
        description:
            - New weight value.
        type: int
    enable:
        description:
            - Enable policy.
        default: True
        type: bool
    name:
        description:
            - Name of policy.
        type: str
    prefix:
        description:
            - Aggregating address prefix.
        type: str
    summary:
        description:
            - Summarize route.
        type: bool
    vr_name:
        description:
            - Name of the virtual router, it must already exist.  See M(paloaltonetworks.panos.panos_virtual_router).
        type: str
        default: default
"""

EXAMPLES = """
- name: Create BGP Aggregation Rule
  paloaltonetworks.panos.panos_bgp_aggregate:
    provider: '{{ provider }}'
    vr_name: 'default'
    name: 'aggr-rule-01'
    prefix: '10.0.0.0/24'
    enable: true
    summary: true

- name: Remove BGP Aggregation Rule
  paloaltonetworks.panos.panos_bgp_aggregate:
    provider: '{{ provider }}'
    vr_name: 'default'
    name: 'aggr-rule-01'
    state: 'absent'
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
        sdk_cls=("network", "BgpPolicyAggregationAddress"),
        sdk_params=dict(
            name=dict(required=True),
            enable=dict(type="bool", default=True),
            prefix=dict(),
            summary=dict(type="bool"),
            as_set=dict(type="bool", default=False),
            attr_local_preference=dict(type="int"),
            attr_med=dict(type="int"),
            attr_weight=dict(type="int"),
            attr_nexthop=dict(type="list", elements="str"),
            attr_origin=dict(
                type="str",
                default="incomplete",
                choices=["igp", "egp", "incomplete"],
            ),
            attr_as_path_limit=dict(type="int"),
            attr_as_path_type=dict(
                type="str",
                default="none",
                choices=["none", "remove", "prepend", "remove-and-prepend"],
            ),
            attr_as_path_prepend_times=dict(type="int"),
            attr_community_type=dict(
                type="str",
                default="none",
                choices=["none", "remove-all", "remove-regex", "append", "overwrite"],
            ),
            attr_community_argument=dict(),
            attr_extended_community_type=dict(
                type="str",
                default="none",
                choices=["none", "remove-all", "remove-regex", "append", "overwrite"],
            ),
            attr_extended_community_argument=dict(),
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
