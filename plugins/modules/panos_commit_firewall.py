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

DOCUMENTATION = r'''
---
module: panos_commit_firewall
short_description: Commit the firewall's candidate configuration.
description:
    - Module that will commit the candidate configuration of a PAN-OS firewall.
    - The new configuration will become active immediately.
author:
    - Robert Hagen (@stealthllama)
version_added: "2.10"
requirements:
    - pan-os-python
    - dateutils
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.provider
options:
    description:
        description:
            - A description of the commit.
        type: str
    admins:
        description:
            - Commit only the changes made by specified list of administrators.
        type: list
    exclude_device_and_network:
        description:
            - Exclude network and device configuration changes.
        type: bool
        default: False
    exclude_shared_objects:
        description:
            - Exclude shared object configuration changes.
        type: bool
        default: False
    exclude_policy_and_objects:
        description:
            - Exclude policy and object configuration changes.
        type: bool
        default: False
    force:
        description:
            - Force the commit.
        type: bool
        default: False
    sync:
        description:
            - Wait for the commit to complete.
        type: bool
        default: True
'''

EXAMPLES = r'''
- name: commit candidate configs on firewall
  panos_commit_firewall:
    provider: '{{ credentials }}'

- name: commit changes by specified admins on firewall
  panos_commit_firewall:
    provider: '{{ credentials }}'
    admins: ['netops','secops','cloudops']
    description: 'Saturday change window'

- name: commit only policy and object changes on firewall
  panos_commit_firewall:
    provider: '{{ credentials }}'
    exclude_device_and_network: True
'''

RETURN = r'''
jobid:
  description: The ID of the PAN-OS commit job.
  type: int
  returned: always
  sample: 49152
starttime:
  description: The time the commit job started.
  type: str
  returned: on success
  sample: 2020-09-06T17:56:20
endtime:
  description: The time the commit job ended.
  type: str
  returned: on success
  sample: 2020-09-06T17:56:35
runtime:
  description: The elapsed time (in seconds) of the commit job.
  type: int
  returned: on success
  sample: 15
details:
  description: Commit job completion messages.
  type: str
  returned: on success
  sample: Configuration committed successfully
warning:
  description: Commit job warnings.
  type: list
  returned: on success
  sample: ["","","","","","","","","","",""]
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from panos.firewall import FirewallCommit
    from dateutils import parser
except ImportError:
    pass


def main():
    # Instantiate the connection helper
    helper = get_connection(
        min_pandevice_version=(1, 0, 0),
        min_panos_version=(8, 0, 0),
        argument_spec=dict(
            description=dict(type='str'),
            admins=dict(type='list'),
            exclude_device_and_network=dict(type='bool'),
            exclude_shared_objects=dict(type='bool'),
            exclude_policy_and_objects=dict(type='bool'),
            force=dict(type='bool'),
            sync=dict(type='bool', default=True)
        )
    )

    # Initialize the Ansible module
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=False,
        required_one_of=helper.required_one_of
    )

    # Verify libs are present, get the parent object.
    parent = helper.get_pandevice_parent(module)

    # Construct the commit command
    cmd = FirewallCommit(
        description=module.params['description'],
        admins=module.params['admins'],
        exclude_device_and_network=module.params['exclude_device_and_network'],
        exclude_shared_objects=module.params['exclude_shared_objects'],
        exclude_policy_and_objects=module.params['exclude_policy_and_objects'],
        force=module.params['force']
    )

    # Execute the commit
    # commit_results = dict(changed=False, jobid=0)
    commit_results = {}
    sync = module.params['sync']
    result = parent.commit(cmd=cmd, sync=sync)

    # Exit with status
    if result is None:
        # No commit was needed
        pass
    elif not sync:
        # When sync is False only jobid is returned
        module_results['jobid'] = int(result)
    elif not result['success']:
        # The commit failed
        module.fail_json(msg=' | '.join(result["messages"]))
    else:
        # The commit succeeded
        commit_results['changed'] = True
        commit_results['jobid'] = result['jobid']
        commit_results['starttime'] = parser.parse(result['starttime'])
        commit_results['endtime'] = parser.parse(result['endtime'])
        commit_results['runtime'] = (commit_results['endtime'] - commit_results['starttime']).seconds
        commit_results['warnings'] = result['warnings']['line']
        commit_results['details'] = result['messages']

    module.exit_json(**commit_results)


if __name__ == '__main__':
    main()
