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
module: panos_log_forwarding_profile_match_list
short_description: Manage log forwarding profile match lists.
description:
    - Manages log forwarding profile match lists.
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
    log_forwarding_profile:
        description:
            - Name of the log forwarding profile to add this match list to.
        type: str
        required: True
    name:
        description:
            - Name of the profile.
        type: str
    description:
        description:
            - Profile description
        type: str
    log_type:
        description:
            - Log type.
        type: str
        choices:
            - traffic
            - threat
            - wildfire
            - url
            - data
            - gtp
            - tunnel
            - auth
            - sctp
            - decryption
        default: 'traffic'
    filter:
        description:
            - The filter.  Leaving this empty means "All logs".
        type: str
    send_to_panorama:
        description:
            - Send to panorama or not
        type: bool
    snmp_profiles:
        description:
            - List of SNMP server profiles.
        type: list
        elements: str
    email_profiles:
        description:
            - List of email server profiles.
        type: list
        elements: str
    syslog_profiles:
        description:
            - List of syslog server profiles.
        type: list
        elements: str
    http_profiles:
        description:
            - List of HTTP server profiles.
        type: list
        elements: str
"""

EXAMPLES = """
# Create a server match list
- name: Create log forwarding profile match list
  paloaltonetworks.panos.panos_log_forwarding_profile_match_list:
    provider: '{{ provider }}'
    log_forwarding_profile: 'my-profile'
    name: 'ml-1'
    description: 'created by Ansible'
    log_type: 'threat'
    filter: '(action eq allow) and (zone eq DMZ)'
    syslog_profiles: ['syslog-prof1']
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
        min_pandevice_version=(1, 11, 0),
        min_panos_version=(8, 0, 0),
        parents=(("objects", "LogForwardingProfile", "log_forwarding_profile"),),
        sdk_cls=("objects", "LogForwardingProfileMatchList"),
        sdk_params=dict(
            name=dict(required=True),
            description=dict(),
            log_type=dict(
                default="traffic",
                choices=[
                    "traffic",
                    "threat",
                    "wildfire",
                    "url",
                    "data",
                    "gtp",
                    "tunnel",
                    "auth",
                    "sctp",
                    "decryption",
                ],
            ),
            filter=dict(),
            send_to_panorama=dict(type="bool"),
            snmp_profiles=dict(type="list", elements="str"),
            email_profiles=dict(type="list", elements="str"),
            syslog_profiles=dict(type="list", elements="str"),
            http_profiles=dict(type="list", elements="str"),
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
