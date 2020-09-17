#!/usr/bin/python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2020,  Palo Alto Networks, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: panos_commit_push
short_description: Commit Panorama's candidate configuration.
description:
    - Module that will push the running Panorama configuration to managed devices.
    - The new configuration will become active immediately.
author:
    - Robert Hagen (@stealthllama)
version_added: "2.9"
requirements:
    - pan-os-python
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.provider
options:
    style:
        description:
            - The type of configuration element to push.
        type: str
        choices:
            - device group
            - template
            - template stack
            - log collector group
            - wildfire appliance
            - wildfire cluster
        required: True
    name:
        description:
            - The name of the configuration element to push.
        type: str
    description:
        description:
            - A description of the commit.
        type: str
    include_template:
        description:
            - Include device group reference templates.
        type: bool
        default: False
    force_template_values:
        description:
            - Force template values to override local settings.
        type: bool
        default: False
    devices:
        description:
            - Push the configuration to specific device serial numbers.
        type: list
    sync:
        description:
            - Wait for the commit to complete.
        type: bool
        default: True
'''

EXAMPLES = '''
- name: push device group configs
  panos_commit_push:
    provider: '{{ credentials }}'
    style: 'device group'
    name: 'Internet Edge Firewalls'
    description: 'Update ECMP routing'

- name: push template configs and force values
  panos_commit_push:
    provider: '{{ credentials }}'
    style: 'template'
    name: 'APAC Regional Template'
    force_template_values: True

- name: push log collector group configs
  panos_commit_push:
    provider: '{{ credentials }}'
    style: 'log collector group'
    name: 'LatAm Collector Group'

- name: push to multiple devices
  panos_commit_push:
    provider: '{{ credentials }}'
    style: 'device group'
    name: 'Partner DMZ Firewalls'
    devices:
      - 0001234567890
      - 0987654321000
      - 1001001F0F000

- name: push to multiple device groups
  panos_commit_push:
    provider: '{{ credentials }}'
    style: 'device group'
    name: '{{ item }}'
    sync: False
  loop:
    - Production Firewalls
    - Staging Firewalls
    - Development Firewalls
'''

RETURN = '''
jobid:
  description: The ID of the PAN-OS commit job.
  type: int
  returned: always
  sample: 49152
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from panos.panorama import PanoramaCommitAll
except ImportError:
    pass


def main():
    helper = get_connection(
        min_pandevice_version=(1, 0, 0),
        min_panos_version=(8, 0, 0),
        argument_spec=dict(
            style=dict(choices=[
                'device group',
                'template',
                'template stack',
                'log collector group',
                'wildfire appliance',
                'wildfire cluster'
            ]
            ),
            name=dict(type='str'),
            description=dict(type='str'),
            include_template=dict(type='bool'),
            force_template_values=dict(type='bool'),
            devices=dict(type='list'),
            sync=dict(type='bool', default=True)
        )
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=False,
        required_one_of=helper.required_one_of
    )

    # Verify libs are present, get the parent object.
    parent = helper.get_pandevice_parent(module)

    # Construct the commit command
    cmd = PanoramaCommitAll(
        style=module.params['style'],
        name=module.params['name'],
        description=module.params['description'],
        include_template=module.params['include_template'],
        force_template_values=module.params['force_template_values'],
        devices=module.params['devices'],
    )

    # Execute the commit
    commit_results = {}
    sync = module.params['sync']
    result = parent.commit(cmd=cmd, sync=sync, sync_all=sync)

    # Exit with status
    if not sync:
        # When sync is False only jobid is returned
        commit_results['jobid'] = int(result)
    elif not result['success']:
        # The commit failed
        module.fail_json(msg=' | '.join(result['messages']))
    else:
        # The commit succeeded
        commit_results['changed'] = True
        commit_results['jobid'] = result['jobid']

    module.exit_json(**commit_results)


if __name__ == '__main__':
    main()
