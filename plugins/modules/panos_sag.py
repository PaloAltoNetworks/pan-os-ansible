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
module: panos_sag
short_description: Create a static address group.
description:
    - Create a static address group object in the firewall used for policy rules.
author: "Vinay Venkataraghavan (@vinayvenkat)"
version_added: '1.0.0'
deprecated:
    alternative: Use M(panos_address_group) instead.
    removed_in: '3.0.0'
    why: This module's functionality is a subset of M(panos_address_group).
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
    - xmltodict can be obtained from PyPI U(https://pypi.python.org/pypi/xmltodict)
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.deprecated_commit
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
    username:
        description:
            - username for authentication
        type: str
        required: false
        default: "admin"
    api_key:
        description:
            - API key that can be used instead of I(username)/I(password) credentials.
        type: str
    sag_name:
        description:
            - name of the dynamic address group
        type: str
        required: true
    sag_match_filter:
        description:
            - Static filter used by the address group
        type: list
        elements: str
    devicegroup:
        description: >
            - The name of the Panorama device group. The group must exist on Panorama. If device group is not defined
            it is assumed that we are contacting a firewall.
        type: str
        required: false
    description:
        description:
            - The purpose / objective of the static Address Group
        type: str
        required: false
    tags:
        description:
            - Tags to be associated with the address group
        type: list
        elements: str
        required: false
    operation:
        description:
            - The operation to perform Supported values are I(add)/I(list)/I(delete).
        type: str
        choices:
            - add
            - list
            - delete
        required: true
'''

EXAMPLES = '''
- name: sag
  panos_sag:
    ip_address: "192.168.1.1"
    password: "admin"
    sag_name: "sag-1"
    static_value: ['test-addresses', ]
    description: "A description for the static address group"
    tags: ["tags to be associated with the group", ]
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule, get_exception

try:
    from pandevice import base
    from pandevice import firewall
    from pandevice import panorama
    from pandevice import objects
    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def get_devicegroup(device, devicegroup):
    dg_list = device.refresh_devices()
    for group in dg_list:
        if isinstance(group, panorama.DeviceGroup):
            if group.name == devicegroup:
                return group
    return False


def find_object(device, dev_group, obj_name, obj_type):
    # Get the firewall objects
    obj_type.refreshall(device)
    if isinstance(device, firewall.Firewall):
        addr = device.find(obj_name, obj_type)
        return addr
    elif isinstance(device, panorama.Panorama):
        addr = device.find(obj_name, obj_type)
        if addr is None:
            if dev_group:
                device.add(dev_group)
                obj_type.refreshall(dev_group)
                addr = dev_group.find(obj_name, obj_type)
        return addr
    else:
        return False


def create_address_group_object(**kwargs):
    """
    Create an Address object

    :param kwargs: key word arguments to instantiate AddressGroup object
    @return False or ```objects.AddressObject```
    """
    ad_object = objects.AddressGroup(
        name=kwargs['address_gp_name'],
        static_value=kwargs['sag_match_filter'],
        description=kwargs['description'],
        tag=kwargs['tag_name']
    )
    if ad_object.static_value or ad_object.dynamic_value:
        return ad_object
    else:
        return None


def add_address_group(device, dev_group, ag_object):
    """
    Create a new dynamic address group object on the
    PAN FW.

    :param device: Firewall Handle
    :param dev_group: Panorama device group
    :param ag_object: Address group object
    """

    if dev_group:
        dev_group.add(ag_object)
    else:
        device.add(ag_object)

    exc = None
    try:
        ag_object.create()
    except Exception:
        exc = get_exception()
        return False, exc

    return True, exc


def get_all_address_group(device):
    """
    Retrieve all the tag to IP address mappings
    :param device:
    :return:
    """
    exc = None
    try:
        ret = objects.AddressGroup.refreshall(device)
    except Exception:
        exc = get_exception()

    if exc:
        return (False, exc)
    else:
        sl = []
        for item in ret:
            sl.append(item.name)
        s = ",".join(sl)
    return s, exc


def delete_address_group(device, dev_group, obj_name):
    """

    :param device:
    :param dev_group:
    :param obj_name:
    :return:
    """
    static_obj = find_object(device, dev_group, obj_name, objects.AddressGroup)
    # If found, delete it

    if static_obj:
        try:
            static_obj.delete()
        except Exception:
            exc = get_exception()
            return False, exc
        return True, None
    else:
        return False, None


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(no_log=True),
        username=dict(default='admin'),
        api_key=dict(no_log=True),
        sag_match_filter=dict(type='list', elements='str', required=False),
        sag_name=dict(required=True),
        commit=dict(type='bool', default=False),
        devicegroup=dict(default=None),
        description=dict(default=None),
        tags=dict(type='list', elements='str', default=[]),
        operation=dict(type='str', required=True, choices=['add', 'list', 'delete'])
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False,
                           required_one_of=[['api_key', 'password']])

    module.deprecate(
        'This module has been deprecated; use panos_address_group',
        version='3.0.0', collection_name='paloaltonetworks.panos'
    )

    if not HAS_LIB:
        module.fail_json(msg='pan-python is required for this module')

    ip_address = module.params["ip_address"]
    password = module.params["password"]
    username = module.params['username']
    api_key = module.params['api_key']
    operation = module.params['operation']

    ag_object = create_address_group_object(address_gp_name=module.params.get('sag_name', None),
                                            sag_match_filter=module.params.get('sag_match_filter', None),
                                            description=module.params.get('description', None),
                                            tag_name=module.params.get('tags', None)
                                            )
    commit = module.params['commit']

    devicegroup = module.params['devicegroup']
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

    if operation == 'add':
        result, exc = add_address_group(device, dev_group, ag_object)

        if result and commit:
            try:
                device.commit(sync=True)
            except Exception:
                exc = get_exception()
                module.fail_json(msg=exc.message)
    elif operation == 'list':
        result, exc = get_all_address_group(device)

        if not exc:
            module.exit_json(msg=result)
        else:
            module.fail_json(msg=exc.message)
    elif operation == 'delete':
        obj_name = module.params.get('sag_name', None)
        result, exc = delete_address_group(device, dev_group, obj_name)
        if not result and exc:
            module.fail_json(msg=exc.message)
        elif not result:
            module.fail_json(msg="Specified object not found.")
    else:
        module.fail_json(changed=False, msg="Unsupported option.")

    module.exit_json(changed=True, msg="Address Group Operation Completed.")


if __name__ == '__main__':
    main()
