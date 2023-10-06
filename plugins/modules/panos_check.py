#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2016 Palo Alto Networks, Inc
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
module: panos_check
short_description: Checks is a PAN-OS device is ready for configuration.
description:
    - Checks to see if the autocommit job has succeeded on a PAN-OS device.
author:
    - Luigi Mori (@jtschichold)
    - Ivan Bojer (@ivanbojer)
    - Garfield Lee Freeman (@shinmog)
    - Michael Richardson (@mrichardson03)
version_added: '1.0.0'
requirements:
    - pan-python
    - pandevice
notes:
    - Panorama is supported.
    - Checkmode is not supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
options:
    initial_delay:
        description:
            - Length of time (in seconds) to wait before doing any readiness checks.
        default: 0
        type: int
    timeout:
        description:
            - Length of time (in seconds) to wait for jobs to finish.
        default: 60
        type: int
    interval:
        description:
            - Length of time (in seconds) to wait between checks.
        default: 0
        type: int
"""

EXAMPLES = """
# Single check.
- name: check if ready
  paloaltonetworks.panos.panos_check:
    provider: '{{ provider }}'
    timeout: 0

# Wait 2 minutes, then check every 5 seconds for 10 minutes.
- name: wait for reboot
  paloaltonetworks.panos.panos_check:
    provider: '{{ provider }}'
    initial_delay: 120
    interval: 5
    timeout: 600
"""

RETURN = """
# Default return values
"""


import time

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    get_connection,
)

try:
    from panos.errors import PanDeviceError
except ImportError:
    try:
        from pandevice.errors import PanDeviceError
    except ImportError:
        pass


def check_jobs(jobs):
    if len(jobs) == 0:
        return False

    for j in jobs:
        job_type = j.findtext(".//type")
        job_result = j.findtext(".//result")

        if job_type is None or job_result is None:
            return False

        if job_type == "AutoCom" and job_result == "OK":
            return True
        elif job_type == "AutoCom":
            return False

    # If we get to this point, the autocommit job is no longer in the job
    # history and it is assumed the device is ready.
    return True


def main():
    helper = get_connection(
        with_classic_provider_spec=True,
        argument_spec=dict(
            initial_delay=dict(default=0, type="int"),
            timeout=dict(default=60, type="int"),
            interval=dict(default=0, type="int"),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=False,
        required_one_of=helper.required_one_of,
    )

    # Optional delay before performing readiness checks.
    if module.params["initial_delay"]:
        time.sleep(module.params["initial_delay"])

    timeout = module.params["timeout"]
    interval = module.params["interval"]
    end_time = time.time() + timeout

    parent = helper.get_pandevice_parent(module, timeout)

    while True:
        try:
            ans = parent.op(cmd="show jobs all")
        except PanDeviceError:
            pass
        else:
            jobs = ans.findall(".//job")
            if check_jobs(jobs):
                break

        if time.time() > end_time:
            module.fail_json(msg="Timeout reached.")

        time.sleep(interval)

    module.exit_json(changed=True, msg="Device is ready.")


if __name__ == "__main__":
    main()
