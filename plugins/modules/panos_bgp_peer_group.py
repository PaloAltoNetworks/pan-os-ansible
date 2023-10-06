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
module: panos_bgp_peer_group
short_description: Manage a BGP Peer Group
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
    aggregated_confed_as_path:
        description:
            - The peers understand Aggregated Confederation AS Path.
        type: bool
    enable:
        description:
            - Enable BGP peer group.
        type: bool
        default: True
    export_nexthop:
        description:
            - Export locally resolved nexthop.
        type: str
        choices:
            - original
            - resolve
            - use-self
        default: 'resolve'
    import_nexthop:
        description:
            - I(type=ebgp) only; override nexthop with peer address.
        type: str
        choices:
            - original
            - use-peer
        default: 'original'
    name:
        description:
            - Name of the BGP peer group.
        type: str
    remove_private_as:
        description:
            - I(type=ebgp) only; remove private AS when exporting route.
        type: bool
    soft_reset_with_stored_info:
        description:
            - Enable soft reset with stored info.
        type: bool
    type:
        description:
            - Peer group type.
        type: str
        choices:
            - ebgp
            - ibgp
            - ebgp-confed
            - ibgp-confed
        default: 'ebgp'
    vr_name:
        description:
            - Name of the virtual router, it must already exist.  See M(paloaltonetworks.panos.panos_virtual_router).
        type: str
        default: 'default'
"""

EXAMPLES = """
- name: Create BGP Peer Group
  paloaltonetworks.panos.panos_bgp_peer_group:
    provider: '{{ provider }}'
    name: 'peer-group-1'
    enable: true
    aggregated_confed_as_path: true
    soft_reset_with_stored_info: false
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
        sdk_cls=("network", "BgpPeerGroup"),
        sdk_params=dict(
            name=dict(required=True),
            enable=dict(default=True, type="bool"),
            aggregated_confed_as_path=dict(type="bool"),
            soft_reset_with_stored_info=dict(type="bool"),
            type=dict(
                default="ebgp", choices=["ebgp", "ibgp", "ebgp-confed", "ibgp-confed"]
            ),
            export_nexthop=dict(
                default="resolve", choices=["original", "resolve", "use-self"]
            ),
            import_nexthop=dict(default="original", choices=["original", "use-peer"]),
            remove_private_as=dict(type="bool"),
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
