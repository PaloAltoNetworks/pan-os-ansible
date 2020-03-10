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
module: panos_l2_subinterface
short_description: configure layer2 subinterface
description:
    - Configure a layer2 subinterface.
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
    lldp_enabled:
        description:
            - Enable LLDP
        type: bool
    lldp_profile:
        description:
            - Reference to an LLDP profile
    netflow_profile:
        description:
            - Reference to a netflow profile.
    comment:
        description:
            - Interface comment.
    zone_name:
        description:
            - Name of the zone for the interface.
            - If the zone does not exist it is created.
    vlan_name:
        description:
            - The VLAN to put this interface in.
            - If the VLAN does not exist it is created.
'''

EXAMPLES = '''
# Create ethernet1/1.5
- name: ethernet1/1.5 in zone sales
  panos_l2_subinterface:
    provider: '{{ provider }}'
    name: "ethernet1/1.5"
    tag: 5
    zone_name: "sales"
    vlan_name: "myVlan"
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
    from pandevice.network import Layer2Subinterface
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
            lldp_enabled=dict(type='bool'),
            lldp_profile=dict(),
            netflow_profile=dict(),
            comment=dict(),
            zone_name=dict(),
            vlan_name=dict(),
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
        'lldp_enabled': module.params['lldp_enabled'],
        'lldp_profile': module.params['lldp_profile'],
        'netflow_profile_l2': module.params['netflow_profile'],
        'comment': module.params['comment'],
    }

    # Get other info.
    state = module.params['state']
    zone_name = module.params['zone_name']
    vlan_name = module.params['vlan_name']
    vsys = module.params['vsys']

    # Sanity check.
    if '.' not in spec['name']:
        module.fail_json(msg='Interface name does not have "." in it')

    # Check on EthernetInterface or AggregateInterface.
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

    if parent_eth.mode != 'layer2':
        module.fail_json(msg='{0} mode is {1}, not layer2'.format(parent_eth.name, parent_eth.mode))

    interfaces = parent_eth.findall(Layer2Subinterface)

    # Build the object based on the user spec.
    eth = Layer2Subinterface(**spec)
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
            changed |= eth.set_vlan(vlan_name, **reference_params)
        except PanDeviceError as e:
            module.fail_json(msg='Failed setref: {0}'.format(e))
    elif state == 'absent':
        # Remove references.
        try:
            changed |= eth.set_vlan(None, **reference_params)
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
