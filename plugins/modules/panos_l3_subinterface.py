#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright 2019 Palo Alto Networks, Inc
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
module: panos_l3_subinterface
short_description: configure layer3 subinterface
description:
    - Configure a layer3 subinterface.
author: "Garfield Lee Freeman (@shinmog)"
version_added: "2.8"
requirements:
    - pan-python
    - pandevice >= 0.8.0
notes:
    - Panorama is supported.
    - Checkmode is supported.
    - If the PAN-OS device is a firewall and I(vsys) is not specified, then
      the vsys will default to I(vsys=vsys1).
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.state
    - paloaltonetworks.panos.fragments.vsys_import
    - paloaltonetworks.panos.fragments.template_only
options:
    name:
        description:
            - Name of the interface to configure.
        required: true
    tag:
        description:
            - Tag (vlan id) for the interface
        required: true
        type: int
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
        type: bool
        default: true
    create_default_route:
        description:
            - Whether or not to add default route with router learned via DHCP.
        type: bool
    dhcp_default_route_metric:
        description:
            - Metric for the DHCP default route.
        type: int
    zone_name:
        description:
            - Name of the zone for the interface.
            - If the zone does not exist it is created.
    vr_name:
        description:
            - Virtual router to add this interface to.
'''

EXAMPLES = '''
# Create ethernet1/1.5 as DHCP.
- name: enable DHCP client on ethernet1/1.5 in zone public
  panos_l3_subinterface:
    provider: '{{ provider }}'
    name: "ethernet1/1.5"
    tag: 1
    create_default_route: True
    zone_name: "public"
    create_default_route: "yes"

# Update ethernet1/2.7 with a static IP address in zone dmz.
- name: ethernet1/2.7 as static in zone dmz
  panos_l3_subinterface:
    provider: '{{ provider }}'
    name: "ethernet1/2.7"
    tag: 7
    enable_dhcp: false
    ip: ["10.1.1.1/24"]
    zone_name: "dmz"
'''

RETURN = '''
# Default return values
'''

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection


try:
    from pandevice.network import AggregateInterface
    from pandevice.network import EthernetInterface
    from pandevice.network import Layer3Subinterface
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
            name=dict(required=True),
            tag=dict(required=True, type='int'),
            ip=dict(type='list'),
            ipv6_enabled=dict(type='bool'),
            management_profile=dict(),
            mtu=dict(type='int'),
            adjust_tcp_mss=dict(type='bool'),
            netflow_profile=dict(),
            comment=dict(),
            ipv4_mss_adjust=dict(type='int'),
            ipv6_mss_adjust=dict(type='int'),
            enable_dhcp=dict(type='bool', default=True),
            create_default_route=dict(type='bool', default=False),
            dhcp_default_route_metric=dict(type='int'),
            zone_name=dict(),
            vr_name=dict(default='default'),
        ),
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # Verify libs are present, get the parent object.
    parent = helper.get_pandevice_parent(module)

    # Get the object params.
    spec = {
        'name': module.params['name'],
        'tag': module.params['tag'],
        'ip': module.params['ip'],
        'ipv6_enabled': module.params['ipv6_enabled'],
        'management_profile': module.params['management_profile'],
        'mtu': module.params['mtu'],
        'adjust_tcp_mss': module.params['adjust_tcp_mss'],
        'netflow_profile': module.params['netflow_profile'],
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
    vr_name = module.params['vr_name']
    vsys = module.params['vsys']

    # Sanity check.
    if '.' not in spec['name']:
        module.fail_json(msg='Interface name does not have "." in it')

    # check on EthernetInterface or AggregateInterface
    parent_iname = spec['name'].split('.')[0]

    # Retrieve the current config.
    if parent_iname.startswith('ae'):
        parent_eth = AggregateInterface(parent_iname)
    else:
        parent_eth = EthernetInterface(parent_iname)

    parent.add(parent_eth)
    try:
        parent_eth.refresh()
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    if parent_eth.mode != 'layer3':
        module.fail_json(msg='{0} mode is {1}, not layer3'.format(parent_eth.name, parent_eth.mode))

    interfaces = parent_eth.findall(Layer3Subinterface)

    # Build the object based on the user spec.
    eth = Layer3Subinterface(**spec)
    parent_eth.add(eth)

    # Which action should we take on the interface?
    changed = False
    reference_params = {
        'refresh': True,
        'update': not module.check_mode,
        'return_type': 'bool',
    }
    if state == 'present':
        for item in interfaces:
            if item.name != eth.name:
                continue
            # Interfaces have children, so don't compare them.
            if not item.equal(eth, compare_children=False):
                changed = True
                eth.extend(item.children)
                if not module.check_mode:
                    try:
                        eth.apply()
                    except PanDeviceError as e:
                        module.fail_json(msg='Failed apply: {0}'.format(e))
            break
        else:
            changed = True
            if not module.check_mode:
                try:
                    eth.create()
                except PanDeviceError as e:
                    module.fail_json(msg='Failed create: {0}'.format(e))

        # Set references.
        try:
            changed |= eth.set_vsys(vsys, **reference_params)
            changed |= eth.set_zone(zone_name, mode=parent_eth.mode, **reference_params)
            changed |= eth.set_virtual_router(vr_name, **reference_params)
        except PanDeviceError as e:
            module.fail_json(msg='Failed setref: {0}'.format(e))
    elif state == 'absent':
        # Remove references.
        try:
            changed |= eth.set_virtual_router(None, **reference_params)
            changed |= eth.set_zone(None, mode=parent_eth.mode, **reference_params)
            changed |= eth.set_vsys(None, **reference_params)
        except PanDeviceError as e:
            module.fail_json(msg='Failed setref: {0}'.format(e))

        # Remove the interface.
        if eth.name in [x.name for x in interfaces]:
            changed = True
            if not module.check_mode:
                try:
                    eth.delete()
                except PanDeviceError as e:
                    module.fail_json(msg='Failed delete: {0}'.format(e))

    # Done!
    module.exit_json(changed=changed, msg='Done')


if __name__ == '__main__':
    main()
