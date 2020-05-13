#!/usr/bin/env python
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

DOCUMENTATION = '''
---
module: panos_check
short_description: check if PAN-OS device is ready for configuration
description:
    - Check if PAN-OS device is ready.
    - Supports config ready (no pending jobs), ha ready, and autocommit done
    - The check could be done once or multiple times until the device is ready.
author:
    - Luigi Mori (@jtschichold)
    - Ivan Bojer (@ivanbojer)
    - Garfield Lee Freeman (@shinmog)
version_added: "2.3"
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
    wait_for:
        description:
            - Type of check to perform
        type: str
        choices: [ jobs, autocommit, ha ]
        default: jobs
'''

EXAMPLES = '''
# Single check.
- name: check if ready
  panos_check:
    provider: '{{ provider }}'
    timeout: 0

# Wait 2 minutes, then check every 5 seconds for 10 minutes.
- name: wait for reboot
  panos_check:
    provider: '{{ provider }}'
    initial_delay: 120
    interval: 5
    timeout: 600

# Wait for autocommit (job ID 1) to complete
- name: check if ready
  panos_check:
    provider: '{{ provider }}'
    wait_for: autocommit
    interval: 30
    timeout: 300
'''

RETURN = '''
# Default return values
'''

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

import time
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def check_jobs(ans):
    jobs = ans.findall('.//job')
    for j in jobs:
        status = j.find('.//status')
        if status is None or status.text != 'FIN':
            return False

    return True


def check_ha(ha_status):
    local_status = ha_status.find('.//local-info/state')

    if local_status is not None and ('active' in local_status.text or 'passive' in local_status.text):
        return True

    return False


def check_autocommit(job):
    status = job.find('.//status')
    if status is None or status.text != 'FIN':
        return False

    return True


def main():
    helper = get_connection(
        with_classic_provider_spec=True,
        argument_spec=dict(
            initial_delay=dict(default=0, type='int'),
            timeout=dict(default=60, type='int'),
            wait_for=dict(type='str', default='jobs',
                          choices=['jobs', 'autocommit', 'ha']),
            interval=dict(default=0, type='int')
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=False,
        required_one_of=helper.required_one_of,
    )

    func_mapping = {
        'jobs': {
            'cmd': '<show><jobs><all></all></jobs></show>',
            'func': check_jobs
        },
        'autocommit': {
            'cmd': '<show><jobs><id>1</id></jobs></show>',
            'func': check_autocommit
        },
        'ha': {
            'cmd': '<show><high-availability><state></state></high-availability></show>',
            'func': check_ha
        }
    }

    cmd = func_mapping[module.params['wait_for']]['cmd']
    func = func_mapping[module.params['wait_for']]['func']

    # Optional delay before performing readiness checks.
    if module.params['initial_delay']:
        time.sleep(module.params['initial_delay'])

    timeout = module.params['timeout']
    interval = module.params['interval']
    end_time = time.time() + timeout

    parent = helper.get_pandevice_parent(module, timeout)

    while True:
        try:
            ans = parent.op(cmd=cmd, cmd_xml=False)
        except PanDeviceError:
            pass
        else:
            if func(ans):
                break

        if time.time() > end_time:
            module.fail_json(msg='Timeout')

        time.sleep(interval)

    module.exit_json(changed=True, msg="done")


if __name__ == '__main__':
    main()