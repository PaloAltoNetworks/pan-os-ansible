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
module: panos_bgp_auth
short_description: Manage a BGP Authentication Profile
description:
    - Use BGP to publish and consume routes from disparate networks.
author:
    - Joshua Colson (@freakinhippie)
    - Garfield Lee Freeman (@shinmog)
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is not supported.
    - Panorama is supported.
    - Since the I(secret) value is encrypted in PAN-OS, there is no way to verify
      if the secret is properly set or not.  Invoking this module with I(state=present)
      will always apply the config to PAN-OS.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.full_template_support
    - paloaltonetworks.panos.fragments.deprecated_commit
    - paloaltonetworks.panos.fragments.gathered_filter
options:
    name:
        description:
            - Name of Authentication Profile.
        type: str
    replace:
        description:
            - B(Deprecated)
            - This is the behavior of I(state=present), so this can safely be removed from your playbooks.
            - HORIZONTALLINE
            - The secret is encrypted so the state cannot be compared.
            - This option forces removal of a matching item before applying the new config.
        type: bool
    secret:
        description:
            - Secret.
        type: str
    vr_name:
        description:
            - Name of the virtual router, it must already exist.  See M(paloaltonetworks.panos.panos_virtual_router).
        type: str
        default: 'default'
"""

EXAMPLES = """
- name: Create BGP Authentication Profile
  paloaltonetworks.panos.panos_bgp_auth:
    provider: '{{ provider }}'
    vr_name: 'my virtual router'
    name: auth-profile-1
    secret: SuperSecretCode
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
    def initial_handling(self, module):
        if module.params["replace"] is not None:
            module.deprecate(
                'Param "replace" is deprecated; please use state instead',
                version="4.0.0",
                collection_name="paloaltonetworks.panos",
            )


def main():
    helper = get_connection(
        helper_cls=Helper,
        template=True,
        template_stack=True,
        with_network_resource_module_state=True,
        with_classic_provider_spec=True,
        with_commit=True,
        with_gathered_filter=True,
        parents=(
            ("network", "VirtualRouter", "vr_name", "default"),
            ("network", "Bgp", None),
        ),
        sdk_cls=("network", "BgpAuthProfile"),
        sdk_params=dict(
            name=dict(required=True),
            secret=dict(no_log=True),
        ),
        extra_params=dict(
            replace=dict(type="bool"),
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
