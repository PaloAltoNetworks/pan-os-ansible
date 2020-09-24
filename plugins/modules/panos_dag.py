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
module: panos_dag
short_description: create a dynamic address group
description:
    - Create a dynamic address group object in the firewall used for policy rules
author: "Luigi Mori (@jtschichold), Ivan Bojer (@ivanbojer), Vinay Venkataraghavan (@vinayvenkat)"
version_added: '1.0.0'
deprecated:
    alternative: Use M(panos_address_group) instead.
    removed_in: '3.0.0'
    why: This module's functionality is a subset of M(panos_address_group).
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
options:
    ip_address:
        description:
            - IP address (or hostname) of PAN-OS device
        type: str
        required: true
        default: null
    password:
        description:
            - password for authentication
        type: str
        required: true
        default: null
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
    dag_name:
        description:
            - name of the dynamic address group
        type: str
        required: true
        default: null
    dag_match_filter:
        description:
            - dynamic filter user by the dynamic address group
        type: str
        default: null
    tag_name:
        description:
            - Add administrative tags to the DAG
        type: list
        elements: str
        required: false
        default: null
    devicegroup:
        description:
            - The name of the Panorama device group. The group must exist on Panorama. If
              device group is not defined it is assumed that we are contacting a firewall.
        type: str
        required: false
    operation:
        description:
            - The operation to perform Supported values are I(add)/I(list)/I(delete).
        type: str
        required: true
        choices: ['add', 'list', 'delete']
        default: null
    commit:
        description:
            - commit if changed
        type: bool
        required: false
        default: false
    description:
        description:
            - The description of the object.
        type: str
'''

EXAMPLES = '''
- name: Create dag
  panos_dag:
    ip_address: "192.168.1.1"
    password: "admin"
    dag_name: "dag-1"
    dag_match_filter: "'aws-tag.aws:cloudformation:logical-id.ServerInstance' and 'instanceState.running'"
    description: 'Add / create dynamic address group to allow access to SaaS Applications'
    operation: 'add'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import get_exception

try:
    from pan.xapi import PanXapiError
    HAS_LIB = True
except ImportError:
    HAS_LIB = False

try:
    from panos import base
    from panos import objects
except ImportError:
    try:
        from pandevice import base
        from pandevice import objects
    except ImportError:
        pass


def create_address_group_object(**kwargs):
    """
    Create an Address object

    @return False or ```objects.AddressObject```
    """
    ad_object = objects.AddressGroup(
        name=kwargs['address_gp_name'],
        dynamic_value=kwargs['dynamic_value'],
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
    """

    if dev_group:
        dev_group.add(ag_object)
    else:
        device.add(ag_object)

    ag_object.create()
    return True


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
        return (s, exc)


def delete_address_group(device, group_name):
    """
    Delete a specific address group

    :param device:
    :param group_name:
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
        for ag in ret:
            if ag.name == group_name:
                ag.delete()
        return (True, None)


def main():

    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(no_log=True, required=True),
        username=dict(default='admin'),
        api_key=dict(no_log=True),
        dag_match_filter=dict(type='str', default=None),
        dag_name=dict(required=True),
        tag_name=dict(type='list', elements='str', required=False),
        commit=dict(type='bool', default=False),
        devicegroup=dict(default=None),
        description=dict(default=None),
        operation=dict(type='str', required=True, choices=['add', 'list', 'delete'])
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False,
                           required_one_of=[['api_key', 'password']])

    module.deprecate(
        'This module has been deprecated; use panos_address_group',
        version='3.0.0', collection_name='paloaltonetworks.panos'
    )

    if not HAS_LIB:
        module.fail_json(msg='Missing required libraries.')

    ip_address = module.params["ip_address"]
    password = module.params["password"]
    username = module.params['username']
    api_key = module.params['api_key']
    operation = module.params['operation']

    ag_object = create_address_group_object(address_gp_name=module.params.get('dag_name', None),
                                            dynamic_value=module.params.get('dag_match_filter', None),
                                            description=module.params.get('description', None),
                                            tag_name=module.params.get('tag_names', None)
                                            )
    commit = module.params['commit']

    # Create the device with the appropriate pandevice type
    device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)

    # If Panorama, validate the devicegroup
    dev_group = None
    '''
    # TODO(vinay) - implement get_devicegroup
    if devicegroup and isinstance(device, panorama.Panorama):
        dev_group = get_devicegroup(device, devicegroup)
        if dev_group:
            device.add(dev_group)
        else:
            module.fail_json(msg='\'%s\' device group not found in Panorama. Is the name correct?' % devicegroup)
    '''

    result = None
    if operation == 'add':
        result = add_address_group(device, dev_group, ag_object)
    elif operation == 'list':
        result, exc = get_all_address_group(device)
    elif operation == 'delete':
        result, exc = delete_address_group(device, group_name=module.params.get('dag_name', None))

    if result and commit:
        try:
            device.commit(sync=True)
        except PanXapiError:
            exc = get_exception()
            module.fail_json(msg=exc.message)

    module.exit_json(changed=True, msg=result)


if __name__ == '__main__':
    main()
