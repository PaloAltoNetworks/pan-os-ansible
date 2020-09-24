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
module: panos_lic
short_description: apply authcode to a device/instance
description:
    - Apply an authcode to a device.
    - The authcode should have been previously registered on the Palo Alto Networks support portal.
    - The device should have Internet access.
author: "Luigi Mori (@jtschichold), Ivan Bojer (@ivanbojer)"
version_added: '1.0.0'
requirements:
    - pan-python
    - pandevice
notes:
    - Panorama is supported
    - Checkmode is not supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
options:
    auth_code:
        description:
            - authcode to be applied.
            - If this is not given, then "request license fetch" is performed instead.
        type: str
    force:
        description:
            - Whether to apply authcode even if device is already licensed / has a serial number.
        type: bool
        default: False
'''

EXAMPLES = '''
- name: Activate my authcode
  panos_lic:
    provider: '{{ provider }}'
    auth_code: "IBADCODE"
  register: result

- debug:
    msg: 'Serial number is {{ result.serialnumber }}'
'''

RETURN = '''
serialnumber:
    description: PAN-OS serial number when this module began execution.
    returned: success
    type: str
    sample: 007200004214
licenses:
    description: List of PAN-OS licenses (as dicts) as a result of this module's execution.
    type: list
    returned: when not using auth_code
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
        min_pandevice_version=(0, 9, 1),
        argument_spec=dict(
            auth_code=dict(no_log=True, ),
            force=dict(type='bool', default=False)
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=False,
        required_one_of=helper.required_one_of,
    )

    parent = helper.get_pandevice_parent(module)

    auth_code = module.params['auth_code']
    changed = False
    licenses = []
    if parent.serial != 'unknown' and not module.params['force']:
        try:
            licenses = parent.request_license_info()
        except PanDeviceError as e:
            module.fail_json(msg='Failed request license info: {0}'.format(e))
    else:
        changed = True
        if auth_code is None:
            try:
                licenses = parent.fetch_licenses_from_license_server()
            except PanDeviceError as e:
                module.fail_json(msg='Failed license fetch: {0}'.format(e))
        else:
            try:
                parent.activate_feature_using_authorization_code(auth_code)
            except PanDeviceError as e:
                module.fail_json(msg='Failed authcode apply: {0}'.format(e))

    # datetime.date objects can't be jsonify'ed, so do that manually.
    ans = []
    date_format = '%b %d, %Y'
    for x in licenses:
        ans.append({
            'feature': x[0],
            'description': x[1],
            'serial': x[2],
            'issued': x[3].strftime(date_format) if hasattr(x[3], 'strftime') else x[3],
            'expires': x[4].strftime(date_format) if hasattr(x[4], 'strftime') else x[4],
            'expired': x[5],
            'authcode': x[6],
        })

    module.exit_json(changed=changed, msg='done', licenses=ans, serialnumber=parent.serial)


if __name__ == '__main__':
    main()
