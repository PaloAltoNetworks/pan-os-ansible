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
module: panos_aggregate_interface
short_description: configure aggregate network interfaces
description:
    - Configure aggregate network interfaces on PanOS
author:
    - Heiko Burghardt (@odysseus107)
version_added: "2.9"
requirements:
    - pan-python can be obtained from PyPi U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPi U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is supported.
    - Panorama is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.vsys_import
    - paloaltonetworks.panos.fragments.template_only
    - paloaltonetworks.panos.fragments.state
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
            - ha
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
            - MTU for aggregate interface.
        type: int
    adjust_tcp_mss:
        description:
            - Adjust TCP MSS.
        type: bool
    netflow_profile:
        description:
            - Netflow profile for aggregate interface.
    lldp_enabled:
        description:
            - (Layer2) Enable LLDP
        type: bool
    lldp_profile:
        description:
            - (Layer2) Reference to an lldp profile
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
            - Enable DHCP on this interface
        type: bool
    create_dhcp_default_route:
        description:
            - Create default route pointing to default gateway provided by server
        type: bool
    dhcp_default_route_metric:
        description:
            - Metric for the DHCP default route
        type: int
    zone_name:
        description:
            - The zone to put this interface into.
    vr_name:
        description:
            - The virtual router to associate with this interface.
    commit:
        description:
            - Commit if changed
        default: true
        type: bool
'''

EXAMPLES = '''
# Create ae1 interface.
- name: create ae1 interface with IP in untrust zone
  panos_aggregate_interface:
    provider: '{{ provider }}'
    if_name: "ae1"
    ip: '[ "192.168.0.1" ]'
    zone_name: 'untrust'
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
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def main():
    helper = get_connection(
        vsys_importable=True,
        template=True,
        with_classic_provider_spec=True,
        with_state=True,
        min_pandevice_version=(0, 13, 0),
        argument_spec=dict(
            if_name=dict(required=True),
            mode=dict(
                default='layer3',
                choices=['layer3', 'layer2', 'virtual-wire', 'ha'],
            ),
            ip=dict(type='list'),
            ipv6_enabled=dict(type='bool'),
            management_profile=dict(),
            mtu=dict(type='int'),
            adjust_tcp_mss=dict(type='bool'),
            netflow_profile=dict(),
            lldp_enabled=dict(type='bool'),
            lldp_profile=dict(),
            comment=dict(),
            ipv4_mss_adjust=dict(type='int'),
            ipv6_mss_adjust=dict(type='int'),
            enable_dhcp=dict(type='bool'),
            create_dhcp_default_route=dict(type='bool'),
            dhcp_default_route_metric=dict(type='int'),
            zone_name=dict(),
            vr_name=dict(default='default'),
            commit=dict(type='bool', default=True),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

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
        'comment': module.params['comment'],
        'ipv4_mss_adjust': module.params['ipv4_mss_adjust'],
        'ipv6_mss_adjust': module.params['ipv6_mss_adjust'],
        'enable_dhcp': module.params['enable_dhcp'],
        'create_dhcp_default_route': module.params['create_dhcp_default_route'],
        'dhcp_default_route_metric': module.params['dhcp_default_route_metric'],
    }

    # Get other info.
    state = module.params['state']
    zone_name = module.params['zone_name']
    vr_name = module.params['vr_name']
    vsys = module.params['vsys']
    commit = module.params['commit']

    # Verify libs are present, get the parent object.
    parent = helper.get_pandevice_parent(module)

    # Retrieve the current config.
    try:
        interfaces = AggregateInterface.refreshall(
            parent, add=False, matching_vsys=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    # Build the object based on the user spec.
    obj = AggregateInterface(**spec)
    parent.add(obj)

    # Which action should we take on the interface?
    changed = False
    reference_params = {
        'refresh': True,
        'update': not module.check_mode,
        'return_type': 'bool',
    }
    if state == 'present':
        for item in interfaces:
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
            changed |= obj.set_zone(zone_name, mode=obj.mode, **reference_params)
            changed |= obj.set_virtual_router(vr_name, **reference_params)
        except PanDeviceError as e:
            module.fail_json(msg='Failed setref: {0}'.format(e))
    elif state == 'absent':
        # Remove references.
        try:
            changed |= obj.set_virtual_router(None, **reference_params)
            changed |= obj.set_zone(None, mode=obj.mode, **reference_params)
            changed |= obj.set_vsys(None, **reference_params)
        except PanDeviceError as e:
            module.fail_json(msg='Failed setref: {0}'.format(e))

        # Remove the interface.
        if obj.name in [x.name for x in interfaces]:
            changed = True
            if not module.check_mode:
                try:
                    obj.delete()
                except PanDeviceError as e:
                    module.fail_json(msg='Failed delete: {0}'.format(e))

    # Commit if we were asked to do so.
    if changed and commit:
        helper.commit(module)

    # Done!
    module.exit_json(changed=changed, msg='Done')


if __name__ == '__main__':
    main()
