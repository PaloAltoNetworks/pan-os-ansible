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
module: panos_zone
short_description: Manage security zone
description:
    - Manage security zones on PAN-OS firewall or in Panorama template.
author:
    - Robert Hagen (@stealthllama)
    - Garfield Lee Freeman (@shinmog)
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
    - pandevice >= 0.8.0
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
    - paloaltonetworks.panos.fragments.full_template_support
    - paloaltonetworks.panos.fragments.vsys
options:
    zone:
        description:
            - Name of the security zone to configure.
        type: str
    mode:
        description:
            - The mode of the security zone. Must match the mode of the interface.
        type: str
        choices:
            - tap
            - virtual-wire
            - layer2
            - layer3
            - external
        default: "layer3"
    interface:
        description:
            - List of member interfaces.
        type: list
        elements: str
    zone_profile:
        description:
            - Zone protection profile.
        type: str
    log_setting:
        description:
            - Log forwarding setting.
        type: str
    enable_userid:
        description:
            - Enable user identification.
        type: bool
        default: False
    include_acl:
        description:
            - User identification ACL include list.
        type: list
        elements: str
    exclude_acl:
        description:
            - User identification ACL exclude list.
        type: list
        elements: str
"""

EXAMPLES = """
# Create an L3 zone.
- name: create DMZ zone on a firewall
  paloaltonetworks.panos.panos_zone:
    provider: '{{ provider }}'
    zone: 'dmz'
    mode: 'layer3'
    zone_profile: 'strict'

# Add an interface to the zone.
- name: add ethernet1/2 to zone dmz
  paloaltonetworks.panos.panos_interface:
    provider: '{{ provider }}'
    zone: 'dmz'
    mode: 'layer3'
    interface: ['ethernet1/2']
    zone_profile: 'strict'

# Delete the zone.
- name: delete the DMZ zone
  paloaltonetworks.panos.panos_interface:
    provider: '{{ provider }}'
    zone: 'dmz'
    state: 'absent'

# Add a zone to a multi-VSYS Panorama template
- name: add Cloud zone to template
  paloaltonetworks.panos.panos_interface:
    provider: '{{ provider }}'
    template: 'Datacenter Template'
    vsys: 'vsys4'
    zone: 'datacenter'
    mode: 'layer3'
    enable_userid: true
    exclude_acl: ['10.0.200.0/24']
"""

RETURN = """
# Default return values
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    get_connection,
)


def main():
    helper = get_connection(
        vsys=True,
        template=True,
        template_stack=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        with_classic_provider_spec=True,
        sdk_cls=("network", "Zone"),
        sdk_params=dict(
            zone=dict(required=True, sdk_param="name"),
            mode=dict(
                choices=["tap", "virtual-wire", "layer2", "layer3", "external"],
                default="layer3",
            ),
            interface=dict(type="list", elements="str"),
            zone_profile=dict(),
            log_setting=dict(),
            enable_userid=dict(
                type="bool", default=False, sdk_param="enable_user_identification"
            ),
            include_acl=dict(type="list", elements="str"),
            exclude_acl=dict(type="list", elements="str"),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    helper.process(module)


if __name__ == "__main__":
    main()
