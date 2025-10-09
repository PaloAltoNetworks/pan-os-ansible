#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2022 Palo Alto Networks, Inc
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
module: panos_dhcp
short_description: Manage DHCP for an interface.
description:
    - Manage DHCP on PAN-OS firewall.
    - Besides I(state=gathered) to see the the entire DHCP config related to a
      specific interface, you will need to use this module to delete the interface
      reference from the PAN-OS config if you intent to delete the interface being
      refered to.
author:
    - Garfield Lee Freeman (@shinmog)
version_added: '2.10.0'
requirements:
    - pan-python >= 0.17
    - pan-os-python >= 1.7.3
notes:
    - Check mode is supported.
    - Panorama is not supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
options:
    interface:
        description:
            - The interface name.
        type: str
"""

EXAMPLES = """
# Gather all DHCP configuration for an interface
- paloaltonetworks.panos.panos_dhcp:
    provider: '{{ provider }}'
    interface: 'ethernet1/1'
    state: 'gathered'

# Delete any and all DHCP configuration
- paloaltonetworks.panos.panos_dhcp:
    provider: '{{ provider }}'
    interface: 'ethernet1/1'
    state: absent
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
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        with_classic_provider_spec=True,
        panorama_error="This is a firewall only module",
        min_pandevice_version=(1, 7, 3),
        sdk_cls=("network", "Dhcp"),
        sdk_params=dict(
            interface=dict(required=True, sdk_param="name"),
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
