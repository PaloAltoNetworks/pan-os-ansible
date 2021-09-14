#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2021 Palo Alto Networks, Inc
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
module: panos_template_variable
short_description: configure template or template stack variable
description:
    - Configure a template or template stack variable on Panorama.
author:
    - Garfield Lee Freeman (@shinmog)
version_added: '2.8.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
    - pandevice >= 1.5.1
notes:
    - Panorama is supported.
    - This is a Panorama only module.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.provider
    - paloaltonetworks.panos.fragments.state
    - paloaltonetworks.panos.fragments.full_template_support
options:
    name:
        description:
            - Name of the variable.
            - Variable names should start with the dollar sign.
        type: str
        required: true
    value:
        description:
            - The variable value.
        type: str
    variable_type:
        description:
            - The variable type.
        type: str
        default: 'ip-netmask'
        choices:
            - ip-netmask
            - ip-range
            - fqdn
            - group-id
            - interface
            - device-priority
            - device-id
"""

EXAMPLES = """
# Create a template variable.
- name: create template variable
  panos_template_variable:
    provider: '{{ provider }}'
    template: 'tmpl name'
    name: '$ip1'
    value: '192.168.1.1'
    variable_type: 'ip-netmask'

# Create a fqdn template stack variable
- name: create fqdn template stack variable
  panos_template_variable:
    name: '$fqdn1'
    value: 'example.com'
    variable_type: 'fqdn'
"""

RETURN = """
# Default return values
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    get_connection,
)

try:
    from panos.errors import PanDeviceError, PanObjectMissing
    from panos.panorama import TemplateVariable
except ImportError:
    try:
        from pandevice.errors import PanDeviceError, PanObjectMissing
        from pandevice.panorama import TemplateVariable
    except ImportError:
        pass


def main():
    helper = get_connection(
        template=True,
        template_stack=True,
        with_state=True,
        firewall_error="This is a Panorama module",
        argument_spec=dict(
            name=dict(required=True),
            value=dict(),
            variable_type=dict(
                type="str",
                default="ip-netmask",
                choices=[
                    "ip-netmask",
                    "ip-range",
                    "fqdn",
                    "group-id",
                    "interface",
                    "device-priority",
                    "device-id",
                ],
            ),
        ),
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # Verify imports, build pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    # Object params.
    spec = {
        "name": module.params["name"],
        "value": module.params["value"],
        "variable_type": module.params["variable_type"],
    }

    # Check for current object.
    listing = []
    live_obj = TemplateVariable(spec["name"])
    parent.add(live_obj)
    try:
        live_obj.refresh()
    except PanObjectMissing:
        live_obj = None
    except PanDeviceError as e:
        module.fail_json(msg="Failed refresh: {0}".format(e))
    else:
        listing.append(live_obj)

    # Build the object and attach to the parent.
    obj = TemplateVariable(**spec)
    parent.add(obj)

    # Perform the requested action.
    changed, diff = helper.apply_state(obj, listing, module)

    # Done!
    module.exit_json(changed=changed, diff=diff, msg="Done!")


if __name__ == "__main__":
    main()
