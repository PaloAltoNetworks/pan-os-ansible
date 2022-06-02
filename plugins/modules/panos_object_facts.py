#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2018 Palo Alto Networks, Inc
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
module: panos_object_facts
short_description: Retrieve facts about objects on PAN-OS devices.
description:
    - Retrieves tag information objects on PAN-OS devices.
author:
    - Michael Richardson (@mrichardson03)
    - Garfield Lee Freeman (@shinmog)
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is supported.
    - Check mode is not supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.vsys
    - paloaltonetworks.panos.fragments.device_group
options:
    name:
        description:
            - Name of object to retrieve.
            - Mutually exclusive with I(name_regex) and I(field).
        type: str
    name_regex:
        description:
            - A python regex for an object's name to retrieve.
            - Mutually exclusive with I(name) and I(field).
        type: str
    field:
        description:
            - The field to search instead of name.
            - Mutually exclusive with I(name) and I(name_regex)
        type: str
    field_search_type:
        description:
            - The type of search to perform when doing a I(field) search.
        type: str
        choices:
            - exact
            - regex
        default: 'exact'
    field_search_value:
        description:
            - The value for the I(field_search) and I(field) specified.
        type: str
    object_type:
        description:
            - Type of object to retrieve.
        type: str
        choices: ['address', 'address-group', 'application', 'application-group', 'custom-url-category', 'service', 'service-group', 'tag']
        default: 'address'
"""

EXAMPLES = """
- name: Retrieve address group object 'Prod'
  panos_object_facts:
    provider: '{{ provider }}'
    name: 'Prod'
    object_type: 'address-group'
  register: result

- name: Retrieve service group object 'Prod-Services'
  panos_object_facts:
    provider: '{{ provider }}'
    name: 'Prod-Services'
    object_type: 'service-group'
  register: result

- name: Find all address objects with "Prod" in the name
  panos_object_facts:
    provider: '{{ provider }}'
    name_regex: '.*Prod.*'
    object_type: 'address'
  register: result

- name: Find all static address objects that use addy1
  panos_object_facts:
    provider: '{{ provider }}'
    object_type: 'address-group'
    field: 'static_value'
    field_search_type: 'exact'
    field_search_value: 'addy1'
  register: result
"""

RETURN = """
ansible_module_results:
    description: Dict containing object attributes.  Empty if object is not found.
    returned: when "name" is specified
    type: dict
objects:
    description: List of object dicts.
    returned: always
    type: list
"""

import re

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    get_connection,
)

try:
    from panos import objects
    from panos.errors import PanDeviceError
except ImportError:
    try:
        from pandevice import objects
        from pandevice.errors import PanDeviceError
    except ImportError:
        pass


COLORS = {
    "color1": "red",
    "color2": "green",
    "color3": "blue",
    "color4": "yellow",
    "color5": "copper",
    "color6": "orange",
    "color7": "purple",
    "color8": "gray",
    "color9": "light green",
    "color10": "cyan",
    "color11": "light gray",
    "color12": "blue gray",
    "color13": "lime",
    "color14": "black",
    "color15": "gold",
    "color16": "brown",
    "color17": "olive",
    "color19": "maroon",
    "color20": "red-orange",
    "color21": "yellow-orange",
    "color22": "forest green",
    "color23": "turquoise blue",
    "color24": "azure blue",
    "color25": "cerulean blue",
    "color26": "midnight blue",
    "color27": "medium blue",
    "color28": "cobalt blue",
    "color29": "violet blue",
    "color30": "blue violet",
    "color31": "medium violet",
    "color32": "medium rose",
    "color33": "lavender",
    "color34": "orchid",
    "color35": "thistle",
    "color36": "peach",
    "color37": "salmon",
    "color38": "magenta",
    "color39": "red violet",
    "color40": "mahogany",
    "color41": "burnt sienna",
    "color42": "chestnut",
}


def colorize(obj, object_type):
    ans = obj.about()
    if object_type == "tag":
        # Fail gracefully if the color is unknown.
        ans["color"] = COLORS.get(obj.color, obj.color)

    return ans


def matches(obj, field, exact=None, regex=None):
    is_str = True
    about = obj.about(field)["About"]
    if isinstance(about, dict):
        is_str = about.get("Type", "string") == "string"

    if exact is not None:
        if is_str:
            return getattr(obj, field) == exact
        else:
            if getattr(obj, field, []) is not None:
                for x in getattr(obj, field, []):
                    if x == exact:
                        return True
            return False
    elif regex is not None:
        if is_str:
            return regex.search(getattr(obj, field)) is not None
        else:
            if getattr(obj, field, []) is not None:
                for x in getattr(obj, field, []):
                    if regex.search(x):
                        return True
            return False

    return False


def main():
    name_params = ["name", "name_regex", "field"]

    helper = get_connection(
        vsys=True,
        device_group=True,
        with_classic_provider_spec=True,
        required_one_of=[
            name_params,
        ],
        argument_spec=dict(
            name=dict(),
            name_regex=dict(),
            field=dict(),
            field_search_type=dict(choices=["exact", "regex"], default="exact"),
            field_search_value=dict(),
            object_type=dict(
                default="address",
                choices=[
                    "address",
                    "address-group",
                    "application",
                    "application-group",
                    "custom-url-category",
                    "service",
                    "service-group",
                    "tag",
                ],
            ),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=False,
        required_one_of=helper.required_one_of,
        mutually_exclusive=[
            name_params,
        ],
    )

    parent = helper.get_pandevice_parent(module)

    obj_types = {
        "address": objects.AddressObject,
        "address-group": objects.AddressGroup,
        "application": objects.ApplicationObject,
        "application-group": objects.ApplicationGroup,
        "custom-url-category": objects.CustomUrlCategory,
        "service": objects.ServiceObject,
        "service-group": objects.ServiceGroup,
        "tag": objects.Tag,
    }

    object_type = module.params["object_type"]
    obj_type = obj_types[object_type]

    try:
        obj_listing = obj_type.refreshall(parent)
    except PanDeviceError as e:
        module.fail_json(msg="Failed {0} refresh: {1}".format(object_type, e))

    results = {}
    ans_objects = []
    if module.params["name"] is not None:
        obj = parent.find(module.params["name"], obj_type)
        if obj:
            results = colorize(obj, object_type)
            ans_objects.append(results)
    elif module.params["name_regex"]:
        try:
            matcher = re.compile(module.params["name_regex"])
        except Exception as e:
            module.fail_json(msg="Invalid regex: {0}".format(e))

        ans_objects = [
            colorize(x, object_type)
            for x in obj_listing
            if matcher.search(x.uid) is not None
        ]
    else:
        # Sanity checks.
        if not hasattr(obj_type(), module.params["field"]):
            module.fail_json(
                msg="Object({0}) does not have field({1})".format(
                    object_type, module.params["field"]
                )
            )
        elif not module.params["field_search_value"]:
            module.fail_json(
                msg="Searching a field requires that field_search_value is specified"
            )

        # Perform requested search type.
        if module.params["field_search_type"] == "exact":
            ans_objects = [
                colorize(x, object_type)
                for x in obj_listing
                if matches(
                    x, module.params["field"], exact=module.params["field_search_value"]
                )
            ]
        elif module.params["field_search_type"] == "regex":
            try:
                regex = re.compile(module.params["field_search_value"])
            except Exception as e:
                module.fail_json(msg="Invalid field regex: {0}".format(e))

            ans_objects = [
                colorize(x, object_type)
                for x in obj_listing
                if matches(x, module.params["field"], regex=regex)
            ]

    # Done.
    module.exit_json(changed=False, ansible_module_results=results, objects=ans_objects)


if __name__ == "__main__":
    main()
