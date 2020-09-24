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

DOCUMENTATION = '''
---
module: panos_bgp
short_description: Configures Border Gateway Protocol (BGP)
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
    - paloaltonetworks.panos.fragments.enabled_state
    - paloaltonetworks.panos.fragments.deprecated_commit
options:
    enable:
        description:
            - Enable BGP.
        type: bool
        default: true
    router_id:
        description:
            - Router ID in IP format (eg. 1.1.1.1)
        type: str
    reject_default_route:
        description:
            - Reject default route.
        type: bool
        default: true
    allow_redist_default_route:
        description:
            - Allow redistribute default route to BGP.
        type: bool
        default: false
    install_route:
        description:
            - Populate BGP learned route to global route table.
        type: bool
        default: false
    ecmp_multi_as:
        description:
            - Support multiple AS in ECMP.
        type: bool
        default: false
    enforce_first_as:
        description:
            - Enforce First AS for EBGP.
        type: bool
        default: true
    local_as:
        description:
            - Local Autonomous System (AS) number.
        type: str
    global_bfd_profile:
        description:
            - Bidirectional Forwarding Detection (BFD) profile.
        type: str
    as_format:
        description:
            - AS format I('2-byte')/I('4-byte').
        type: str
        choices: ['2-byte', '4-byte']
        default: '2-byte'
    always_compare_med:
        description:
            - Always compare MEDs.
        type: bool
        default: false
    deterministic_med_comparison:
        description:
            - Deterministic MEDs comparison.
        type: bool
        default: true
    default_local_preference:
        description:
            - Default local preference.
        type: int
        default: 100
    graceful_restart_enable:
        description:
            - Enable graceful restart.
        type: bool
        default: true
    gr_stale_route_time:
        description:
            - Time to remove stale routes after peer restart (in seconds).
        type: int
    gr_local_restart_time:
        description:
            - Local restart time to advertise to peer (in seconds).
        type: int
    gr_max_peer_restart_time:
        description:
            - Maximum of peer restart time accepted (in seconds).
        type: int
    reflector_cluster_id:
        description:
            - Route reflector cluster ID.
        type: str
    confederation_member_as:
        description:
            - Confederation requires member-AS number.
        type: str
    aggregate_med:
        description:
            - Aggregate route only if they have same MED attributes.
        type: bool
        default: True
    vr_name:
        description:
            - Name of the virtual router; it must already exist.
        type: str
        default: "default"
'''

EXAMPLES = '''
- name: Configure and enable BGP
  panos_bgp:
    provider: '{{ provider }}'
    router_id: '1.1.1.1'
    local_as: '64512'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from panos.errors import PanDeviceError
    from panos.network import Bgp
    from panos.network import BgpRoutingOptions
    from panos.network import VirtualRouter
except ImportError:
    try:
        from pandevice.errors import PanDeviceError
        from pandevice.network import Bgp
        from pandevice.network import BgpRoutingOptions
        from pandevice.network import VirtualRouter
    except ImportError:
        pass


def setup_args():
    return dict(
        enable=dict(default=True, type='bool'),
        router_id=dict(type='str'),
        reject_default_route=dict(type='bool', default=True),
        allow_redist_default_route=dict(type='bool', default=False),
        install_route=dict(type='bool', default=False),
        ecmp_multi_as=dict(type='bool', default=False),
        enforce_first_as=dict(type='bool', default=True),
        local_as=dict(type='str'),
        global_bfd_profile=dict(type='str'),
        as_format=dict(type='str', default='2-byte', choices=['2-byte', '4-byte']),
        always_compare_med=dict(type='bool', default=False),
        deterministic_med_comparison=dict(type='bool', default=True),
        default_local_preference=dict(type='int', default=100),
        graceful_restart_enable=dict(type='bool', default=True),
        gr_stale_route_time=dict(type='int'),
        gr_local_restart_time=dict(type='int'),
        gr_max_peer_restart_time=dict(type='int'),
        reflector_cluster_id=dict(type='str'),
        confederation_member_as=dict(type='str'),
        aggregate_med=dict(type='bool', default=True),
        vr_name=dict(default='default'),
        commit=dict(type='bool', default=False),
    )


def main():
    helper = get_connection(
        template=True,
        template_stack=True,
        with_enabled_state=True,
        with_classic_provider_spec=True,
        argument_spec=setup_args(),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    parent = helper.get_pandevice_parent(module)

    # Other params.
    vr_name = module.params['vr_name']
    commit = module.params['commit']

    vr = VirtualRouter(vr_name)
    parent.add(vr)
    try:
        vr.refresh()
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))
    parent = vr

    listing = parent.findall(Bgp)

    # Generate the kwargs for network.Bgp.
    bgp_params = [
        'enable', 'router_id', 'reject_default_route', 'allow_redist_default_route',
        'install_route', 'ecmp_multi_as', 'enforce_first_as', 'local_as', 'global_bfd_profile'
    ]
    bgp_spec = dict((k, module.params[k]) for k in bgp_params)

    # Generate the kwargs for network.BgpRoutingOptions.
    bgp_routing_options_params = [
        'as_format', 'always_compare_med', 'deterministic_med_comparison',
        'default_local_preference', 'graceful_restart_enable',
        'gr_stale_route_time', 'gr_local_restart_time', 'gr_max_peer_restart_time',
        'reflector_cluster_id', 'confederation_member_as', 'aggregate_med',
    ]
    bgp_routing_options_spec = dict((k, module.params[k]) for k in bgp_routing_options_params)

    bgp = Bgp(**bgp_spec)
    bgp_routing_options = BgpRoutingOptions(**bgp_routing_options_spec)
    bgp.add(bgp_routing_options)
    parent.add(bgp)

    # Apply the state.
    changed, diff = helper.apply_state(bgp, listing, module, 'enable')

    if commit and changed:
        helper.commit(module)

    module.exit_json(msg='BGP configuration successful.', changed=changed, diff=diff)


if __name__ == '__main__':
    main()
