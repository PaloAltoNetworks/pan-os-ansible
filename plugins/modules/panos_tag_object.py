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
module: panos_tag_object
short_description: Create tag objects on PAN-OS devices.
description:
    - Create tag objects on PAN-OS devices.
author: "Michael Richardson (@mrichardson03)"
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.vsys
    - paloaltonetworks.panos.fragments.device_group
    - paloaltonetworks.panos.fragments.state
    - paloaltonetworks.panos.fragments.deprecated_commit
options:
    name:
        description:
            - Name of the tag.
        type: str
        required: true
    color:
        description:
            - Color for the tag.
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
    comments:
        description:
            - Comments for the tag.
        type: str
"""

EXAMPLES = """
- name: Create tag object 'Prod'
  panos_tag_object:
    provider: '{{ provider }}'
    name: 'Prod'
    color: 'red'
    comments: 'Prod Environment'

- name: Remove tag object 'Prod'
  panos_tag_object:
    provider: '{{ provider }}'
    name: 'Prod'
    state: 'absent'
"""

RETURN = """
# Default return values
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    get_connection,
)

try:
    from panos.errors import PanDeviceError
    from panos.objects import Tag
except ImportError:
    try:
        from pandevice.errors import PanDeviceError
        from pandevice.objects import Tag
    except ImportError:
        pass

COLOR_NAMES = [
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
]


def main():
    helper = get_connection(
        vsys=True,
        device_group=True,
        with_classic_provider_spec=True,
        with_state=True,
        argument_spec=dict(
            name=dict(type="str", required=True),
            color=dict(type="str", default=None, choices=COLOR_NAMES),
            comments=dict(type="str"),
            commit=dict(type="bool", default=False),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        required_one_of=helper.required_one_of,
        supports_check_mode=True,
    )

    parent = helper.get_pandevice_parent(module)

    spec = {"name": module.params["name"], "comments": module.params["comments"]}

    if module.params["color"]:
        spec["color"] = Tag.color_code(module.params["color"])

    commit = module.params["commit"]

    try:
        listing = Tag.refreshall(parent, add=False)
    except PanDeviceError as e:
        module.fail_json(msg="Failed refresh: {0}".format(e))

    obj = Tag(**spec)
    parent.add(obj)

    changed, diff = helper.apply_state(obj, listing, module)

    if commit and changed:
        helper.commit(module)

    module.exit_json(changed=changed, diff=diff)


if __name__ == "__main__":
    main()
