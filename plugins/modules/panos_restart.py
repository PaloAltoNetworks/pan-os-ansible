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

DOCUMENTATION = '''
---
module: panos_restart
short_description: Restart a device
description:
    - Restart a PAN-OS device.
author:
    - Luigi Mori (@jtschichold)
    - Ivan Bojer (@ivanbojer)
    - Garfield Lee Freeman (@shinmog)
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is not supported.
    - Panorama is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
'''

EXAMPLES = '''
- name: Restart PAN-OS
  panos_restart:
    provider: '{{ provider }}'
'''

RETURN = '''
# Standard return values.
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
        with_classic_provider_spec=True,
        argument_spec=dict(),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=False,
        required_one_of=helper.required_one_of,
    )

    parent = helper.get_pandevice_parent(module)

    try:
        parent.restart()
    except PanDeviceError as e:
        module.fail_json(msg='Failed to restart: {0}'.format(e))

    module.exit_json(changed=True, msg="done")


if __name__ == '__main__':
    main()
