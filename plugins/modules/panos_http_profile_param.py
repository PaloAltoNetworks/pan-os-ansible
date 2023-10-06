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
module: panos_http_profile_param
short_description: Manage HTTP params for a HTTP profile.
description:
    - Manages HTTP params for a HTTP profile.
author: "Garfield Lee Freeman (@shinmog)"
version_added: '1.0.0'
requirements:
    - pan-python
    - pandevice >= 0.11.1
    - PAN-OS >= 8.0
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
    http_profile:
        description:
            - Name of the http server profile.
        type: str
        required: True
    log_type:
        description:
            - The log type for this parameter.
        type: str
        choices:
            - auth
            - config
            - data
            - decryption
            - globalprotect
            - gtp
            - hip match
            - iptag
            - sctp
            - system
            - threat
            - traffic
            - tunnel
            - url
            - user id
            - wildfire
        required: True
    param:
        description:
            - The param name.
        type: str
    value:
        description:
            - The value to assign the param.
        type: str
"""

EXAMPLES = """
- name: Add a param to the config log type
  paloaltonetworks.panos.panos_http_profile_param:
    provider: '{{ provider }}'
    http_profile: 'my-profile'
    log_type: 'user id'
    param: 'serial'
    value: '$serial'
"""

RETURN = """
# Default return values
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    ConnectionHelper,
    get_connection,
)


class Helper(ConnectionHelper):
    def spec_handling(self, spec, module):
        cls_map = {
            "config": "HttpConfigParam",
            "system": "HttpSystemParam",
            "threat": "HttpThreatParam",
            "traffic": "HttpTrafficParam",
            "hip match": "HttpHipMatchParam",
            "url": "HttpUrlParam",
            "data": "HttpDataParam",
            "wildfire": "HttpWildfireParam",
            "tunnel": "HttpTunnelParam",
            "user id": "HttpUserIdParam",
            "gtp": "HttpGtpParam",
            "auth": "HttpAuthParam",
            "sctp": "HttpSctpParam",
            "iptag": "HttpIpTagParam",
            "decryption": "HttpDecryptionParam",
            "globalprotect": "HttpGlobalProtectParam",
        }

        self.sdk_cls = ("device", cls_map[module.params["log_type"]])


def main():
    helper = get_connection(
        helper_cls=Helper,
        vsys_shared=True,
        device_group=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        with_classic_provider_spec=True,
        min_pandevice_version=(1, 10, 0),
        min_panos_version=(8, 0, 0),
        parents=(("device", "HttpServerProfile", "http_profile"),),
        sdk_params=dict(
            param=dict(required=True, sdk_param="name"),
            value=dict(),
        ),
        extra_params=dict(
            log_type=dict(
                required=True,
                choices=[
                    "config",
                    "system",
                    "threat",
                    "traffic",
                    "hip match",
                    "url",
                    "data",
                    "wildfire",
                    "tunnel",
                    "user id",
                    "gtp",
                    "auth",
                    "sctp",
                    "iptag",
                    "decryption",
                    "globalprotect",
                ],
            ),
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
