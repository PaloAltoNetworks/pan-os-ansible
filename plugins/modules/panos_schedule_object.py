#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2020 Palo Alto Networks, Inc
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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: panos_schedule_object
short_description: Create schedule objects on PAN-OS devices.
description:
    - Create schedule objects on PAN-OS devices.
author: "Michael Richardson (@mrichardson03)"
version_added: '2.1.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.vsys
    - paloaltonetworks.panos.fragments.device_group
    - paloaltonetworks.panos.fragments.state
options:
    name:
        description:
            - Name of the object.
        type: str
        required: true
    disable_override:
        description:
            - If the override is disabled
        type: bool
    type:
        description:
            - Type of schedule
        type: str
        choices:
            - recurring
            - non-recurring
    non_recurring_date_time:
        description:
            - Date and time range string (e.x. '2019/11/01@00:15-2019/11/28@00:30') for a non-recurring schedule
        type: list
        elements: str
    recurrence:
        description:
            - Recurrence schedule
        type: str
        choices:
            - daily
            - weekly
    daily_time:
        description:
            - Time range (e.x. '17:00-19:00') for a daily recurring schedule
        type: list
        elements: str
    weekly_sunday_time:
        description:
            - Time range (e.x. '17:00-19:00') for a weekly recurring schedule (Sunday)
        type: list
        elements: str
    weekly_monday_time:
        description:
            - Time range (e.x. '17:00-19:00') for a weekly recurring schedule (Monday)
        type: list
        elements: str
    weekly_tuesday_time:
        description:
            - Time range (e.x. '17:00-19:00') for a weekly recurring schedule (Tuesday)
        type: list
        elements: str
    weekly_wednesday_time:
        description:
            - Time range (e.x. '17:00-19:00') for a weekly recurring schedule (Wednesday)
        type: list
        elements: str
    weekly_thursday_time:
        description:
            - Time range (e.x. '17:00-19:00') for a weekly recurring schedule (Thursday)
        type: list
        elements: str
    weekly_friday_time:
        description:
            - Time range (e.x. '17:00-19:00') for a weekly recurring schedule (Friday)
        type: list
        elements: str
    weekly_saturday_time:
        description:
            - Time range (e.x. '17:00-19:00') for a weekly recurring schedule (Saturday)
        type: list
        elements: str
'''

EXAMPLES = '''
- name: Create schedule object
  panos_schedule_object:
    provider: '{{ provider }}'
    name: 'Monday-Work-Day'
    type: 'recurring'
    recurrence: 'weekly'
    weekly_monday_time:
      - '09:00-17:00'

- name: Create non-recurring schedule object
  panos_schedule_object:
    provider: '{{ device }}'
    name: 'Week-of-Sept-21'
    type: 'non-recurring'
    non_recurring_date_time: '2020/09/21@00:15-2020/09/25@17:00'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from panos.objects import ScheduleObject
    from panos.errors import PanDeviceError
except ImportError:
    try:
        from pandevice.objects import ScheduleObject
        from pandevice.errors import PanDeviceError
    except ImportError:
        pass


def main():
    helper = get_connection(
        vsys=True,
        device_group=True,
        with_classic_provider_spec=True,
        with_state=True,
        argument_spec=dict(
            name=dict(type='str', required=True),
            disable_override=dict(type='bool'),
            type=dict(type='str', choices=['recurring', 'non-recurring']),
            non_recurring_date_time=dict(type='list', elements='str'),
            recurrence=dict(type='str', choices=['daily', 'weekly']),
            daily_time=dict(type='list', elements='str'),
            weekly_sunday_time=dict(type='list', elements='str'),
            weekly_monday_time=dict(type='list', elements='str'),
            weekly_tuesday_time=dict(type='list', elements='str'),
            weekly_wednesday_time=dict(type='list', elements='str'),
            weekly_thursday_time=dict(type='list', elements='str'),
            weekly_friday_time=dict(type='list', elements='str'),
            weekly_saturday_time=dict(type='list', elements='str')
        )
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        required_one_of=helper.required_one_of,
        supports_check_mode=True
    )

    parent = helper.get_pandevice_parent(module)

    spec = {
        'name': module.params['name'],
        'disable_override': module.params['disable_override'],
        'type': module.params['type'],
        'non_recurring_date_time': module.params['non_recurring_date_time'],
        'recurrence': module.params['recurrence'],
        'daily_time': module.params['daily_time'],
        'weekly_sunday_time': module.params['weekly_sunday_time'],
        'weekly_monday_time': module.params['weekly_monday_time'],
        'weekly_tuesday_time': module.params['weekly_tuesday_time'],
        'weekly_wednesday_time': module.params['weekly_wednesday_time'],
        'weekly_thursday_time': module.params['weekly_thursday_time'],
        'weekly_friday_time': module.params['weekly_friday_time'],
        'weekly_saturday_time': module.params['weekly_saturday_time']
    }

    try:
        listing = ScheduleObject.refreshall(parent, add=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    obj = ScheduleObject(**spec)
    parent.add(obj)

    changed, diff = helper.apply_state(obj, listing, module)
    module.exit_json(changed=changed, diff=diff)


if __name__ == '__main__':
    main()
