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
short_description: Manage tag objects on PAN-OS devices.
description:
    - Manage tag objects on PAN-OS devices.
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
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.deprecated_commit
    - paloaltonetworks.panos.fragments.gathered_filter
options:
    name:
        description:
            - Name of the tag.
        type: str
    color_value:
        description:
            - The XML value of the color for this tag.
            - Mutually exclusive with I(color).
        type: str
    color:
        description:
            - Color for the tag.
            - Mutually exclusive with I(color_value).
            - NOTE that this param is not available for I(gathered_filter) as it is a meta-param.
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
  paloaltonetworks.panos.panos_tag_object:
    provider: '{{ provider }}'
    name: 'Prod'
    color: 'red'
    comments: 'Prod Environment'

- name: Remove tag object 'Prod'
  paloaltonetworks.panos.panos_tag_object:
    provider: '{{ provider }}'
    name: 'Prod'
    state: 'absent'
"""

RETURN = """
# Default return values
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    ConnectionHelper,
    get_connection,
)


COLOR_NAMES = [
    "",
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
    "",
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


def to_color(color_value):
    """Returns the color for the given color_value."""
    if color_value is None or not color_value.startswith("color"):
        return None
    cv = int(color_value[5:])
    return COLOR_NAMES[cv]


class Helper(ConnectionHelper):
    def initial_handling(self, module):
        if module.params["color"] and module.params["color_value"]:
            module.fail_json(msg="Specify either 'color' or 'color_value', not both")

    def spec_handling(self, spec, module):
        if (
            module.params["state"] not in ("present", "replaced")
            or not module.params["color"]
        ):
            return

        for num, x in enumerate(COLOR_NAMES):
            if module.params["color"] == x:
                spec["color"] = "color{0}".format(num)
                break
        else:
            module.fail_json(
                msg="Unable to find color_value for color: {0}".format(
                    module.params["color"]
                )
            )

    def post_state_handling(self, obj, result, module):
        if "before" in result and result["before"] is not None:
            result["before"]["color"] = to_color(result["before"]["color_value"])

        if "after" in result and result["after"] is not None:
            result["after"]["color"] = to_color(result["after"]["color_value"])

        if "gathered" in result:
            if isinstance(result["gathered"], dict):
                result["gathered"]["color"] = to_color(
                    result["gathered"]["color_value"]
                )
            elif isinstance(result["gathered"], list):
                for x in result["gathered"]:
                    x["color"] = to_color(x["color_value"])


def main():
    helper = get_connection(
        helper_cls=Helper,
        vsys=True,
        device_group=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        with_classic_provider_spec=True,
        with_commit=True,
        sdk_cls=("objects", "Tag"),
        sdk_params=dict(
            name=dict(required=True),
            color_value=dict(sdk_param="color"),
            comments=dict(),
        ),
        extra_params=dict(
            color=dict(choices=[x for x in COLOR_NAMES if x]),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        required_one_of=helper.required_one_of,
        supports_check_mode=True,
    )

    helper.process(module)


if __name__ == "__main__":
    main()
