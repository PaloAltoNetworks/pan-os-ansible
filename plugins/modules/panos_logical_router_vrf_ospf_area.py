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
module: panos_logical_router_vrf_ospf_area
short_description: Manage logical router OSPF Area configuration
description:
    - Manage PANOS Logical Router OSPF AREA configuration
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
    name:
        description:
            - The Area ID
        type: str
    authentication:
        description:
            - Authentication profile name
        type: str
    type:
        description:
            - Area type
        type: str
    import_list:
        description:
            - Import list
        type: str
    export_list:
        description:
            - Export list
        type: str
    inbound_filter_list:
        description:
            - Inbound filter list
        type: str
    outbound_filter_list:
        description:
            - Outbound filter list
        type: str
    no_summary:
        description:
            - No summary
        type: bool
    metric:
        description:
            - Metric value
        type: int
    metric_type:
        description:
            - Metric type
        type: str
"""

EXAMPLES = """
- name: test_panos_logical_router_vrf - Configure an OSPF Area
  paloaltonetworks.panos.panos_logical_router_vrf_ospf_area:
    provider: '{{ device }}'
    logical_router: 'default'
    vrf_name: "default"
    name: "0.0.0.0"
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
        sdk_cls=("network", "VrfOspfArea"),
        parents=(
            ("network", "LogicalRouter", "logical_router"),
            ("network", "Vrf", "vrf_name"),
        ),
        sdk_params=dict(
            name=dict(type="str", required=True),
            authentication=dict(type="str"),
            type=dict(type="str"),
            import_list=dict(type="str"),
            export_list=dict(type="str"),
            inbound_filter_list=dict(type="str"),
            outbound_filter_list=dict(type="str"),
            no_summary=dict(type="bool"),
            metric=dict(type="int"),
            metric_type=dict(type="str"),
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
