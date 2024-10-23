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
module: panos_snapshot_report
short_description: Generates a report by comparing two snapshot made with the M(paloaltonetworks.panos.panos_state_snapshot) module.
description:
    - A wrapper around the PAN-OS Upgrade Assurance package.
    - This is an 'offline' module, meaning it operates only on available facts. It does not need to connect to a device.
      It's a wrapper around the L(SnapshotCompare class, https://pan.dev/panos/docs/panos-upgrade-assurance/api/snapshot_compare/#class-snapshotcompare).
    - The module takes two snapshots made with M(paloaltonetworks.panos.panos_state_snapshot) module, compares them and produces a report in a form of
      a B(dict). Keys in this report match the state areas, values contain comparison details.
    - You can limit the report to the state area's you're only interested in. You can also adjust the comparison by excluding some or
      limiting to particular properties.
    - Please refer to package's documentation for L(syntax,https://pan.dev/panos/docs/panos-upgrade-assurance/configuration-details/#readiness-checks)
      and L(configuration dialect,https://pan.dev/panos/docs/panos-upgrade-assurance/dialect/).
author: "Łukasz Pawlęga (@fosix)"
version_added: '2.18.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
    - panos-upgrade-assurance can be obtained from PyPI U(https://pypi.python.org/pypi/panos-upgrade-assurance)
notes:
    - This is an offline module, no device connection is made.
    - Check mode is not supported.
options:
    left_snapshot:
        description: One of the snapshots to compare. It can be any snapshot taken in any time, but normally, in an upgrade scenario,
                     you would think about it as the pre-upgrade snapshot.
        type: dict
        required: true
    right_snapshot:
        description: One of the snapshots to compare. It can be any snapshot taken in any time, but normally, in an upgrade scenario,
                     you would think about it as the post-upgrade snapshot.
        type: dict
        required: true
    reports:
        description:
            - 'A list of Firewall state areas available in both snapshots: I(left_snapshot) and I(right_snapshot).'
            - To use the default comparison method, this is a list of strings.
              If you would like to modify the default behavior additional configuration can be specified per state area.
            - For a list of currently available state areas as well as possible ways of modifying the reports please refer to
              L(package documentation,https://pan.dev/panos/docs/panos-upgrade-assurance/configuration-details/#reports).
            - To capture the actual report use a register.
        type: list
        elements: raw
        default: ["all"]
"""

EXAMPLES = """
- name: Compare licenses in two snapshots, skip device's serial number to avoid false-positives
  panos_snapshot_report:
    left_snapshot: '{{ snap_1.response }}'
    right_snapshot: '{{ snap_2.response }}'
    reports:
      - license:
          properties:
            - '!serial'
    register: report
- name: Print the report to stdout
  ansible.builtin.debug:
    var: report.response
"""

RETURN = """
response:
    description:
        - This is a B(dict) where keys are state areas names just as you specify them in the I(reports) property.
        - Values contain a report generated for particular state area. The structure is the same for each report except for 'session_stats'.
          For details refer to L(package documentation, For a list of currently available state areas please refer to
          L(package documentation,https://pan.dev/panos/docs/panos-upgrade-assurance/configuration-details/#reports).
    type: dict
    returned: always
    sample:
        content_version:
            added:
                added_keys: []
                passed: true
            changed:
                changed_raw:
                    version:
                        left_snap: 8647-7730
                        right_snap: 8647-7729
                passed: false
            missing:
                missing_keys: []
                passed: true
            passed: false
        ip_sec_tunnels:
            added:
                added_keys: []
                passed: true
            changed:
                changed_raw:
                    ipsec_tun:
                        added:
                            added_keys: []
                            passed: true
                        changed:
                            changed_raw:
                                state:
                                    left_snap: init
                                    right_snap: running
                            passed: false
                        missing:
                            missing_keys: []
                            passed: true
                        passed: false
                passed: false
            missing:
                missing_keys: []
                passed: true
            passed: false
        license:
            added:
                added_keys: []
                passed: true
            changed:
                changed_raw: {}
                passed: true
            missing:
                missing_keys:
                    - AutoFocus Device License
                passed: false
            passed: false
        nics:
            added:
                added_keys: []
                passed: true
            changed:
                changed_raw:
                    ethernet1/1:
                        left_snap: up
                        right_snap: down
                passed: false
            missing:
                missing_keys:
                    - tunnel
                passed: false
            passed: false
"""

from ansible.module_utils.basic import AnsibleModule
import sys

PUA_AVAILABLE = True
try:
    import panos_upgrade_assurance
    from panos_upgrade_assurance.snapshot_compare import SnapshotCompare
    from panos_upgrade_assurance.exceptions import SnapshotSchemeMismatchException
except ImportError:
    PUA_AVAILABLE = False
    pass

MIN_PUA_VER = (0, 3, 0)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            left_snapshot=dict(type="dict", required=True),
            right_snapshot=dict(type="dict", required=True),
            reports=dict(type="list", default=["all"], elements="raw"),
        ),
        supports_check_mode=False,
    )

    if not PUA_AVAILABLE:
        module.fail_json(
            msg='Missing required library "panos_upgrade_assurance".', syspath=sys.path
        )

    pua_ver = tuple(int(x) for x in panos_upgrade_assurance.__version__.split("."))
    if pua_ver < MIN_PUA_VER:
        module.fail_json(
            msg="{0} version ({1}) < minimum version ({2})".format(
                "panos_upgrade_assurance",
                "{0}.{1}.{2}".format(*pua_ver),
                "{0}.{1}.{2}".format(*MIN_PUA_VER),
            )
        )

    try:
        results = SnapshotCompare(
            left_snapshot=module.params["left_snapshot"],
            right_snapshot=module.params["right_snapshot"],
        ).compare_snapshots(reports=module.params["reports"])
    except SnapshotSchemeMismatchException as exc:
        module.fail_json(msg=getattr(exc, "message", repr(exc)))

    module.exit_json(changed=False, response=results)


if __name__ == "__main__":
    main()
