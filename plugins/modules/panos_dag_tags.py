#!/usr/bin/python
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

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: panos_dag_tags
short_description: Create tags for DAG's on PAN-OS devices.
description:
    - Create the ip address to tag associations. Tags will in turn be used to create DAG's
author: "Vinay Venkataraghavan (@vinayvenkat)"
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
deprecated:
  removed_in: '3.0.0'
  why: Using new modern API calls in the panos_registered_ip
  alternative: Use M(panos_registered_ip) instead.
notes:
    - Checkmode is not supported.
    - Panorama is not supported.
    - use panos_registered_ip from now on
options:
    ip_address:
        description:
            - IP address (or hostname) of PAN-OS device
        type: str
        required: true
    password:
        description:
            - password for authentication
        type: str
        required: true
    api_key:
        description:
            - API key that can be used instead of I(username)/I(password) credentials.
        type: str
    username:
        description:
            - username for authentication
        type: str
        default: "admin"
    description:
        description:
            - The purpose / objective of the static Address Group
        type: str
    commit:
        description:
            - commit if changed
        type: bool
        default: false
    devicegroup:
        description: >
            - Device groups are used for the Panorama interaction with Firewall(s). The group must exists on Panorama.
            If device group is not define we assume that we are contacting Firewall.
        type: str
    operation:
        description:
            - The action to be taken. Supported values are I(add)/I(update)/I(find)/I(delete).
        type: str
        choices: ['add', 'update', 'find', 'delete']
        required: true
    tag_names:
        description:
            - The list of the tags that will be added or removed from the IP address.
        type: list
        elements: str
        required: true
    ip_to_register:
        description:
            - IP that will be registered with the given tag names.
        type: str
'''

EXAMPLES = '''
- name: Create the tags to map IP addresses
  panos_dag_tags:
    ip_address: "{{ ip_address }}"
    password: "{{ password }}"
    ip_to_register: "{{ ip_to_register }}"
    tag_names: "{{ tag_names }}"
    description: "Tags to allow certain IP's to access various SaaS Applications"
    operation: 'add'
  tags: "adddagip"

- name: List the IP address to tag mapping
  panos_dag_tags:
    ip_address: "{{ ip_address }}"
    password: "{{ password }}"
    tag_names: "{{ tag_names }}"
    description: "List the IP address to tag mapping"
    operation: 'list'
  tags: "listdagip"

- name: Unregister an IP address from a tag mapping
  panos_dag_tags:
    ip_address: "{{ ip_address }}"
    password: "{{ password }}"
    ip_to_register: "{{ ip_to_register }}"
    tag_names: "{{ tag_names }}"
    description: "Unregister IP address from tag mappings"
    operation: 'delete'
  tags: "deletedagip"
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule, get_exception

try:
    from pan.xapi import PanXapiError
    HAS_LIB = True
except ImportError:
    HAS_LIB = False

try:
    from panos import base
    from panos import panorama
except ImportError:
    try:
        from pandevice import base
        from pandevice import panorama
    except ImportError:
        pass


def get_devicegroup(device, devicegroup):
    dg_list = device.refresh_devices()
    for group in dg_list:
        if isinstance(group, panorama.DeviceGroup):
            if group.name == devicegroup:
                return group
    return False


def register_ip_to_tag_map(device, ip_addresses, tag):
    exc = None
    try:
        device.userid.register(ip_addresses, tag)
    except PanXapiError:
        exc = get_exception()

    if exc:
        return False, exc

    return True, exc


def get_all_address_group_mapping(device):
    exc = None
    ret = None
    try:
        ret = device.userid.get_registered_ip()
    except PanXapiError:
        exc = get_exception()

    if exc:
        return False, exc

    return ret, exc


def delete_address_from_mapping(device, ip_address, tags):
    exc = None
    try:
        device.userid.unregister(ip_address, tags)
    except PanXapiError:
        exc = get_exception()

    if exc:
        return False, exc

    return True, exc


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(required=True, no_log=True),
        username=dict(default='admin'),
        api_key=dict(no_log=True),
        devicegroup=dict(default=None),
        description=dict(default=None),
        ip_to_register=dict(type='str', required=False),
        tag_names=dict(type='list', elements='str', required=True),
        commit=dict(type='bool', default=False),
        operation=dict(type='str', choices=['add', 'update', 'find', 'delete'], required=True)
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if not HAS_LIB:
        module.fail_json(msg='pan-python is required for this module')

    ip_address = module.params["ip_address"]
    password = module.params["password"]
    username = module.params['username']
    api_key = module.params['api_key']
    commit = module.params['commit']
    devicegroup = module.params['devicegroup']
    operation = module.params['operation']

    # Create the device with the appropriate pandevice type
    device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)

    # If Panorama, validate the devicegroup
    dev_group = None
    if devicegroup and isinstance(device, panorama.Panorama):
        dev_group = get_devicegroup(device, devicegroup)
        if dev_group:
            device.add(dev_group)
        else:
            module.fail_json(msg='\'%s\' device group not found in Panorama. Is the name correct?' % devicegroup)

    result = None
    if operation == 'add':
        result, exc = register_ip_to_tag_map(device,
                                             ip_addresses=module.params.get('ip_to_register', None),
                                             tag=module.params.get('tag_names', None)
                                             )
    elif operation == 'list':
        result, exc = get_all_address_group_mapping(device)
    elif operation == 'delete':
        result, exc = delete_address_from_mapping(device,
                                                  ip_address=module.params.get('ip_to_register', None),
                                                  tags=module.params.get('tag_names', [])
                                                  )
    else:
        module.fail_json(msg="Unsupported option")

    if not result:
        module.fail_json(msg=exc.message)

    if commit:
        try:
            device.commit(sync=True)
        except PanXapiError:
            exc = get_exception()
            module.fail_json(msg=exc)

    module.exit_json(changed=True, msg=result)


if __name__ == "__main__":
    main()
