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

DOCUMENTATION = r"""
---
module: panos_commit_firewall
short_description: Commit the firewall's candidate configuration.
description:
    - Module that will commit the candidate configuration of a PAN-OS firewall.
    - The new configuration will become active immediately.
author:
    - Robert Hagen (@stealthllama)
version_added: '2.0.0'
requirements:
    - pan-os-python
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
        elements: str
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
"""

EXAMPLES = r"""
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
"""

RETURN = r"""
jobid:
  description: The ID of the PAN-OS commit job.
  type: int
  returned: always
  sample: 49152
details:
  description: Commit job completion messages.
  type: str
  returned: on success
  sample: Configuration committed successfully
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    get_connection,
)

try:
    from panos.firewall import FirewallCommit
except ImportError:
    pass


def main():
    # Instantiate the connection helper
    helper = get_connection(
        min_pandevice_version=(1, 0, 0),
        min_panos_version=(8, 0, 0),
        argument_spec=dict(
            description=dict(type="str"),
            admins=dict(type="list", elements="str"),
            exclude_device_and_network=dict(type="bool", default=False),
            exclude_shared_objects=dict(type="bool", default=False),
            exclude_policy_and_objects=dict(type="bool", default=False),
            force=dict(type="bool", default=False),
            sync=dict(type="bool", default=True),
        ),
    )

    # Initialize the Ansible module
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=False,
        required_one_of=helper.required_one_of,
    )

    # Verify libs are present, get the parent object.
    parent = helper.get_pandevice_parent(module)

    # Construct the commit command
    cmd = FirewallCommit(
        description=module.params["description"],
        admins=module.params["admins"],
        exclude_device_and_network=module.params["exclude_device_and_network"],
        exclude_shared_objects=module.params["exclude_shared_objects"],
        exclude_policy_and_objects=module.params["exclude_policy_and_objects"],
        force=module.params["force"],
    )

    # Execute the commit
    commit_results = dict(changed=False, jobid=0)
    # commit_results = {}
    sync = module.params["sync"]
    result = parent.commit(cmd=cmd, sync=sync)

    # Exit with status
    if result is None:
        # No commit was needed
        pass
    elif not sync:
        # When sync is False only jobid is returned
        commit_results["jobid"] = int(result)
    elif not result["success"]:
        # The commit failed
        module.fail_json(msg=" | ".join(result["messages"]))
    else:
        # The commit succeeded
        commit_results["changed"] = True
        commit_results["jobid"] = result["jobid"]
        commit_results["details"] = result["messages"]

    module.exit_json(**commit_results)


if __name__ == "__main__":
    main()
