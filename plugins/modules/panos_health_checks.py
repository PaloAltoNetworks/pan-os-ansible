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
module: panos_health_checks
short_description: Runs health checks (boolean in nature) against a Firewall device.
description:
    - A wrapper around the PAN-OS Upgrade Assurance package.
    - The module is meant to run health checks available in the package's CheckFirewall.run_health_checks()
      L(method,https://pan.dev/panos/docs/panos-upgrade-assurance/api/check_firewall/#checkfirewallrun_health_checks).
      Since it's just a wrapper, the way you would configure a check is exactly the same as if you would run the class directly.
      Please refer to package's documentation for L(syntax,https://pan.dev/panos/docs/panos-upgrade-assurance/configuration-details/#health-checks)
      and L(configuration dialect,https://pan.dev/panos/docs/panos-upgrade-assurance/dialect/).
    - Health checks are designed to check the overall status of the system is ok and it is not affected by any specific 
      security or software advisories.
author: "Adam Baumeister (@adambaumeister)"
version_added: '2.18.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
    - pan-os-upgrade-assurance can be obtained from PyPI U(https://pypi.org/project/panos-upgrade-assurance)
notes:
    - Panorama is not supported.
    - Check mode is not supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.vsys
options:
    checks:
        description:
            - A list of checks that should be run against a device. For the details on currently supported checks please refer to
              L(package's documentation,https://pan.dev/panos/docs/panos-upgrade-assurance/configuration-details/#health-checks).
            - In most of the cases it is enough to specify a check name to run it with default settings.
              In this case the list element is of type B(str). If additional configuration is required the element is a one element B(dict),
              where key is the check name and value contains the check's configuration. For information which check requires additional configuration
              please refer to L(package documentation,https://pan.dev/panos/docs/panos-upgrade-assurance/configuration-details/#health-checks).
        type: list
        elements: raw
        default: ["all"]
    force_fail:
        description: When set to B(true) will make the module fail when at least one of the checks did not pass.
        type: bool
        default: false
    skip_force_locale:
        description:
            - When set to B(true) will skip the B(en_US.UTF-8) locales on the checks.
            - Use with caution only when you actually use different, English based locales but you do not have B(en_US.UTF-8) installed.
        type: bool
        default: false
"""

EXAMPLES = """
- name: Run all Health Checks
  panos_health_checks:
    provider: '{{ device }}'
"""

RETURN = """
response:
    description:
        - This is a B(dict) where keys are checks names just as you specify them in the I(checks) property.
        - Each value is also a B(dict).
        - When I(force_fail) has the default value of B(false) this B(dict) contains results for all checks that were specified in I(checks) property.
        - When I(force_fail) is set to B(true) it contains only checks that failed.
    type: dict
    returned: always
    sample:
        device_root_certificate_issue::
            reason: "[FAIL] Device is running a software version that is impacted by the device root certificate expiry"
            state: false
    contains:
        state:
            description: A result of a check.
            type: bool
            returned: always
        reason:
            description:
                - A free text describing the check result.
                - 'Prefixed with a keyword: SUCCESS, FAIL, ERROR, SKIPPED.'
                - Meaningful only for failed tests as the ones succeeded are self explanatory.
            type: str
            returned: always
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    get_connection,
)

MIN_PUA_VER = (0, 3, 0)

try:
    from panos_upgrade_assurance.check_firewall import CheckFirewall
    from panos_upgrade_assurance.firewall_proxy import FirewallProxy
except ImportError:
    pass


def main():
    results = dict()

    helper = get_connection(
        vsys=True,
        with_classic_provider_spec=True,
        min_panos_upgrade_assurance_version=MIN_PUA_VER,
        argument_spec=dict(
            checks=dict(type="list", default=["all"], elements="raw"),
            force_fail=dict(type="bool", default=False),
            skip_force_locale=dict(type="bool", default=False),
        ),
        panorama_error="This is a firewall only module",
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=False,
    )
    results = dict()
    module_failed = False

    firewall = FirewallProxy(firewall=helper.get_pandevice_parent(module))

    checks = CheckFirewall(
        node=firewall, skip_force_locale=module.params["skip_force_locale"]
    )
    results = checks.run_health_checks(checks_configuration=module.params["checks"])

    if module.params["force_fail"]:
        for check in list(results.keys()):
            if results[check]["state"]:
                del results[check]
            else:
                module_failed = True

    module.exit_json(changed=False, response=results, failed=module_failed)


if __name__ == "__main__":
    main()
