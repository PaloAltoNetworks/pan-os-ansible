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
module: panos_bgp_dampening
short_description: Manage a BGP Dampening Profile
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
    - paloaltonetworks.panos.fragments.full_template_support
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.deprecated_commit
    - paloaltonetworks.panos.fragments.gathered_filter
options:
    vr_name:
        description:
            - Name of the virtual router; it must already exist.
            - See M(paloaltonetworks.panos.panos_virtual_router).
        type: str
        default: 'default'
    cutoff:
        description:
            - Cutoff threshold value.
        type: float
    decay_half_life_reachable:
        description:
            - Decay half-life while reachable (in seconds).
        type: int
    decay_half_life_unreachable:
        description:
            - Decay half-life while unreachable (in seconds).
        type: int
    enable:
        description:
            - Enable profile.
        default: True
        type: bool
    max_hold_time:
        description:
            - Maximum of hold-down time (in seconds).
        type: int
    name:
        description:
            - Name of Dampening Profile.
        type: str
    reuse:
        description:
            - Reuse threshold value.
        type: float
"""

EXAMPLES = """
- name: Create BGP Dampening Profile
  paloaltonetworks.panos.panos_bgp_dampening:
    name: damp-profile-1
    enable: true
    commit: true
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
        sdk_cls=("network", "BgpDampeningProfile"),
        sdk_params=dict(
            name=dict(type="str", required=True),
            enable=dict(default=True, type="bool"),
            cutoff=dict(type="float"),
            reuse=dict(type="float"),
            max_hold_time=dict(type="int"),
            decay_half_life_reachable=dict(type="int"),
            decay_half_life_unreachable=dict(type="int"),
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
