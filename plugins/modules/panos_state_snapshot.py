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
module: panos_state_snapshot
short_description: Takes a snapshot of a state of a Firewall device.
description:
    - A wrapper around the PAN-OS Upgrade Assurance package.
    - The module takes a snapshot of a state of specified areas. It runs the package's CheckFirewall.run_snapshots()
      L(method, https://pan.dev/panos/docs/panos-upgrade-assurance/api/check_firewall/#checkfirewallrun_snapshots).
      Since it's just a wrapper, the way you would configure snapshot area is exactly the same as if you would run the class directly.
      Please refer to package's documentation for L(syntax,https://pan.dev/panos/docs/panos-upgrade-assurance/configuration-details/#readiness-checks)
      and L(configuration dialect,https://pan.dev/panos/docs/panos-upgrade-assurance/dialect/).
author: "Łukasz Pawlęga (@fosix)"
version_added: '2.18.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
    - panos-upgrade-assurance can be obtained from PyPI U(https://pypi.python.org/pypi/panos-upgrade-assurance)
notes:
    - Panorama is not supported.
    - Check mode is not supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.vsys
options:
    state_areas:
        description:
            - A list of Firewall state areas that we should take a snapshot of. For the details on currently supported list please refer to
              L(package documentation, https://pan.dev/panos/docs/panos-upgrade-assurance/configuration-details/#state-snapshots).
            - In most of the cases it is enough to specify a snapshot name to run it with default settings.
              In this case the list element is of type B(str). If additional configuration is required the element is a single element B(dict),
              where key is the state snapshot name and value contains the snapshot's configuration. For information which snapshot requires additional
              configuration please refer to L(package documentation, https://pan.dev/panos/docs/panos-upgrade-assurance/configuration-details/#state-snapshots).
            - To capture the actual snapshot data use a register.
        type: list
        elements: raw
        default: ["all"]
"""

EXAMPLES = """
- name: Run snapshot of all areas except for session statistics
  panos_state_snapshot:
    provider: '{{ device }}'
    state_areas:
      - '!session_stats'
    register: snapshot
"""

RETURN = """
response:
    description:
        - This is a B(dict) where keys are state areas names just as you specify them in the I(state_areas) property.
        - Values contain the snapshot data. Type and structure differs per state area. Please refer to
          L(package documentation, https://pan.dev/panos/docs/panos-upgrade-assurance/configuration-details/#state-snapshots) for details.
    type: dict
    returned: always
    sample:
        arp_table: {}
        content_version:
            version: 8635-7675
        ip_sec_tunnels: {}
        license:
            DNS Security:
                authcode: null
                base-license-name: PA-VM
                description: Palo Alto Networks DNS Security License
                expired: no
                expires: December 31, 2023
                feature: DNS Security
                issued: April 13, 2023
                serial: "xxxxxxxxxxxxxxxxx"
            PA-VM:
                authcode: null
                description: Standard VM-300
                expired: no
                expires: December 31, 2023
                feature: PA-VM
                issued: April 13, 2023
                serial: "xxxxxxxxxxxxxxxxx"
        routes: {}
        session_stats:
            age-accel-thresh: "80"
            age-accel-tsf: "2"
            age-scan-ssf: "8"
            age-scan-thresh: "80"
            age-scan-tmo: "10"
            cps: "0"
            dis-def: "60"
            dis-sctp: "30"
            dis-tcp: "90"
            dis-udp: "60"
            icmp-unreachable-rate: "200"
            kbps: "0"
            max-pending-mcast: "0"
            num-active: "0"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    get_connection,
)

MIN_PUA_VER = (0, 3, 0)

try:
    from panos_upgrade_assurance.firewall_proxy import FirewallProxy
    from panos_upgrade_assurance.check_firewall import CheckFirewall
except ImportError:
    pass


def main():
    results = dict()

    helper = get_connection(
        vsys=True,
        with_classic_provider_spec=True,
        min_panos_upgrade_assurance_version=MIN_PUA_VER,
        argument_spec=dict(
            state_areas=dict(type="list", default=["all"], elements="raw")
        ),
        panorama_error="This is a firewall only module",
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec, supports_check_mode=False
    )

    firewall = FirewallProxy(firewall=helper.get_pandevice_parent(module))
    checks = CheckFirewall(firewall)
    results = checks.run_snapshots(module.params["state_areas"])

    module.exit_json(changed=False, response=results)


if __name__ == "__main__":
    main()
