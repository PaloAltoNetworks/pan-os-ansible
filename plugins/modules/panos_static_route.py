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
module: panos_static_route
short_description: Manage static routes on PAN-OS devices.
description:
    - Manage static routes on PAN-OS devices.
author:
    - Michael Richardson (@mrichardson03)
    - Garfield Lee Freeman (@shinmog)
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is supported.
    - Panorama is supported.
    - IPv6 is not supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
    - paloaltonetworks.panos.fragments.full_template_support
options:
    name:
        description:
            - Name of static route.
        type: str
    destination:
        description:
            - Destination network.  Required if I(state=present).
        type: str
    nexthop_type:
        description:
            - Type of next hop.
        type: str
        choices:
            - ip-address
            - discard
            - none
            - next-vr
        default: 'ip-address'
    nexthop:
        description:
            - Next hop IP address.  Required if I(state=present).
        type: str
    admin_dist:
        description:
            - Administrative distance for static route.
        type: str
    metric:
        description:
            - Metric for route.
        type: int
        default: '10'
    virtual_router:
        description:
            - Virtual router to use.
        type: str
        default: 'default'
    interface:
        description:
            - The Interface to use.
        type: str
    enable_path_monitor:
        description:
            - Enable path monitor.
        type: bool
    failure_condition:
        description:
            - Path monitor failure condition.
        type: str
        choices:
            - any
            - all
    preemptive_hold_time:
        description:
            - Path monitor preemptive hold time in minutes.
        type: int
"""

EXAMPLES = """
- name: Create route 'Test-One'
  panos_static_route:
    provider: '{{ provider }}'
    name: 'Test-One'
    destination: '1.1.1.0/24'
    nexthop: '10.0.0.1'

- name: Create route 'Test-Two'
  panos_static_route:
    provider: '{{ provider }}'
    name: 'Test-Two'
    destination: '2.2.2.0/24'
    nexthop: '10.0.0.1'

- name: Create route 'Test-Three'
  panos_static_route:
    provider: '{{ provider }}'
    name: 'Test-Three'
    destination: '3.3.3.0/24'
    nexthop: '10.0.0.1'

- name: Delete route 'Test-Two'
  panos_static_route:
    provider: '{{ provider }}'
    name: 'Test-Two'
    state: 'absent'

- name: Create route 'Test-Four'
  panos_static_route:
    provider: '{{ provider }}'
    name: 'Test-Four'
    destination: '4.4.4.0/24'
    nexthop: '10.0.0.1'
    virtual_router: 'VR-Two'

- name: Create route 'Test-Five'
  panos_static_route:
    provider: '{{ provider }}'
    name: 'Test-Five'
    destination: '5.5.5.0/24'
    nexthop_type: 'none'
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
        if module.params["state"] == "merged" and spec["nexthop_type"] == "none":
            msg = [
                "Nexthop cannot be set to None with state='merged'.",
                "You will need to use either state='present' or state='replaced'.",
            ]
            module.fail_json(msg=" ".join(msg))

        if spec["nexthop_type"] == "none":
            spec["nexthop_type"] = None


def main():
    helper = get_connection(
        helper_cls=Helper,
        template=True,
        template_stack=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        with_classic_provider_spec=True,
        parents=(("network", "VirtualRouter", "virtual_router", "default"),),
        sdk_cls=("network", "StaticRoute"),
        sdk_params=dict(
            name=dict(required=True),
            destination=dict(),
            nexthop_type=dict(
                default="ip-address",
                choices=["ip-address", "discard", "none", "next-vr"],
            ),
            nexthop=dict(),
            admin_dist=dict(),
            metric=dict(type="int", default=10),
            interface=dict(),
            enable_path_monitor=dict(type="bool"),
            failure_condition=dict(choices=["any", "all"]),
            preemptive_hold_time=dict(type="int"),
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
