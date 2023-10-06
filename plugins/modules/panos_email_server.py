#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2019 Palo Alto Networks, Inc
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
module: panos_email_server
short_description: Manage email servers in an email profile.
description:
    - Manages email servers in an email server profile.
author: "Garfield Lee Freeman (@shinmog)"
version_added: '1.0.0'
requirements:
    - pan-python
    - pandevice >= 0.11.1
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.vsys_shared
    - paloaltonetworks.panos.fragments.device_group
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
options:
    email_profile:
        description:
            - Name of the email server profile.
        type: str
        required: True
    name:
        description:
            - Server name.
        type: str
    display_name:
        description:
            - Display name
        type: str
    from_email:
        description:
            - From email address
        type: str
    to_email:
        description:
            - Destination email address.
        type: str
    also_to_email:
        description:
            - Additional destination email address
        type: str
    email_gateway:
        description:
            - IP address or FQDN of email gateway to use.
        type: str
    protocol:
        description:
            - Specify whether to use clear-text or encrypted SMTP.
        type: str
        choices:
            - SMTP
            - TLS
        default: SMTP
"""

EXAMPLES = """
# Create a profile
- name: Create email server in an email profile
  paloaltonetworks.panos.panos_email_server:
    provider: '{{ provider }}'
    email_profile: 'my-profile'
    name: 'my-email-server'
    from_email: 'alerts@example.com'
    to_email: 'notify@example.com'
    email_gateway: 'smtp.example.com'
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
        vsys_shared=True,
        device_group=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        with_classic_provider_spec=True,
        min_pandevice_version=(0, 11, 1),
        min_panos_version=(7, 1, 0),
        parents=(("device", "EmailServerProfile", "email_profile"),),
        sdk_cls=("device", "EmailServer"),
        sdk_params=dict(
            name=dict(required=True),
            display_name=dict(),
            from_email=dict(sdk_param="from"),
            to_email=dict(sdk_param="to"),
            also_to_email=dict(sdk_param="also_to"),
            email_gateway=dict(),
            protocol=dict(choices=["SMTP", "TLS"], default="SMTP"),
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
