#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2017 Palo Alto Networks, Inc
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

DOCUMENTATION = """
---
module: panos_object
short_description: create/read/update/delete object in PAN-OS or Panorama
description:
    - Policy objects form the match criteria for policy rules and many other functions in PAN-OS. These may include
    - address object, address groups, service objects, service groups, and tag.
author: "Bob Hagen (@stealthllama)"
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
deprecated:
  removed_in: '4.0.0'
  why: Updated to idempotent modules
  alternative: >
                 Use M(paloaltonetworks.panos.panos_address_object), M(paloaltonetworks.panos.panos_address_group),
                 M(paloaltonetworks.panos.panos_service_object), M(paloaltonetworks.panos.panos_service_group), or
                 M(paloaltonetworks.panos.panos_tag_object) as appropriate.
notes:
    - Checkmode is not supported.
    - Panorama is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.vsys
    - paloaltonetworks.panos.fragments.deprecated_commit
options:
    ip_address:
        description:
            - IP address (or hostname) of PAN-OS device or Panorama management console being configured.
        type: str
        required: true
    username:
        description:
            - Username credentials to use for authentication.
        type: str
        required: false
        default: "admin"
    password:
        description:
            - Password credentials to use for authentication.
        type: str
    api_key:
        description:
            - API key that can be used instead of I(username)/I(password) credentials.
        type: str
    operation:
        description:
            - The operation to be performed.
        type: str
        required: true
        choices:
            - add
            - update
            - delete
            - find
    addressobject:
        description:
            - The name of the address object.
        type: str
    address:
        description:
            - The IP address of the host or network in CIDR notation.
        type: str
    address_type:
        description:
            - The type of address object definition.  Valid types are I(ip-netmask) and I(ip-range).
        type: str
        choices: ['ip-netmask', 'ip-range', 'fqdn']
        default: 'ip-netmask'
    addressgroup:
        description:
            - A static group of address objects or dynamic address group.
        type: str
    static_value:
        description:
            - A group of address objects to be used in an addressgroup definition.
        type: list
        elements: str
    dynamic_value:
        description:
            - The filter match criteria to be used in a dynamic addressgroup definition.
        type: str
    serviceobject:
        description:
            - The name of the service object.
        type: str
    source_port:
        description:
            - The source port to be used in a service object definition.
        type: str
    destination_port:
        description:
            - The destination port to be used in a service object definition.
        type: str
    protocol:
        description:
            - The IP protocol to be used in a service object definition.
        type: str
        choices:
            - tcp
            - udp
    servicegroup:
        description:
            - A group of service objects.
        type: str
    services:
        description:
            - The group of service objects used in a servicegroup definition.
        type: list
        elements: str
    description:
        description:
            - The description of the object.
        type: str
    tag_name:
        description:
            - The name of an object or rule tag.
        type: str
    color:
        description: >
            - The color of the tag object.  Valid values are I(red, green, blue, yellow, copper, orange, purple, gray,
            light green, cyan, light gray, blue gray, lime, black, gold, brown, olive, maroon, red-orange,
            yellow-orange, forest green, turquoise blue, azure blue, cerulean blue, midnight blue, medium blue,
            cobalt blue, violet blue, blue violet, medium violet, medium rose, lavender, orchid, thistle, peach,
            salmon, magenta, reggd violet, mahogany, burnt sienna and chestnut).
        type: str
        choices:
            - red
            - green
            - blue
            - yellow
            - copper
            - orange
            - purple
            - gray
            - light green
            - cyan
            - light gray
            - blue gray
            - lime
            - black
            - gold
            - brown
            - olive
            - maroon
            - red-orange
            - yellow-orange
            - forest green
            - turquoise blue
            - azure blue
            - cerulean blue
            - midnight blue
            - medium blue
            - cobalt blue
            - violet blue
            - blue violet
            - medium violet
            - medium rose
            - lavender
            - orchid
            - thistle
            - peach
            - salmon
            - magenta
            - red violet
            - mahogany
            - burnt sienna
            - chestnut
    vsys:
        description:
            - The vsys to put the object into.
            - Firewall only.
        type: str
        default: "vsys1"
    devicegroup:
        description:
            - The name of the (preexisting) Panorama device group.
            - If undefined and ip_address is Panorama, this defaults to shared.
        type: str
        required: false
"""

EXAMPLES = """
- name: search for shared address object
  paloaltonetworks.panos.panos_object:
    ip_address: '{{ ip_address }}'
    username: '{{ username }}'
    password: '{{ password }}'
    operation: 'find'
    address: 'DevNet'

- name: create an address group in devicegroup using API key
  paloaltonetworks.panos.panos_object:
    ip_address: '{{ ip_address }}'
    api_key: '{{ api_key }}'
    operation: 'add'
    addressgroup: 'Prod_DB_Svrs'
    static_value: ['prod-db1', 'prod-db2', 'prod-db3']
    description: 'Production DMZ database servers'
    tag_name: 'DMZ'
    devicegroup: 'DMZ Firewalls'

- name: create a global service for TCP 3306
  paloaltonetworks.panos.panos_object:
    ip_address: '{{ ip_address }}'
    api_key: '{{ api_key }}'
    operation: 'add'
    serviceobject: 'mysql-3306'
    destination_port: '3306'
    protocol: 'tcp'
    description: 'MySQL on tcp/3306'

- name: create a global tag
  paloaltonetworks.panos.panos_object:
    ip_address: '{{ ip_address }}'
    username: '{{ username }}'
    password: '{{ password }}'
    operation: 'add'
    tag_name: 'ProjectX'
    color: 'yellow'
    description: 'Associated with Project X'

- name: delete an address object from a devicegroup using API key
  paloaltonetworks.panos.panos_object:
    ip_address: '{{ ip_address }}'
    api_key: '{{ api_key }}'
    operation: 'delete'
    addressobject: 'Win2K test'
"""

RETURN = """
# Default return values
"""

from ansible.module_utils.basic import AnsibleModule

try:
    from panos.panorama import DeviceGroup, Panorama
    from panos.firewall import Firewall
    from panos import objects
    from panos.base import PanDevice
    from panos.errors import PanDeviceError
except ImportError:
    try:
        from pandevice.panorama import DeviceGroup, Panorama
        from pandevice.firewall import Firewall
        from pandevice import objects
        from pandevice.base import PanDevice
        from pandevice.errors import PanDeviceError
    except ImportError:
        pass

try:
    import json

    import xmltodict
    from pan.xapi import PanXapiError

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def get_devicegroup(device, devicegroup):
    dg_list = device.refresh_devices()
    for group in dg_list:
        if isinstance(group, DeviceGroup):
            if group.name == devicegroup:
                return group
    return False


def find_object(device, dev_group, obj_name, obj_type):
    # Get the firewall objects
    obj_type.refreshall(device)
    if isinstance(device, Firewall):
        addr = device.find(obj_name, obj_type)
        return addr
    elif isinstance(device, Panorama):
        addr = device.find(obj_name, obj_type)
        if addr is None:
            if dev_group:
                device.add(dev_group)
                obj_type.refreshall(dev_group)
                addr = dev_group.find(obj_name, obj_type)
        return addr
    else:
        return False


def create_object(**kwargs):
    if kwargs["addressobject"]:
        newobject = objects.AddressObject(
            name=kwargs["addressobject"],
            value=kwargs["address"],
            type=kwargs["address_type"],
            description=kwargs["description"],
            tag=kwargs["tag_name"],
        )
        if newobject.type and newobject.value:
            return newobject
        else:
            return False
    elif kwargs["addressgroup"]:
        newobject = objects.AddressGroup(
            name=kwargs["addressgroup"],
            static_value=kwargs["static_value"],
            dynamic_value=kwargs["dynamic_value"],
            description=kwargs["description"],
            tag=kwargs["tag_name"],
        )
        if newobject.static_value or newobject.dynamic_value:
            return newobject
        else:
            return False
    elif kwargs["serviceobject"]:
        newobject = objects.ServiceObject(
            name=kwargs["serviceobject"],
            protocol=kwargs["protocol"],
            source_port=kwargs["source_port"],
            destination_port=kwargs["destination_port"],
            tag=kwargs["tag_name"],
        )
        if newobject.protocol and newobject.destination_port:
            return newobject
        else:
            return False
    elif kwargs["servicegroup"]:
        newobject = objects.ServiceGroup(
            name=kwargs["servicegroup"],
            value=kwargs["services"],
            tag=kwargs["tag_name"],
        )
        if newobject.value:
            return newobject
        else:
            return False
    elif kwargs["tag_name"]:
        t = objects.Tag
        c = t.color_code(kwargs["color"])
        newobject = objects.Tag(
            name=kwargs["tag_name"], color=c, comments=kwargs["description"]
        )
        if newobject.name:
            return newobject
        else:
            return False
    else:
        return False


def add_object(device, dev_group, new_object):
    if dev_group:
        dev_group.add(new_object)
    else:
        device.add(new_object)
    new_object.create()
    return True


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(no_log=True),
        username=dict(default="admin"),
        api_key=dict(no_log=True),
        operation=dict(required=True, choices=["add", "update", "delete", "find"]),
        addressobject=dict(default=None),
        addressgroup=dict(default=None),
        serviceobject=dict(default=None),
        servicegroup=dict(default=None),
        address=dict(default=None),
        address_type=dict(
            default="ip-netmask", choices=["ip-netmask", "ip-range", "fqdn"]
        ),
        static_value=dict(type="list", elements="str", default=None),
        dynamic_value=dict(default=None),
        protocol=dict(default=None, choices=["tcp", "udp"]),
        source_port=dict(default=None),
        destination_port=dict(default=None),
        services=dict(type="list", elements="str", default=None),
        description=dict(default=None),
        tag_name=dict(default=None),
        color=dict(
            default=None,
            choices=[
                "red",
                "green",
                "blue",
                "yellow",
                "copper",
                "orange",
                "purple",
                "gray",
                "light green",
                "cyan",
                "light gray",
                "blue gray",
                "lime",
                "black",
                "gold",
                "brown",
                "olive",
                "maroon",
                "red-orange",
                "yellow-orange",
                "forest green",
                "turquoise blue",
                "azure blue",
                "cerulean blue",
                "midnight blue",
                "medium blue",
                "cobalt blue",
                "violet blue",
                "blue violet",
                "medium violet",
                "medium rose",
                "lavender",
                "orchid",
                "thistle",
                "peach",
                "salmon",
                "magenta",
                "red violet",
                "mahogany",
                "burnt sienna",
                "chestnut",
            ],
        ),
        vsys=dict(default="vsys1"),
        devicegroup=dict(default=None),
        commit=dict(type="bool"),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False,
        required_one_of=[["api_key", "password"]],
        mutually_exclusive=[
            [
                "addressobject",
                "addressgroup",
                "serviceobject",
                "servicegroup",
                "tag_name",
            ]
        ],
    )
    if not HAS_LIB:
        module.fail_json(msg="Missing required libraries.")

    ip_address = module.params["ip_address"]
    password = module.params["password"]
    username = module.params["username"]
    api_key = module.params["api_key"]
    operation = module.params["operation"]
    addressobject = module.params["addressobject"]
    addressgroup = module.params["addressgroup"]
    serviceobject = module.params["serviceobject"]
    servicegroup = module.params["servicegroup"]
    address = module.params["address"]
    address_type = module.params["address_type"]
    static_value = module.params["static_value"]
    dynamic_value = module.params["dynamic_value"]
    protocol = module.params["protocol"]
    source_port = module.params["source_port"]
    destination_port = module.params["destination_port"]
    services = module.params["services"]
    description = module.params["description"]
    tag_name = module.params["tag_name"]
    color = module.params["color"]
    vsys = module.params["vsys"]
    devicegroup = module.params["devicegroup"]
    commit = module.params["commit"]

    # Create the device with the appropriate pandevice type
    device = PanDevice.create_from_device(
        ip_address, username, password, api_key=api_key
    )

    # If Panorama, validate the devicegroup
    dev_group = None
    if hasattr(device, "refresh_devices"):
        # Panorama: set the device group.
        if devicegroup == "shared":
            # Device group of None is "shared" scope for Panorama.
            devicegroup = None
        if devicegroup is not None:
            dev_group = get_devicegroup(device, devicegroup)
            if dev_group:
                device.add(dev_group)
            else:
                module.fail_json(
                    msg="'%s' device group not found in Panorama. Is the name correct?"
                    % devicegroup
                )
    else:
        # Firewall: set the targetted vsys.
        device.vsys = vsys

    # What type of object are we talking about?
    if addressobject:
        obj_name = addressobject
        obj_type = objects.AddressObject
    elif addressgroup:
        obj_name = addressgroup
        obj_type = objects.AddressGroup
    elif serviceobject:
        obj_name = serviceobject
        obj_type = objects.ServiceObject
    elif servicegroup:
        obj_name = servicegroup
        obj_type = objects.ServiceGroup
    elif tag_name:
        obj_name = tag_name
        obj_type = objects.Tag
    else:
        module.fail_json(msg="No object type defined!")

    # Which operation shall we perform on the object?
    msg = None
    if operation == "find":
        # Search for the object
        match = find_object(device, dev_group, obj_name, obj_type)

        # If found, format and return the result
        if match:
            match_dict = xmltodict.parse(match.element_str())
            module.exit_json(
                stdout_lines=json.dumps(match_dict, indent=2), msg="Object matched"
            )
        else:
            module.fail_json(
                msg="Object '%s' not found. Is the name correct?" % obj_name
            )
    elif operation == "delete":
        # Search for the object
        match = find_object(device, dev_group, obj_name, obj_type)

        # If found, delete it
        if match:
            try:
                match.delete()
            except PanXapiError as e:
                module.fail_json(msg=e.message)

            msg = "Object '{0}' successfully deleted".format(obj_name)
        else:
            module.fail_json(
                msg="Object '%s' not found. Is the name correct?" % obj_name
            )
    elif operation == "add":
        # Search for the object. Fail if found.
        match = find_object(device, dev_group, obj_name, obj_type)
        if match:
            module.fail_json(
                msg="Object '%s' already exists. Use operation: 'update' to change it."
                % obj_name
            )
        else:
            try:
                new_object = create_object(
                    addressobject=addressobject,
                    addressgroup=addressgroup,
                    serviceobject=serviceobject,
                    servicegroup=servicegroup,
                    address=address,
                    address_type=address_type,
                    static_value=static_value,
                    dynamic_value=dynamic_value,
                    protocol=protocol,
                    source_port=source_port,
                    destination_port=destination_port,
                    services=services,
                    description=description,
                    tag_name=tag_name,
                    color=color,
                )
                changed = add_object(device, dev_group, new_object)
            except PanXapiError as e:
                module.fail_json(msg=e.message)
        msg = "Object '{0}' successfully added".format(obj_name)
    elif operation == "update":
        # Search for the object. Update if found.
        match = find_object(device, dev_group, obj_name, obj_type)
        if match:
            try:
                new_object = create_object(
                    addressobject=addressobject,
                    addressgroup=addressgroup,
                    serviceobject=serviceobject,
                    servicegroup=servicegroup,
                    address=address,
                    address_type=address_type,
                    static_value=static_value,
                    dynamic_value=dynamic_value,
                    protocol=protocol,
                    source_port=source_port,
                    destination_port=destination_port,
                    services=services,
                    description=description,
                    tag_name=tag_name,
                    color=color,
                )
                changed = add_object(device, dev_group, new_object)
            except PanXapiError as e:
                module.fail_json(msg=e.message)
            msg = "Object '{0}' successfully updated.".format(obj_name)
        else:
            module.fail_json(
                msg="Object '%s' does not exist. Use operation: 'add' to add it."
                % obj_name
            )

    # Optional: commit the change.
    if commit:
        try:
            device.commit(sync=True)
        except PanDeviceError as e:
            module.fail_json(msg="Failed to commit: {0}".format(e))

    # Done.
    module.exit_json(changed=True, msg=msg)


if __name__ == "__main__":
    main()
