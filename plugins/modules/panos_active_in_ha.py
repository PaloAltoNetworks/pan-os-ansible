#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2023 Palo Alto Networks, Inc
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
module: panos_active_in_ha
short_description: Checks if node is an active node in HA pair.
description:
    - A wrapper around the PAN-OS Upgrade Assurance package.
    - A simple boolean check, verifies if a node is an active (B(true)) or passive (B(false)) node in an HA pair.
    - If node does not belong to an HA pair or the pair is no configured correctly the module will fail.
author: "Łukasz Pawlęga (@fosix)"
version_added: '2.18.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
    - panos-upgrade-assurance can be obtained from PyPI U(https://pypi.org/project/panos-upgrade-assurance)
notes:
    - Panorama is not supported.
    - Check mode is not supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.vsys
options:
    force_fail:
        description:
            - When set to B(true) will make the module fail also when node is passive.
              This option is useful when we want to skip using M(ansible.builtin.assert).
        type: bool
        default: false
    skip_config_sync:
        description:
            - When set to B(true) will skip configuration synchronization state between nodes before trying to retrieve
              node's current state in an HA pair. Can be useful when working with partially upgraded nodes. Use with caution.
        type: bool
        default: false
    ignore_non_functional:
        description:
            - Use with caution, when set to `True` will ignore if device state is `non-functional` on one of the nodes. Helpful
              when verifying a state of a partially upgraded HA pair with vmseries plugin version mismatch.
        type: bool
        default: false
# """

EXAMPLES = """
- name: Check if a node is active in HA pair
  panos_active_in_ha:
    provider: '{{ provider }}'
  register: active_ha
- name: Run tasks dedicated to active node
  ansible.builtin.include_tasks: active_dedicated.yml
  when: active_ha.response.active
"""

RETURN = """
# Default return values
response:
    description:
        - Information on test results.
        - This dict is available also when module is failed.
    returned: always
    type: dict
    sample:
        active: true
        reason: '[SUCCESS]'
    contains:
        active:
            description: Information if the device is active or not.
            returned: always
            type: bool
        reason:
            description: Meaningful if the device is not active.
            returned: always
            type: str
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    get_connection,
)

try:
    from panos_upgrade_assurance.check_firewall import CheckFirewall
    from panos_upgrade_assurance.firewall_proxy import FirewallProxy
    from panos_upgrade_assurance.utils import CheckStatus
except ImportError:
    pass

MIN_PUA_VER = (0, 3, 0)


def main():
    results = dict()

    helper = get_connection(
        vsys=True,
        with_classic_provider_spec=True,
        min_panos_upgrade_assurance_version=MIN_PUA_VER,
        argument_spec=dict(
            force_fail=dict(type="bool", default=False),
            skip_config_sync=dict(type="bool", default=False),
            ignore_non_functional=dict(type="bool", default=False),
        ),
        panorama_error="This is a firewall only module",
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec, supports_check_mode=False
    )

    firewall = FirewallProxy(firewall=helper.get_pandevice_parent(module))

    is_active = CheckFirewall(firewall).check_is_ha_active(
        skip_config_sync=module.params["skip_config_sync"],
        ignore_non_functional=module.params["ignore_non_functional"],
    )

    if module.params["force_fail"]:
        response = str(is_active)
        module_failed = not bool(is_active)
    else:
        response = {"active": bool(is_active), "reason": str(is_active)}
        module_failed = (
            True
            if is_active.status in [CheckStatus.ERROR, CheckStatus.SKIPPED]
            else False
        )

    module.exit_json(changed=False, response=response, failed=module_failed)


if __name__ == "__main__":
    main()
