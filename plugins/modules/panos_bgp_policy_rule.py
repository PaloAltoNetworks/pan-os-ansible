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
module: panos_bgp_policy_rule
short_description: Manage a BGP Policy Import/Export Rule
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
    - paloaltonetworks.panos.fragments.state
    - paloaltonetworks.panos.fragments.deprecated_commit
options:
    type:
        description:
            - The type of rule.
        type: str
        choices:
            - import
            - export
        required: True
    name:
        description:
            - Name of filter.
        type: str
        required: True
    enable:
        description:
            - Enable rule.
        type: bool
        default: True
    match_afi:
        description:
            - Address Family Identifier.
        type: str
        choices:
            - ip
            - ipv6
    match_safi:
        description:
            - Subsequent Address Family Identifier.
        type: str
        choices:
            - ip
            - ipv6
    match_route_table:
        description:
            - Route table to match rule.
        type: str
        choices:
            - unicast
            - multicast
            - both
    match_nexthop:
        description:
            - Next-hop attributes.
        type: list
        elements: str
    match_from_peer:
        description:
            - Filter by peer that sent this route.
        type: list
        elements: str
    match_med:
        description:
            - Multi-Exit Discriminator.
        type: int
    match_as_path_regex:
        description:
            - AS-path regular expression.
        type: str
    match_community_regex:
        description:
            - Community AS-path regular expression.
        type: str
    match_extended_community_regex:
        description:
            - Extended Community AS-path regular expression.
        type: str
    used_by:
        description:
            - Peer-groups that use this rule.
        type: list
        elements: str
    action:
        description:
            - Rule action.
        type: str
        choices:
            - allow
            - deny
    action_local_preference:
        description:
            - New local preference value.
        type: int
    action_med:
        description:
            - New MED value.
        type: int
    action_nexthop:
        description:
            - Nexthop address.
        type: str
    action_origin:
        description:
            - New route origin.
        type: str
        choices:
            - igp
            - egp
            - incomplete
    action_as_path_limit:
        description:
            - Add AS path limit attribute if it does not exist.
        type: int
    action_as_path_type:
        description:
            - AS path update options.
        type: str
        choices:
            - none
            - remove
            - prepend
            - remove-and-prepend
    action_as_path_prepend_times:
        description:
            - Prepend local AS for specified number of times.
        type: int
    action_community_type:
        description:
            - Community update options.
        type: str
        choices:
            - none
            - remove-all
            - remove-regex
            - append
            - overwrite
    action_community_modifier:
        description:
            - Modifier for the community action. Required if 'action_community_type' is set to 'append' or 'overwrite'.
        type: str
    action_community_argument:
        description:
            - Argument to the action community value if needed.
        type: str
    action_extended_community_type:
        description:
            - Extended community update options.
        type: str
    action_extended_community_argument:
        description:
            - Argument to the action extended community value if needed.
        type: str
    action_dampening:
        description:
            - Route flap dampening profile; only with "import" type.
        type: str
    action_weight:
        description:
            - New weight value; only with "import" type.
        type: int
    address_prefix:
        description:
            - List of address prefix dicts with "name"/"exact" keys.
        type: list
        elements: dict
    vr_name:
        description:
            - Name of the virtual router; it must already exist; see M(paloaltonetworks.panos.panos_virtual_router).
        type: str
        default: default
"""

EXAMPLES = """
# Add a BGP Policy
- name: Create Policy Import Rule
  paloaltonetworks.panos.panos_bgp_policy_rule:
    provider: '{{ provider }}'
    vr_name: 'default'
    name: 'import-rule-001'
    type: 'import'
    enable: true
    action: 'allow'
    address_prefix:
      - name: '10.1.1.0/24'
      - name: '10.1.2.0/24'
        exact: false
      - name: '10.1.3.0/24'
        exact: true
    action_dampening: 'dampening-profile'

- name: Create Policy Export Rule
  paloaltonetworks.panos.panos_bgp_policy_rule:
    provider: '{{ provider }}'
    vr_name: 'default'
    name: 'export-rule-001'
    type: 'export'
    enable: true
    action: 'allow'

- name: Remove Export Rule
  paloaltonetworks.panos.panos_bgp_policy_rule:
    provider: '{{ provider }}'
    state: 'absent'
    vr_name: 'default'
    name: 'export-rule-001'
    type: 'export'
"""

RETURN = """
# Default return values
"""

from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    get_connection,
)

try:
    from panos.errors import PanDeviceError
    from panos.network import (
        Bgp,
        BgpPolicyAddressPrefix,
        BgpPolicyExportRule,
        BgpPolicyImportRule,
        VirtualRouter,
    )
except ImportError:
    try:
        from pandevice.errors import PanDeviceError
        from pandevice.network import (
            Bgp,
            BgpPolicyAddressPrefix,
            BgpPolicyExportRule,
            BgpPolicyImportRule,
            VirtualRouter,
        )
    except ImportError:
        pass


def setup_args():
    return dict(
        commit=dict(type="bool"),
        vr_name=dict(default="default"),
        type=dict(type="str", required=True, choices=["import", "export"]),
        name=dict(type="str", required=True),
        enable=dict(default=True, type="bool"),
        match_afi=dict(type="str", choices=["ip", "ipv6"]),
        match_safi=dict(type="str", choices=["ip", "ipv6"]),
        match_route_table=dict(type="str", choices=["unicast", "multicast", "both"]),
        match_nexthop=dict(type="list", elements="str"),
        match_from_peer=dict(type="list", elements="str"),
        match_med=dict(type="int"),
        match_as_path_regex=dict(type="str"),
        match_community_regex=dict(type="str"),
        match_extended_community_regex=dict(type="str"),
        used_by=dict(type="list", elements="str"),
        action=dict(type="str", choices=["allow", "deny"]),
        action_local_preference=dict(type="int"),
        action_med=dict(type="int"),
        action_nexthop=dict(type="str"),
        action_origin=dict(type="str", choices=["igp", "egp", "incomplete"]),
        action_as_path_limit=dict(type="int"),
        action_as_path_type=dict(
            type="str", choices=["none", "remove", "prepend", "remove-and-prepend"]
        ),
        action_as_path_prepend_times=dict(type="int"),
        action_community_type=dict(
            type="str",
            choices=["none", "remove-all", "remove-regex", "append", "overwrite"],
        ),
        action_community_modifier=dict(type="str"),
        action_community_argument=dict(type="str"),
        action_extended_community_type=dict(type="str"),
        action_extended_community_argument=dict(type="str"),
        action_dampening=dict(type="str"),
        action_weight=dict(type="int"),
        address_prefix=dict(type="list", elements="dict"),
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
        "match_afi": module.params["match_afi"],
        "match_safi": module.params["match_safi"],
        "match_route_table": module.params["match_route_table"],
        "match_nexthop": module.params["match_nexthop"],
        "match_from_peer": module.params["match_from_peer"],
        "match_med": module.params["match_med"],
        "match_as_path_regex": module.params["match_as_path_regex"],
        "match_community_regex": module.params["match_community_regex"],
        "match_extended_community_regex": module.params[
            "match_extended_community_regex"
        ],
        "used_by": module.params["used_by"],
        "action": module.params["action"],
        "action_local_preference": module.params["action_local_preference"],
        "action_med": module.params["action_med"],
        "action_nexthop": module.params["action_nexthop"],
        "action_origin": module.params["action_origin"],
        "action_as_path_limit": module.params["action_as_path_limit"],
        "action_as_path_type": module.params["action_as_path_type"],
        "action_as_path_prepend_times": module.params["action_as_path_prepend_times"],
        "action_community_type": module.params["action_community_type"],
        "action_community_modifier": module.params["action_community_modifier"],
        "action_community_argument": module.params["action_community_argument"],
        "action_extended_community_type": module.params[
            "action_extended_community_type"
        ],
        "action_extended_community_argument": module.params[
            "action_extended_community_argument"
        ],
    }
    # Add the correct rule type.
    if module.params["type"] == "import":
        spec["action_dampening"] = module.params["action_dampening"]
        spec["action_weight"] = module.params["action_weight"]
        obj = BgpPolicyImportRule(**spec)
    else:
        obj = BgpPolicyExportRule(**spec)

    # Since address_prefix can legitimately be empty, only process it if non-empty
    if module.params["address_prefix"] is not None:
        # Handle address prefixes.
        for x in module.params["address_prefix"]:
            if "name" not in x:
                module.fail_json(
                    msg='Address prefix dict requires "name": {0}'.format(x)
                )
            obj.add(
                BgpPolicyAddressPrefix(
                    to_text(x["name"], encoding="utf-8", errors="surrogate_or_strict"),
                    None if x.get("exact") is None else module.boolean(x["exact"]),
                )
            )

    listing = bgp.findall(obj.__class__)
    bgp.add(obj)

    # Apply the state.
    resp = helper.apply_state(obj, listing, module)

    # Optional commit.
    if resp["changed"] and module.params["commit"]:
        helper.commit(module)

    resp["msg"] = "done"
    module.exit_json(**resp)


if __name__ == "__main__":
    main()
