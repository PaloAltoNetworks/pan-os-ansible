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
module: panos_virtual_router
short_description: Manage a Virtual Router
description:
    - Manage PANOS Virtual Router
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
    interface:
        description:
            -  List of interface names
        type: list
        elements: str
    ad_static:
        description:
            -  Administrative distance for this protocol
        type: int
    ad_static_ipv6:
        description:
            -  Administrative distance for this protocol
        type: int
    ad_ospf_int:
        description:
            -  Administrative distance for this protocol
        type: int
    ad_ospf_ext:
        description:
            -  Administrative distance for this protocol
        type: int
    ad_ospfv3_int:
        description:
            -  Administrative distance for this protocol
        type: int
    ad_ospfv3_ext:
        description:
            -  Administrative distance for this protocol
        type: int
    ad_ibgp:
        description:
            -  Administrative distance for this protocol
        type: int
    ad_ebgp:
        description:
            -  Administrative distance for this protocol
        type: int
    ad_rip:
        description:
            -  Administrative distance for this protocol
        type: int
"""

EXAMPLES = """
- name: Create Virtual Router
  paloaltonetworks.panos.panos_virtual_router:
    provider: '{{ provider }}'
    name: vr-1
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
        vsys_importable=True,
        template=True,
        template_stack=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        with_classic_provider_spec=True,
        with_commit=True,
        with_set_vsys_reference=True,
        sdk_cls=("network", "VirtualRouter"),
        sdk_params=dict(
            name=dict(type="str", default="default"),
            interface=dict(type="list", elements="str"),
            ad_static=dict(type="int"),
            ad_static_ipv6=dict(type="int"),
            ad_ospf_int=dict(type="int"),
            ad_ospf_ext=dict(type="int"),
            ad_ospfv3_int=dict(type="int"),
            ad_ospfv3_ext=dict(type="int"),
            ad_ibgp=dict(type="int"),
            ad_ebgp=dict(type="int"),
            ad_rip=dict(type="int"),
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
