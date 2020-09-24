#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2017 Palo Alto Networks, Inc
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

DOCUMENTATION = '''
---
module: panos_userid
short_description: Allow for registration and de-registration of userid
description:
    - Userid allows for user to IP mapping that can be used in the policy rules.
author: "Ivan Bojer (@ivanbojer)"
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is not supported.
    - Panorama is not supported.
    - This operation is runtime and does not require explicit commit of the firewall configuration.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.state
options:
    userid:
        description:
            - User UPN
        type: str
        required: true
    register_ip:
        description:
            - IP of the user's machine that needs to be registered with userid.
        type: str
        required: true
'''

EXAMPLES = '''
- name: Register user ivanb to 10.0.1.101
  panos_userid:
    provider: '{{ provider }}'
    userid: 'ACMECORP\\ivanb'
    register_ip: '10.0.1.101'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from panos.errors import PanDeviceError
except ImportError:
    try:
        from pandevice.errors import PanDeviceError
    except ImportError:
        pass


def main():
    helper = get_connection(
        with_state=True,
        with_classic_provider_spec=True,
        panorama_error='The user-id API is not supported on Panorama',
        argument_spec=dict(
            userid=dict(required=True),
            register_ip=dict(required=True),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=False,
        required_one_of=helper.required_one_of,
    )

    parent = helper.get_pandevice_parent(module)

    func = None
    prefix = ''
    if module.params['state'] == 'present':
        func = 'login'
    else:
        func = 'logout'
        prefix = 'un'

    # Apply the state.
    try:
        getattr(parent.userid, func)(module.params['userid'], module.params['register_ip'])
    except PanDeviceError as e:
        module.fail_json(msg='Failed to {0} {1}: {2}'.format(func, module.params['userid'], e))

    module.exit_json(msg="User '{0}' successfully {1}registered".format(module.params['userid'], prefix))


if __name__ == '__main__':
    main()
