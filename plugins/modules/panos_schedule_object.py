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

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
module: panos_schedule_object
short_description: Manage schedule objects on PAN-OS devices.
description:
    - Manage schedule objects on PAN-OS devices.
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
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
options:
    name:
        description:
            - Name of the object.
        type: str
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
"""

EXAMPLES = """
- name: Create schedule object
  paloaltonetworks.panos.panos_schedule_object:
    provider: '{{ provider }}'
    name: 'Monday-Work-Day'
    type: 'recurring'
    recurrence: 'weekly'
    weekly_monday_time:
      - '09:00-17:00'

- name: Create non-recurring schedule object
  paloaltonetworks.panos.panos_schedule_object:
    provider: '{{ device }}'
    name: 'Week-of-Sept-21'
    type: 'non-recurring'
    non_recurring_date_time: '2020/09/21@00:15-2020/09/25@17:00'
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
        vsys=True,
        device_group=True,
        with_classic_provider_spec=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        sdk_cls=("objects", "ScheduleObject"),
        sdk_params=dict(
            name=dict(type="str", required=True),
            disable_override=dict(type="bool"),
            type=dict(type="str", choices=["recurring", "non-recurring"]),
            non_recurring_date_time=dict(type="list", elements="str"),
            recurrence=dict(type="str", choices=["daily", "weekly"]),
            daily_time=dict(type="list", elements="str"),
            weekly_sunday_time=dict(type="list", elements="str"),
            weekly_monday_time=dict(type="list", elements="str"),
            weekly_tuesday_time=dict(type="list", elements="str"),
            weekly_wednesday_time=dict(type="list", elements="str"),
            weekly_thursday_time=dict(type="list", elements="str"),
            weekly_friday_time=dict(type="list", elements="str"),
            weekly_saturday_time=dict(type="list", elements="str"),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        required_one_of=helper.required_one_of,
        supports_check_mode=True,
    )

    helper.process(module)


if __name__ == "__main__":
    main()
