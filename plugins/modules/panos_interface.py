#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright 2016 Palo Alto Networks, Inc
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

DOCUMENTATION = '''
---
module: panos_interface
short_description: configure data-port network interfaces
description:
    - Configure data-port (DP) network interface. By default DP interfaces are static.
author:
    - Luigi Mori (@jtschichold)
    - Ivan Bojer (@ivanbojer)
    - Garfield Lee Freeman (@shinmog)
version_added: "2.3"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
    - pandevice >= 0.8.0
notes:
    - Checkmode is supported.
    - If the PAN-OS device is a firewall and I(vsys) is not specified, then
      the vsys will default to I(vsys=vsys1).
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.state
    - paloaltonetworks.panos.fragments.vsys_import
    - paloaltonetworks.panos.fragments.template_only
options:
    if_name:
        description:
            - Name of the interface to configure.
        required: true
    mode:
        description:
            - The interface mode.
        default: "layer3"
        choices:
            - layer3
            - layer2
            - virtual-wire
            - tap
            - ha
            - decrypt-mirror
            - aggregate-group
    ip:
        description:
            - List of static IP addresses.
        type: list
    ipv6_enabled:
        description:
            - Enable IPv6.
        type: bool
    management_profile:
        description:
            - Interface management profile name.
    mtu:
        description:
            - MTU for layer3 interface.
        type: int
    adjust_tcp_mss:
        description:
            - Adjust TCP MSS for layer3 interface.
        type: bool
    netflow_profile:
        description:
            - Netflow profile for layer3 interface.
    lldp_enabled:
        description:
            - Enable LLDP for layer2 interface.
    lldp_profile:
        description:
            - LLDP profile name for layer2 interface.
    netflow_profile_l2:
        description:
            - Netflow profile name for layer2 interface.
    link_speed:
        description:
            - Link speed.
        choices:
            - auto
            - 10
            - 100
            - 1000
    link_duplex:
        description:
            - Link duplex.
        choices:
            - auto
            - full
            - half
    link_state:
        description:
            - Link state.
        choices:
            - auto
            - up
            - down
    aggregate_group:
        description:
            - Aggregate interface name.
    comment:
        description:
            - Interface comment.
    ipv4_mss_adjust:
        description:
            - (7.1+) TCP MSS adjustment for IPv4.
        type: int
    ipv6_mss_adjust:
        description:
            - (7.1+) TCP MSS adjustment for IPv6.
        type: int
    enable_dhcp:
        description:
            - Enable DHCP on this interface.
        default: "true"
        type: bool
    create_default_route:
        description:
            - Whether or not to add default route with router learned via DHCP.
        default: "false"
        type: bool
    dhcp_default_route_metric:
        description:
            - Metric for the DHCP default route.
        type: int
    zone_name:
        description:
            - Name of the zone for the interface.
            - If the zone does not exist it is created.
            - If the zone already exists its mode should match I(mode).
    vlan_name:
        description:
            - The VLAN to put this interface in.
            - If the VLAN does not exist it is created.
            - Only specify this if I(mode=layer2).
    vr_name:
        description:
            - Name of the virtual router; it must already exist.
        default: "default"
    vsys_dg:
        description:
            - B(Deprecated)
            - Use I(vsys) to specify the vsys instead.
            - HORIZONTALLINE
            - Name of the vsys (if firewall) or device group (if panorama) to put this object.
    commit:
        description:
            - Commit if changed
        default: true
        type: bool
    operation:
        description:
            - B(Removed)
            - Use I(state) instead.
'''

EXAMPLES = '''
# Create ethernet1/1 as DHCP.
- name: enable DHCP client on ethernet1/1 in zone public
  panos_interface:
    provider: '{{ provider }}'
    if_name: "ethernet1/1"
    zone_name: "public"
    create_default_route: "yes"

# Update ethernet1/2 with a static IP address in zone dmz.
- name: ethernet1/2 as static in zone dmz
  panos_interface:
    provider: '{{ provider }}'
    if_name: "ethernet1/2"
    mode: "layer3"
    ip: ["10.1.1.1/24"]
    enable_dhcp: false
    zone_name: "dmz"
'''

RETURN = '''
# Default return values
'''

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import get_exception
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection, eltostr


try:
    from pandevice.network import EthernetInterface
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def main():
    helper = get_connection(
        vsys_importable=True,
        template=True,
        with_classic_provider_spec=True,
        with_state=True,
        min_pandevice_version=(0, 8, 0),
        argument_spec=dict(
            if_name=dict(required=True),
            mode=dict(
                default='layer3',
                choices=[
                    'layer3', 'layer2', 'virtual-wire', 'tap', 'ha',
                    'decrypt-mirror', 'aggregate-group',
                ],
            ),
            ip=dict(type='list'),
            ipv6_enabled=dict(type='bool'),
            management_profile=dict(),
            mtu=dict(type='int'),
            adjust_tcp_mss=dict(type='bool'),
            netflow_profile=dict(),
            lldp_enabled=dict(),
            lldp_profile=dict(),
            netflow_profile_l2=dict(),
            link_speed=dict(choices=['auto', '10', '100', '1000']),
            link_duplex=dict(choices=['auto', 'full', 'half']),
            link_state=dict(choices=['auto', 'up', 'down']),
            aggregate_group=dict(),
            comment=dict(),
            ipv4_mss_adjust=dict(type='int'),
            ipv6_mss_adjust=dict(type='int'),
            enable_dhcp=dict(type='bool', default=True),
            create_default_route=dict(type='bool', default=False),
            dhcp_default_route_metric=dict(type='int'),
            zone_name=dict(),
            vr_name=dict(default='default'),
            vlan_name=dict(),
            commit=dict(type='bool', default=True),

            # TODO(gfreeman) - remove this in 2.12.
            vsys_dg=dict(),

            # TODO(gfreeman) - remove in the next release.
            operation=dict(),
        ),
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # TODO(gfreeman) - remove in the next release.
    if module.params['operation'] is not None:
        module.fail_json(msg='Operation has been removed; use "state"')

    # Get the object params.
    spec = {
        'name': module.params['if_name'],
        'mode': module.params['mode'],
        'ip': module.params['ip'],
        'ipv6_enabled': module.params['ipv6_enabled'],
        'management_profile': module.params['management_profile'],
        'mtu': module.params['mtu'],
        'adjust_tcp_mss': module.params['adjust_tcp_mss'],
        'netflow_profile': module.params['netflow_profile'],
        'lldp_enabled': module.params['lldp_enabled'],
        'lldp_profile': module.params['lldp_profile'],
        'netflow_profile_l2': module.params['netflow_profile_l2'],
        'link_speed': module.params['link_speed'],
        'link_duplex': module.params['link_duplex'],
        'link_state': module.params['link_state'],
        'aggregate_group': module.params['aggregate_group'],
        'comment': module.params['comment'],
        'ipv4_mss_adjust': module.params['ipv4_mss_adjust'],
        'ipv6_mss_adjust': module.params['ipv6_mss_adjust'],
        'enable_dhcp': True if module.params['enable_dhcp'] else None,
        # 'create_dhcp_default_route': set below
        'dhcp_default_route_metric': module.params['dhcp_default_route_metric'],
    }

    if module.params['create_default_route']:
        spec['create_dhcp_default_route'] = True
    elif spec['enable_dhcp']:
        spec['create_dhcp_default_route'] = False
    else:
        spec['create_dhcp_default_route'] = None

    # Get other info.
    state = module.params['state']
    zone_name = module.params['zone_name']
    vlan_name = module.params['vlan_name']
    vr_name = module.params['vr_name'] if module.params['vr_name'] else None
    vsys = module.params['vsys']
    vsys_dg = module.params['vsys_dg']

    # TODO(gfreeman) - Remove vsys_dg in 2.12, as well as this code chunk.
    # In the mean time, we'll need to do this special handling.
    if vsys_dg is not None:
        module.deprecate('Param "vsys_dg" is deprecated, use "vsys"', '2.12')
        if vsys is None:
            vsys = vsys_dg
        else:
            msg = [
                'Params "vsys" and "vsys_dg" both given',
                'Specify one or the other, not both.',
            ]
            module.fail_json(msg='.  '.join(msg))
    elif vsys is None:
        # TODO(gfreeman) - v2.12, just set the default for vsys to 'vsys1'.
        vsys = 'vsys1'

    module.params['vsys'] = vsys

    # Verify libs are present, get the parent object.
    parent = helper.get_pandevice_parent(module)

    # Retrieve the current config.
    try:
        interfaces = EthernetInterface.refreshall(
            parent, add=False, matching_vsys=False)
    except PanDeviceError:
        e = get_exception()
        module.fail_json(msg=e.message)

    # Build the object based on the user spec.
    eth = EthernetInterface(**spec)
    parent.add(eth)

    # Which action should we take on the interface?
    changed = False
    diff = None
    reference_params = {
        'refresh': True,
        'update': not module.check_mode,
        'return_type': 'bool',
    }
    if state == 'present':
        for item in interfaces:
            if item.name != eth.name:
                continue
            diff = dict(
                before=eltostr(item)
            )
            # Interfaces have children, so don't compare them.
            if not item.equal(eth, compare_children=False):
                changed = True
                eth.extend(item.children)
                diff['after'] = eltostr(eth)
                if not module.check_mode:
                    try:
                        eth.apply()
                    except PanDeviceError as e:
                        module.fail_json(msg='Failed apply: {0}'.format(e))
            break
        else:
            changed = True
            diff = dict(
                before="",
                after=eltostr(eth)
            )
            if not module.check_mode:
                try:
                    eth.create()
                except PanDeviceError as e:
                    module.fail_json(msg='Failed create: {0}'.format(e))

        # Set references.
        try:
            changed |= eth.set_vsys(vsys, **reference_params)
            changed |= eth.set_zone(zone_name, mode=eth.mode, **reference_params)
            changed |= eth.set_vlan(vlan_name, **reference_params)
            changed |= eth.set_virtual_router(vr_name, **reference_params)
        except PanDeviceError as e:
            module.fail_json(msg='Failed setref: {0}'.format(e))
    elif state == 'absent':
        # Remove references.
        try:
            changed |= eth.set_virtual_router(None, **reference_params)
            changed |= eth.set_vlan(None, **reference_params)
            changed |= eth.set_zone(None, mode=eth.mode, **reference_params)
            changed |= eth.set_vsys(None, **reference_params)
        except PanDeviceError as e:
            module.fail_json(msg='Failed setref: {0}'.format(e))

        # Remove the interface.
        if eth.name in [x.name for x in interfaces]:
            changed = True
            diff = dict(
                before=eltostr(eth),
                after=""
            )
            if not module.check_mode:
                try:
                    eth.delete()
                except PanDeviceError as e:
                    module.fail_json(msg='Failed delete: {0}'.format(e))

    # Commit if we were asked to do so.
    if changed and module.params['commit']:
        helper.commit(module)

    # Done!
    module.exit_json(changed=changed, diff=diff, msg='Done')


if __name__ == '__main__':
    main()
