#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

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
module: panos_vlan_interface
short_description: configure VLAN interfaces
description:
    - Configure VLAN interfaces.
author: "Garfield Lee Freeman (@shinmog)"
version_added: "2.8"
requirements:
    - pan-python
    - pandevice
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
    name:
        description:
            - Name of the interface to configure.
            - This should be in the format "vlan.<some_number>".
        required: true
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
    create_dhcp_default_route:
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
            - If the zone already exists it should be I(mode=layer3).
    vlan_name:
        description:
            - The VLAN to put this interface in.
            - If the VLAN does not exist it is created.
    vr_name:
        description:
            - Name of the virtual router
'''

EXAMPLES = '''
# Create vlan.2 as DHCP
- name: enable DHCP client on ethernet1/1 in zone public
  panos_vlan_interface:
    provider: '{{ provider }}'
    name: "vlan.2"
    zone_name: "public"
    enable_dhcp: true
    create_default_route: true

# Set vlan.7 with a static IP
- name: Configure vlan.7
  panos_vlan_interface:
    provider: '{{ provider }}'
    name: "vlan.7"
    ip: ["10.1.1.1/24"]
    management_profile: "allow ping"
    vlan_name: "dmz"
    zone_name: "L3-untrust"
    vr_name: "default"
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
    from pandevice.network import Vlan
    from pandevice.network import VlanInterface
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def main():
    helper = get_connection(
        vsys_importable=True,
        template=True,
        with_classic_provider_spec=True,
        with_state=True,
        min_pandevice_version=(0, 9, 0),
        argument_spec=dict(
            name=dict(required=True),
            ip=dict(type='list'),
            ipv6_enabled=dict(type='bool'),
            management_profile=dict(),
            mtu=dict(type='int'),
            adjust_tcp_mss=dict(type='bool'),
            netflow_profile=dict(),
            comment=dict(),
            ipv4_mss_adjust=dict(type='int'),
            ipv6_mss_adjust=dict(type='int'),
            enable_dhcp=dict(type='bool'),
            create_dhcp_default_route=dict(type='bool'),
            dhcp_default_route_metric=dict(type='int'),
            zone_name=dict(),
            vlan_name=dict(),
            vr_name=dict(),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # Get the object params.
    spec = {
        'name': module.params['name'],
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
        'create_dhcp_default_route': True if module.params['create_dhcp_default_route'] else None,
        'dhcp_default_route_metric': module.params['dhcp_default_route_metric'],
    }

    # Get other info.
    zone_name = module.params['zone_name']
    vlan_name = module.params['vlan_name']
    vr_name = module.params['vr_name']
    vsys = module.params['vsys']

    if vsys is None:
        vsys = 'vsys1'
        module.params['vsys'] = vsys

    # Verify libs are present, get the parent object.
    parent = helper.get_pandevice_parent(module)

    # Retrieve the current config.
    try:
        listing = VlanInterface.refreshall(
            parent, add=False, matching_vsys=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    # Build the object based on the user spec.
    obj = VlanInterface(**spec)
    parent.add(obj)

    # Which action should we take on the interface?
    changed = False
    reference_params = {
        'refresh': True,
        'update': not module.check_mode,
        'return_type': 'bool',
    }
    if module.params['state'] == 'present':
        for item in listing:
            if item.name != obj.name:
                continue
            # Interfaces have children, so don't compare them.
            if not item.equal(obj, compare_children=False):
                changed = True
                obj.extend(item.children)
                if not module.check_mode:
                    try:
                        obj.apply()
                    except PanDeviceError as e:
                        module.fail_json(msg='Failed apply: {0}'.format(e))
            break
        else:
            changed = True
            if not module.check_mode:
                try:
                    obj.create()
                except PanDeviceError as e:
                    module.fail_json(msg='Failed create: {0}'.format(e))

        # Set references.
        try:
            changed |= obj.set_vsys(vsys, **reference_params)
            changed |= obj.set_vlan_interface(vlan_name, **reference_params)
            changed |= obj.set_zone(zone_name, mode='layer3', **reference_params)
            changed |= obj.set_virtual_router(vr_name, **reference_params)
        except PanDeviceError as e:
            module.fail_json(msg='Failed setref: {0}'.format(e))
    elif module.params['state'] == 'absent':
        # Remove references.
        try:
            changed |= obj.set_virtual_router(None, **reference_params)
            changed |= obj.set_zone(None, mode='layer3', **reference_params)
            changed |= obj.set_vlan_interface(None, **reference_params)
            changed |= obj.set_vsys(None, **reference_params)
        except PanDeviceError as e:
            module.fail_json(msg='Failed setref: {0}'.format(e))

        # Remove the interface.
        if obj.name in [x.name for x in listing]:
            changed = True
            if not module.check_mode:
                try:
                    obj.delete()
                except PanDeviceError as e:
                    module.fail_json(msg='Failed delete: {0}'.format(e))

    # Done!
    module.exit_json(changed=changed, msg='done')


if __name__ == '__main__':
    main()
