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
module: panos_logical_router_vrf_static_route
short_description: Manage logical router static routes
description:
    - Manage PANOS Logical Routers Static Routes.
author:
    - Adam Baumeister (@abaumeister)
version_added: '3.3.0'
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
    name:
        description:
            - Static route name
        type: str
    destination:
        description:
            - Destination network
        type: str
    nexthop_type:
        description:
            - ip-address, discard, or next-vr
        type: str
        choices:
            - "ip-address"
            - "discard"
            - "next-lr"
    nexthop:
        description:
            - Next hop IP address or Next VR Name
        type: str
    interface:
        description:
            - Next hop interface
        type: str
    admin_dist:
        description:
            - Administrative distance
        type: str
    metric:
        description:
            - Metric
        type: int
        default: 10
    enable_path_monitor:
        description:
            - Enable Path Monitor
        type: bool
    failure_condition:
        description:
            - Path Monitor failure condition set 'any' or 'all'
        type: str
    preemptive_hold_time:
        description:
            - Path Monitor Preemptive Hold Time in minutes
        type: int
    bfd_profile:
        description:
            - Name of the BRD profile
        type: str
"""

EXAMPLES = """
- name: Create Logical Router
  paloaltonetworks.panos.panos_logical_router_vrf_static_route:
    provider: '{{ provider }}'
    name: lr-1
    commit: true
    destination: 1.1.1.1/32
    nexthop: 192.168.10.1
    nexthop_type: ip-address
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
        sdk_cls=("network", "VrfStaticRoute"),
        parents=(
            ("network", "LogicalRouter", "logical_router"),
            ("network", "Vrf", "vrf_name"),
        ),
        sdk_params=dict(
            name=dict(required=True),
            destination=dict(required=True),
            nexthop_type=dict(choices=["ip-address", "discard", "next-lr"]),
            nexthop=dict(),
            interface=dict(),
            admin_dist=dict(),
            metric=dict(type="int", default=10),
            enable_path_monitor=dict(type="bool"),
            failure_condition=dict(),
            preemptive_hold_time=dict(type="int"),
            bfd_profile=dict(),
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
