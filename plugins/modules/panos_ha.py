#!/usr/bin/python
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

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: panos_ha
short_description: Configures High Availability on PAN-OS
description:
    - Configures High Availability on PAN-OS in A/S and A/A modes including
      all HA interface configuration.  Assumes physical interfaces are of
      type HA already using panos_interface.

      This module has the following limitations due to no support in pandevice -
      * No peer_backup_ip, this prevents full configuration of ha1_backup links
      * Speed and Duplex of ports was intentially skipped
author:
    - Patrick Avery (@unknown)
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
    - currently requires specific pandevice release 0.13
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.state
    - paloaltonetworks.panos.fragments.vsys_import
    - paloaltonetworks.panos.fragments.full_template_support
    - paloaltonetworks.panos.fragments.deprecated_commit
notes:
    - Checkmode is supported.
    - Panorama is supported.
options:
    # ha.HighAvailability
    ha_enabled:
        description:
            - Enable HA
        default: true
        type: bool
    ha_group_id:
        description:
            - The group identifier
        default: 1
        type: int
    ha_config_sync:
        description: Enabled configuration synchronization
        default: true
        type: bool
    ha_peer_ip:
        description: HA Peer HA1 IP address
        type: str
    ha_peer_ip_backup:
        description: HA Peer HA1 Backup IP address
        type: str
    ha_mode:
        description: Mode of HA
        type: str
        choices:
            - active-passive
            - active-active
        default: active-passive
    ha_passive_link_state:
        description: Passive link state
        type: str
        choices:
            - shutdown
            - auto
        default: auto
    ha_state_sync:
        description: Enabled state synchronization
        type: bool
        default: false
    ha_ha2_keepalive:
        description: Enable HA2 keepalives
        type: bool
        default: True
    ha_ha2_keepalive_action:
        description: HA2 keepalive action
        type: str
    ha_ha2_keepalive_threshold:
        description: HA2 keepalive threshold
        type: int

    # Active/Active
    ha_device_id:
        description: HA3 device id (0 or 1)
        type: int
        choices:
            - 0
            - 1
    ha_session_owner_selection:
        description: active-active session owner mode
        type: str
        choices:
            - primary-device
            - first-packet
    ha_session_setup:
        description: active-active session setup mode
        type: str
        choices:
            - primary-device
            - first-packet
            - ip-modulo
            - ip-hash
    ha_tentative_hold_time:
        description: active-active tentative hold timer
        type: int
    ha_sync_qos:
        description: active-active network sync qos
        type: bool
    ha_sync_virtual_router:
        description: active-active network sync virtual router
        type: bool
    ha_ip_hash_key:
        description: active-active hash key used by ip-hash algorithm
        type: str
        choices:
            - source
            - source-and-destination

    # ha.HA1
    ha1_ip_address:
        description: IP of the HA1 interface
        type: str
    ha1_netmask:
        description: Netmask of the HA1 interface
        type: str
    ha1_port:
        description: Interface to use for this HA1 interface (eg. ethernet1/5)
        type: str
    ha1_gateway:
        description: Default gateway of the HA1 interface
        type: str

    # ha.HA1Backup
    ha1b_ip_address:
        description: IP of the HA1Backup interface
        type: str
    ha1b_netmask:
        description: Netmask of the HA1Backup interface
        type: str
    ha1b_port:
        description: Interface to use for this HA1Backup interface (eg. ethernet1/5)
        type: str
    ha1b_gateway:
        description: Default gateway of the HA1Backup interface
        type: str

    # ha.HA2
    ha2_ip_address:
        description: IP of the HA2 interface
        type: str
    ha2_netmask:
        description: Netmask of the HA2 interface
        type: str
    ha2_port:
        description: Interface to use for this HA2 interface (eg. ethernet1/5)
        type: str
        default: ha2-a
    ha2_gateway:
        description: Default gateway of the HA2 interface
        type: str

    # ha.HA2Backup
    ha2b_ip_address:
        description: IP of the HA2Backup interface
        type: str
    ha2b_netmask:
        description: Netmask of the HA2Backup interface
        type: str
    ha2b_port:
        description: Interface to use for this HA2Backup interface (eg. ethernet1/5)
        type: str
    ha2b_gateway:
        description: Default gateway of the HA2Backup interface
        type: str

    # ha.HA3
    ha3_port:
        description: Interface to use for this HA3 interface (eg. ethernet1/5, ae1)
        type: str
'''

EXAMPLES = '''
  - name: set ports to HA mode
    panos_interface:
      provider: '{{ provider }}'
      if_name: "{{ item }}"
      mode: "ha"
      enable_dhcp: false
    with_items:
      - ethernet1/1
      - ethernet1/2
      - ethernet1/3
      - ethernet1/4
      - ethernet1/5

  - name: Configure Active/Standby HA
    panos_ha:
      provider: '{{ provider }}'
      state: present
      ha_peer_ip: "192.168.50.1"
      ha1_ip_address: "192.168.50.2"
      ha1_netmask: "255.255.255.252"
      ha1_port: "ethernet1/1"
      ha2_port: "ethernet1/3"

  - name: Configure Active/Active HA
    panos_ha:
      provider: "{{ provider }}"
      state: present
      ha_mode: "active-active"
      ha_device_id: 0
      ha_session_owner_selection: "first-packet"
      ha_session_setup: "first-packet"
      ha_peer_ip: "192.168.50.1"
      ha_peer_ip_backup: "192.168.50.5"
      ha1_port: "ethernet1/1"
      ha1_ip_address: "192.168.50.2"
      ha1_netmask: "255.255.255.252"
      ha1b_port: "ethernet1/2"
      ha1b_ip_address: "192.168.50.6"
      ha1b_netmask: "255.255.255.252"
      ha2_port: "ethernet1/3"
      ha2b_port: "ethernet1/4"
      ha3_port: "ethernet1/5"
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from panos.ha import HighAvailability, HA1, HA1Backup, HA2, HA2Backup, HA3
    from panos.errors import PanDeviceError
except ImportError:
    try:
        from pandevice.ha import HighAvailability, HA1, HA1Backup, HA2, HA2Backup, HA3
        from pandevice.errors import PanDeviceError
    except ImportError:
        pass


def setup_args():
    return dict(
        commit=dict(type='bool', default=False),
        ha_enabled=dict(type='bool', default=True),
        ha_group_id=dict(type='int', default=1),
        ha_config_sync=dict(type='bool', default=True),
        ha_peer_ip=dict(type='str'),
        ha_peer_ip_backup=dict(type='str'),
        ha_mode=dict(type='str', choices=['active-passive', 'active-active'], default='active-passive'),
        ha_passive_link_state=dict(type='str', choices=['shutdown', 'auto'], default='auto'),
        ha_state_sync=dict(type='bool', default=False),
        ha_ha2_keepalive=dict(type='bool', default=True),
        ha_ha2_keepalive_action=dict(type='str'),
        ha_ha2_keepalive_threshold=dict(type='int'),
        ha_device_id=dict(type='int', choices=[0, 1]),
        ha_session_owner_selection=dict(type='str', choices=['primary-device', 'first-packet']),
        ha_session_setup=dict(type='str', choices=['primary-device', 'first-packet', 'ip-modulo', 'ip-hash']),
        ha_tentative_hold_time=dict(type='int'),
        ha_sync_qos=dict(type='bool'),
        ha_sync_virtual_router=dict(type='bool'),
        ha_ip_hash_key=dict(type='str', choices=['source', 'source-and-destination']),
        ha1_ip_address=dict(type='str'),
        ha1_netmask=dict(type='str'),
        ha1_port=dict(type='str'),
        ha1_gateway=dict(type='str'),
        ha1b_ip_address=dict(type='str'),
        ha1b_netmask=dict(type='str'),
        ha1b_port=dict(type='str'),
        ha1b_gateway=dict(type='str'),
        ha2_ip_address=dict(type='str'),
        ha2_netmask=dict(type='str'),
        ha2_port=dict(type='str', default='ha2-a'),
        ha2_gateway=dict(type='str'),
        ha2b_ip_address=dict(type='str'),
        ha2b_netmask=dict(type='str'),
        ha2b_port=dict(type='str'),
        ha2b_gateway=dict(type='str'),
        ha3_port=dict(type='str'),
    )


def main():
    helper = get_connection(
        vsys_importable=True,
        template=True,
        template_stack=True,
        with_state=True,
        min_pandevice_version=(0, 13, 0),
        with_classic_provider_spec=True,
        argument_spec=setup_args(),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # Verify imports, build pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    # Retrieve current HA configuration.
    try:
        listing = HighAvailability.refreshall(parent, add=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    # Exclude non-object items from kwargs passed to the object.
    exclude_list = [
        'ip_address', 'username', 'password', 'api_key', 'state', 'commit',
        'provider', 'template', 'template_stack', 'vsys', 'port',
    ]

    # Remove excluded items from spec
    spec_included = dict((k, module.params[k]) for k in helper.argument_spec.keys() if k not in exclude_list)

    # Generate the kwargs for ha.HighAvailability
    ha_obj_spec = {k.replace('ha_', ''): spec_included[k] for k in spec_included if k.startswith("ha_")}

    # Generate the kwargs for ha.HA1
    ha1_obj_spec = {k.replace('ha1_', ''): spec_included[k] for k in spec_included if k.startswith("ha1_")}

    # Generate the kwargs for ha.HA1Backup
    ha1b_obj_spec = {k.replace('ha1b_', ''): spec_included[k] for k in spec_included if k.startswith("ha1b_")}

    # Generate the kwargs for ha.HA2
    ha2_obj_spec = {k.replace('ha2_', ''): spec_included[k] for k in spec_included if k.startswith("ha2_")}

    # Generate the kwargs for ha.HA2Backup
    ha2b_obj_spec = {k.replace('ha2b_', ''): spec_included[k] for k in spec_included if k.startswith("ha2b_")}

    # Generate the kwargs for ha.HA3
    ha3_obj_spec = {k.replace('ha3_', ''): spec_included[k] for k in spec_included if k.startswith("ha3_")}

    state = module.params['state']
    commit = module.params['commit']

    # Create the new state object.
    obj = HighAvailability(**ha_obj_spec)

    # Add sub-objects only if at least one param for that type is specified.
    '''
    obj.add(HA1(**ha1_obj_spec))
    obj.add(HA1Backup(**ha1b_obj_spec))
    obj.add(HA2(**ha2_obj_spec))
    obj.add(HA2Backup(**ha2b_obj_spec))
    obj.add(HA3(**ha3_obj_spec))
    '''
    class_specs = [
        (HA1, ha1_obj_spec),
        (HA1Backup, ha1b_obj_spec),
        (HA2, ha2_obj_spec),
        (HA2Backup, ha2b_obj_spec),
        (HA3, ha3_obj_spec),
    ]
    for cls_type, cls_spec in class_specs:
        if any(x is not None for x in cls_spec.values()):
            sub_obj = cls_type(**cls_spec)
            obj.add(sub_obj)

    # Add ha object to parent
    parent.add(obj)

    # HighAvailability.refreshall() is not working for these in pandevice.ha
    # removing until this is fixed to prevent changed from always equal to True
    listing[0].session_owner_selection = obj.session_owner_selection
    listing[0].session_setup = obj.session_setup

    # Apply the state.
    changed, diff = helper.apply_state(obj, listing, module)

    if commit and changed:
        helper.commit(module)

    module.exit_json(msg='Done', changed=changed, diff=diff)


if __name__ == '__main__':
    main()
