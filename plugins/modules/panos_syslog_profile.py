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
module: panos_syslog_profile
short_description: Manage syslog server profiles.
description:
    - Manages syslog server profiles.
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
    name:
        description:
            - Name of the profile.
        type: str
    config:
        description:
            - Custom config log format.
        type: str
    system:
        description:
            - Custom system log format.
        type: str
    threat:
        description:
            - Custom threat log format.
        type: str
    traffic:
        description:
            - Custom traffic log format.
        type: str
    hip_match:
        description:
            - Custom HIP match log format.
        type: str
    url:
        description:
            - PAN-OS 8.0+
            - Custom url log format.
        type: str
    data:
        description:
            - PAN-OS 8.0+
            - Custom data log format.
        type: str
    wildfire:
        description:
            - PAN-OS 8.0+
            - Custom wildfire log format.
        type: str
    tunnel:
        description:
            - PAN-OS 8.0+
            - Custom tunnel log format.
        type: str
    user_id:
        description:
            - PAN-OS 8.0+
            - Custom user-ID log format.
        type: str
    gtp:
        description:
            - PAN-OS 8.0+
            - Custom GTP log format.
        type: str
    auth:
        description:
            - PAN-OS 8.0+
            - Custom auth log format.
        type: str
    sctp:
        description:
            - PAN-OS 8.1+
            - Custom SCTP log format.
        type: str
    iptag:
        description:
            - PAN-OS 9.0+
            - Custom Iptag log format.
        type: str
    escaped_characters:
        description:
            - Characters to be escaped.
        type: str
    escape_character:
        description:
            - Escape character
        type: str
"""

EXAMPLES = """
# Create a profile
- name: Create syslog profile
  paloaltonetworks.panos.panos_syslog_profile:
    provider: '{{ provider }}'
    name: 'my-profile'
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
        sdk_cls=("device", "SyslogServerProfile"),
        sdk_params=dict(
            name=dict(required=True),
            config=dict(),
            system=dict(),
            threat=dict(),
            traffic=dict(),
            hip_match=dict(),
            url=dict(),
            data=dict(),
            wildfire=dict(),
            tunnel=dict(),
            user_id=dict(),
            gtp=dict(),
            auth=dict(),
            sctp=dict(),
            iptag=dict(),
            escaped_characters=dict(),
            escape_character=dict(),
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
