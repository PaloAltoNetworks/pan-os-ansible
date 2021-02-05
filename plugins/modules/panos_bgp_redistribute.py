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
short_description: Configures a BGP Redistribution Rule
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
    - paloaltonetworks.panos.fragments.state
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
        required: True
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
            - See M(panos_virtual_router)
        type: str
        default: 'default'
"""

EXAMPLES = """
- name: BGP use Redistribution Policy 1
  panos_bgp_redistribute:
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

try:
    from panos.errors import PanDeviceError
    from panos.network import Bgp, BgpRedistributionRule, VirtualRouter
except ImportError:
    try:
        from pandevice.errors import PanDeviceError
        from pandevice.network import Bgp, BgpRedistributionRule, VirtualRouter
    except ImportError:
        pass


def setup_args():
    return dict(
        commit=dict(type="bool", default=False),
        vr_name=dict(default="default"),
        name=dict(type="str", required=True),
        enable=dict(default=True, type="bool"),
        address_family_identifier=dict(
            type="str", default="ipv4", choices=["ipv4", "ipv6"]
        ),
        route_table=dict(
            type="str", default="unicast", choices=["unicast", "multicast", "both"]
        ),
        set_origin=dict(
            type="str", default="incomplete", choices=["igp", "egp", "incomplete"]
        ),
        set_med=dict(type="int"),
        set_local_preference=dict(type="int"),
        set_as_path_limit=dict(type="int"),
        set_community=dict(type="list", elements="str"),
        set_extended_community=dict(type="list", elements="str"),
        metric=dict(type="int"),
    )


def main():
    helper = get_connection(
        template=True,
        template_stack=True,
        with_state=True,
        with_classic_provider_spec=True,
        argument_spec=setup_args(),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    parent = helper.get_pandevice_parent(module)

    vr = VirtualRouter(module.params["vr_name"])
    parent.add(vr)
    try:
        vr.refresh()
    except PanDeviceError as e:
        module.fail_json(msg="Failed refresh: {0}".format(e))

    bgp = vr.find("", Bgp)
    if bgp is None:
        module.fail_json(msg='BGP is not configured for "{0}"'.format(vr.name))

    spec = {
        "name": module.params["name"],
        "enable": module.params["enable"],
        "address_family_identifier": module.params["address_family_identifier"],
        "route_table": module.params["route_table"],
        "set_origin": module.params["set_origin"],
        "set_med": module.params["set_med"],
        "set_local_preference": module.params["set_local_preference"],
        "set_as_path_limit": module.params["set_as_path_limit"],
        "set_community": module.params["set_community"],
        "set_extended_community": module.params["set_extended_community"],
        "metric": module.params["metric"],
    }

    listing = bgp.findall(BgpRedistributionRule)
    obj = BgpRedistributionRule(**spec)
    bgp.add(obj)

    changed, diff = helper.apply_state(obj, listing, module)

    if changed and module.params["commit"]:
        helper.commit(module)

    module.exit_json(changed=changed, diff=diff, msg="done")


if __name__ == "__main__":
    main()
