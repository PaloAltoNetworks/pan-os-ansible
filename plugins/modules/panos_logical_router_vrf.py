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
module: panos_logical_router_vrf
short_description: Manage Logical Router VRFs
description:
    - Manage PANOS Logical Router VRFs.
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
            - Name of the Logical Router
        type: str
        required: true
    name:
        description:
            - Name of VRF
        type: str
    interface:
        description:
            - List of interface names
        type: list
        elements: str
    ad_static:
        description:
            - Administrative distance for this protocol
        type: int
    ad_static_ipv6:
        description:
            - Administrative distance for this protocol
        type: int
    ad_ospf_inter:
        description:
            - Administrative distance for this protocol
        type: int
    ad_ospf_intra:
        description:
            - Administrative distance for this protocol
        type: int
    ad_ospf_ext:
        description:
            - Administrative distance for this protocol
        type: int
    ad_ospfv3_inter:
        description:
            - Administrative distance for this protocol
        type: int
    ad_ospfv3_intra:
        description:
            - Administrative distance for this protocol
        type: int
    ad_ospfv3_ext:
        description:
            - Administrative distance for this protocol
        type: int
    ad_bgp_internal:
        description:
            - Administrative distance for this protocol
        type: int
    ad_bgp_external:
        description:
            - Administrative distance for this protocol
        type: int
    ad_bgp_local:
        description:
            - Administrative distance for this protocol
        type: int
    ad_rip:
        description:
            - Administrative distance for this protocol
        type: int
    bgp_enable:
        description:
            - Enable BGP
        type: bool
    bgp_router_id:
        description:
            - Router id of this BGP instance
        type: str
    bgp_local_as:
        description:
            - Local AS number
        type: str
    bgp_install_route:
        description:
            - Populate BGP learned route to global route table
        type: bool
    bgp_enforce_first_as:
        description:
            - Enforce First AS
        type: bool
    bgp_fast_external_failover:
        description:
            - Immediately reset session if a link to a directly connected external peer goes down
        type: bool
    bgp_ecmp_multi_as:
        description:
            - Support multiple AS in ECMP
        type: bool
    bgp_default_local_preference:
        description:
            - Global Default Local Preference
        type: int
    bgp_graceful_shutdown:
        description:
            - Gracefully Shutdown BGP following RFC-8326
        type: bool
    bgp_always_advertise_network_route:
        description:
            - Always advertise network routes even if not present in RIB
        type: bool
    bgp_med_always_compare_med:
        description:
            - Always compare MEDs
        type: bool
    bgp_med_deterministic_med_comparison:
        description:
            - Deterministic MEDs comparison
        type: bool
    bgp_graceful_restart_enable:
        description:
            - Graceful-restart options enabled
        type: bool
    bgp_graceful_restart_stale_route_time:
        description:
            - Time to remove stale routes after peer restart
        type: int
    bgp_graceful_max_peer_restart_time:
        description:
            - Maximum of peer restart time accepted
        type: int
    bgp_graceful_local_restart_time:
        description:
            - Local restart time to advertise to peer
        type: int
    bgp_global_bfd:
        description:
            - BGP Global BFD Profile
        type: str
    bgp_redistribution_profile_ipv4_unicast:
        description:
            - IPv4 Redistribution Profile
        type: str
    bgp_redistribution_profile_ipv6_unicast:
        description:
            - IPv6 Redistribution Profile
        type: str
    ospf_enable:
        description:
            - Enable OSPF
        type: bool
    ospf_router_id:
        description:
            - Router ID in IP format (eg. 1.1.1.1)
        type: str
    ospf_global_bfd:
        description:
            - OSPF Global BFD Profile
        type: str
    ospf_spf_timer:
        description:
            - SPF timer setting
        type: str
    ospf_global_if_timer:
        description:
            - Global protocol timer setting
        type: str
    ospf_redistribution_profile:
        description:
            - Redistribution profile setting
        type: str
    ospf_rfc1583:
        description:
            - RFC 1583 compatibility
        type: bool
    ospf_graceful_restart_enable:
        description:
            - Enable OSPF graceful restart
        type: bool
    ospf_graceful_restart_grace_period:
        description:
            - Graceful restart period
        type: int
    ospf_graceful_restart_helper_enable:
        description:
            - Graceful restart helper enable
        type: bool
    ospf_graceful_restart_strict_lsa_checking:
        description:
            - Graceful restart strict lsa checking
        type: bool
    ospf_graceful_restart_max_neighbor_restart_time:
        description:
            - Graceful restart neighbor restart time
        type: int
    ospfv3_enable:
        description:
            - Enable OSPFv3
        type: bool
    ospfv3_router_id:
        description:
            - Router ID in IP format (eg. 1.1.1.1)
        type: str
    ospfv3_global_bfd:
        description:
            - OSPFv3 Global BFD Profile
        type: str
    ospfv3_spf_timer:
        description:
            - SPF timer setting
        type: str
    ospfv3_global_if_timer:
        description:
            - Global protocol timer setting
        type: str
    ospfv3_redistribution_profile:
        description:
            - Redistribution profile setting
        type: str
    ospfv3_disable_transit_traffic:
        description:
            - Disable R-Bit and v6-Bit
        type: bool
    ospfv3_graceful_restart_enable:
        description:
            - Enable OSPFv3 graceful restart
        type: bool
    ospfv3_graceful_restart_grace_period:
        description:
            - Graceful restart period
        type: int
    ospfv3_graceful_restart_helper_enable:
        description:
            - Graceful restart helper enable
        type: bool
    ospfv3_graceful_restart_strict_lsa_checking:
        description:
            - Graceful restart strict lsa checking
        type: bool
    ospfv3_graceful_restart_max_neighbor_restart_time:
        description:
            - Graceful restart neighbor restart time
        type: int
    rib_filter_ipv4_static:
        description:
            - IPv4 static route map
        type: str
    rib_filter_ipv4_bgp:
        description:
            - IPv4 BGP route map
        type: str
    rib_filter_ipv4_ospf:
        description:
            - IPv4 OSPF route map
        type: str
    rib_filter_ipv6_static:
        description:
            - IPv6 static route map
        type: str
    rib_filter_ipv6_bgp:
        description:
            - IPv6 BGP route map
        type: str
    rib_filter_ipv6_ospfv3:
        description:
            - IPv6 OSPFv3 route map
        type: str
    ecmp_enable:
        description:
            - Enable Equal Cost Multipath
        type: bool
    ecmp_symmetric_return:
        description:
            - Allows return packets to egress out of the ingress interface of the flow
        type: bool
    ecmp_strict_source_path:
        description:
            - Force VPN traffic to exit interface that the source-ip belongs to
        type: bool
    ecmp_max_path:
        description:
            - Maximum number of ECMP paths supported, change this configuration will result in a virtual router restart
        type: int
    ecmp_algorithm:
        description:
            - Load balancing algorithm
        type: str
    ecmp_algorithm_src_only:
        description:
            - Only use source address for hash
        type: bool
    ecmp_algorithm_use_port:
        description:
            - Use source/destination port for hash
        type: bool
    ecmp_algorithm_hash_seed:
        description:
            - User-specified hash seed
        type: int
"""

EXAMPLES = """
- name: Add ethernet1/1 to VRF "default" on logical router "default"
  paloaltonetworks.panos.panos_logical_router_vrf:
    provider: '{{ provider }}'
    logical_router: default
    name: default
    interfaces:
      - ethernet1/1

- name: Enable BGP
  paloaltonetworks.panos.panos_logical_router_vrf:
    provider: '{{ device }}'
    logical_router: default
    name: default
    bgp_enable: true
    bgp_router_id: 10.10.10.10
    bgp_local_as: 65500
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
        sdk_cls=("network", "Vrf"),
        parents=(("network", "LogicalRouter", "logical_router"),),
        sdk_params=dict(
            # Note; the bellow attributes were mapped automatically from the arg specification within pan-os-python
            #  using AI
            # --- General ---
            name=dict(type="str", required=True),
            interface=dict(type="list", elements="str"),
            # --- Administrative Distance (AD) ---
            ad_static=dict(type="int"),
            ad_static_ipv6=dict(type="int"),
            ad_ospf_inter=dict(type="int"),
            ad_ospf_intra=dict(type="int"),
            ad_ospf_ext=dict(type="int"),
            ad_ospfv3_inter=dict(type="int"),
            ad_ospfv3_intra=dict(type="int"),
            ad_ospfv3_ext=dict(type="int"),
            ad_bgp_internal=dict(type="int"),
            ad_bgp_external=dict(type="int"),
            ad_bgp_local=dict(type="int"),
            ad_rip=dict(type="int"),
            # --- BGP Configuration ---
            bgp_enable=dict(type="bool"),
            bgp_router_id=dict(type="str"),
            bgp_local_as=dict(type="str"),
            bgp_install_route=dict(type="bool"),
            bgp_enforce_first_as=dict(type="bool"),
            bgp_fast_external_failover=dict(type="bool"),
            bgp_ecmp_multi_as=dict(type="bool"),
            bgp_default_local_preference=dict(type="int"),
            bgp_graceful_shutdown=dict(type="bool"),
            bgp_always_advertise_network_route=dict(type="bool"),
            bgp_med_always_compare_med=dict(type="bool"),
            bgp_med_deterministic_med_comparison=dict(type="bool"),
            bgp_graceful_restart_enable=dict(type="bool"),
            bgp_graceful_restart_stale_route_time=dict(type="int"),
            bgp_graceful_max_peer_restart_time=dict(type="int"),
            bgp_graceful_local_restart_time=dict(type="int"),
            bgp_global_bfd=dict(type="str"),
            bgp_redistribution_profile_ipv4_unicast=dict(type="str"),
            bgp_redistribution_profile_ipv6_unicast=dict(type="str"),
            # --- OSPF Configuration ---
            ospf_enable=dict(type="bool"),
            ospf_router_id=dict(type="str"),
            ospf_global_bfd=dict(type="str"),
            ospf_spf_timer=dict(type="str"),
            ospf_global_if_timer=dict(type="str"),
            ospf_redistribution_profile=dict(type="str"),
            ospf_rfc1583=dict(type="bool"),
            ospf_graceful_restart_enable=dict(type="bool"),
            ospf_graceful_restart_grace_period=dict(type="int"),
            ospf_graceful_restart_helper_enable=dict(type="bool"),
            ospf_graceful_restart_strict_lsa_checking=dict(type="bool"),
            ospf_graceful_restart_max_neighbor_restart_time=dict(type="int"),
            # --- OSPFv3 Configuration ---
            ospfv3_enable=dict(type="bool"),
            ospfv3_router_id=dict(type="str"),
            ospfv3_global_bfd=dict(type="str"),
            ospfv3_spf_timer=dict(type="str"),
            ospfv3_global_if_timer=dict(type="str"),
            ospfv3_redistribution_profile=dict(type="str"),
            ospfv3_disable_transit_traffic=dict(type="bool"),
            ospfv3_graceful_restart_enable=dict(type="bool"),
            ospfv3_graceful_restart_grace_period=dict(type="int"),
            ospfv3_graceful_restart_helper_enable=dict(type="bool"),
            ospfv3_graceful_restart_strict_lsa_checking=dict(type="bool"),
            ospfv3_graceful_restart_max_neighbor_restart_time=dict(type="int"),
            # --- RIB Filters ---
            rib_filter_ipv4_static=dict(type="str"),
            rib_filter_ipv4_bgp=dict(type="str"),
            rib_filter_ipv4_ospf=dict(type="str"),
            rib_filter_ipv6_static=dict(type="str"),
            rib_filter_ipv6_bgp=dict(type="str"),
            rib_filter_ipv6_ospfv3=dict(type="str"),
            # --- ECMP Configuration ---
            ecmp_enable=dict(type="bool"),
            ecmp_symmetric_return=dict(type="bool"),
            ecmp_strict_source_path=dict(type="bool"),
            ecmp_max_path=dict(type="int"),
            ecmp_algorithm=dict(type="str"),
            ecmp_algorithm_src_only=dict(type="bool"),
            ecmp_algorithm_use_port=dict(type="bool"),
            ecmp_algorithm_hash_seed=dict(type="int"),
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
