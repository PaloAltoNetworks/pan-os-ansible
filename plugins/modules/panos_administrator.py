#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

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

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

DOCUMENTATION = '''
---
module: panos_administrator
short_description: Manage PAN-OS administrator user accounts.
description:
    - Manages PAN-OS administrator user accounts.
author: "Garfield Lee Freeman (@shinmog)"
version_added: "2.8"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is supported.
    - Panorama is supported.
    - Because "request password-hash" does not always generate the same hash
      with the same password every time, it isn't possible to tell if the
      admin's password is correct or not.  Specifying check mode or
      I(state=present) with I(admin_password) specified will always report
      I(changed=True) in the return value.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.state
    - paloaltonetworks.panos.fragments.full_template_support
options:
    admin_username:
        description:
            - Admin name.
        default: "admin"
    authentication_profile:
        description:
            - The authentication profile.
    web_client_cert_only:
        description:
            - Use only client certificate authenciation (Web)
        type: bool
    superuser:
        description:
            - Admin type - superuser
        type: bool
    superuser_read_only:
        description:
            - Admin type - superuser, read only
        type: bool
    panorama_admin:
        description:
            - This is for Panorama only.
            - Make the user a Panorama admin only
        type: bool
    device_admin:
        description:
            - Admin type - device admin
        type: bool
    device_admin_read_only:
        description:
            - Admin type - device admin, read only
        type: bool
    vsys:
        description:
            - This is for multi-vsys physical firewalls only.
            - The list of vsys this admin should manage.
        type: list
    vsys_read_only:
        description:
            - This is for multi-vsys physical firewalls only.
            - The list of vsys this read only admin should manage.
        type: list
    ssh_public_key:
        description:
            - Use public key authentication (ssh)
    role_profile:
        description:
            - The role based profile.
    admin_password:
        description:
            - New plain text password for the I(admin_username) user.
            - If this is not specified, then the password is left as-is.
            - Takes priority over I(admin_phash)
    admin_phash:
        description:
            - New password hash for the I(admin_username) user
            - If this is not specified, then the phash is left as-is.
    password_profile:
        description:
            - The password profile for this user.
    commit:
        description:
            - Commit configuration if changed.
        default: true
        type: bool
'''

EXAMPLES = '''
# Configure user "foo"
# Doesn't commit the candidate config
  - name: configure foo administrator
    panos_administrator:
      provider: '{{ provider }}'
      admin_username: 'foo'
      admin_password: 'secret'
      superuser: true
      commit: false
'''

RETURN = '''
status:
    description: success status
    returned: success
    type: string
    sample: "done"
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection


try:
    from pandevice.device import Administrator
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def main():
    helper = get_connection(
        template=True,
        template_stack=True,
        with_state=True,
        with_classic_provider_spec=True,
        min_pandevice_version=(0, 8, 0),
        argument_spec=dict(
            admin_username=dict(default='admin'),
            authentication_profile=dict(),
            web_client_cert_only=dict(type='bool'),
            superuser=dict(type='bool'),
            superuser_read_only=dict(type='bool'),
            panorama_admin=dict(type='bool'),
            device_admin=dict(type='bool'),
            device_admin_read_only=dict(type='bool'),
            vsys=dict(type='list'),
            vsys_read_only=dict(type='list'),
            ssh_public_key=dict(),
            role_profile=dict(),
            admin_password=dict(no_log=True),
            admin_phash=dict(no_log=True),
            password_profile=dict(no_log=False),
            commit=dict(type='bool', default=True)
        ),
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # Verify imports, build pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    # Get administrator object spec.
    spec_params = [
        'authentication_profile', 'web_client_cert_only', 'superuser',
        'superuser_read_only', 'panorama_admin', 'device_admin',
        'device_admin_read_only', 'vsys', 'vsys_read_only',
        'ssh_public_key', 'role_profile', 'password_profile',
    ]
    params = dict((k, module.params[k]) for k in spec_params)
    params['name'] = module.params['admin_username']
    password = module.params['admin_password']
    phash = module.params['admin_phash']

    # Get other params.
    state = module.params['state']
    commit = module.params['commit']

    # Get the current administrators.
    try:
        admins = Administrator.refreshall(parent, add=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.foramt(e))
    obj = Administrator(**params)
    parent.add(obj)

    # Set "password_hash" by requesting a password hash.
    if password is not None:
        try:
            obj.password_hash = helper.device.request_password_hash(password)
        except PanDeviceError as e:
            module.fail_json(msg='Failed to get phash: {0}'.format(e))
    elif phash is not None:
        obj.password_hash = phash
    # Perform the requested action.
    changed = False
    if state == 'present':
        for item in admins:
            if item.name != obj.name:
                continue
            # If user did not specify a password, keep the current one.
            if obj.password_hash is None and item.password_hash:
                obj.password_hash = item.password_hash
            # Don't use .equal() here because we don't want pandevice to
            # try and do smart things with the password_hash field.
            if obj.element_str() != item.element_str():
                changed = True
                if not module.check_mode:
                    try:
                        obj.apply()
                    except PanDeviceError as e:
                        module.fail_json(msg='Failed apply: {0}'.format(e))

                    # If changing the current user's password, we have to
                    # fetch the new API key before any subsequent API commands
                    # (aka - commit) will work.
                    if (
                        helper.device._api_username == obj.name
                        and (password is not None or phash is not None)
                    ):
                        if phash is not None:
                            msg = [
                                'Password of current user was changed by hash.',
                                'Exiting module as API key cannot be determined.',
                            ]
                            module.warn(' '.join(msg))
                            module.exit_json(changed=changed)
                        helper.device._api_key = None
                        helper.device._api_password = password
                        try:
                            helper.device.xapi.api_key = helper.device.api_key
                        except PanDeviceError as e:
                            module.fail_json(msg='Failed API key refresh: {0}'.format(e))
            break
        else:
            changed = True
            if not module.check_mode:
                try:
                    obj.create()
                except PanDeviceError as e:
                    module.fail_json(msg='Failed create: {0}'.format(e))
    elif state == 'absent':
        if obj.name in [x.name for x in admins]:
            changed = True
            if not module.check_mode:
                try:
                    obj.delete()
                except PanDeviceError as e:
                    module.fail_json(msg='Failed delete: {0}'.format(e))

    # Commit if appropriate.
    if changed and commit:
        helper.commit(module)

    # Done.
    module.exit_json(changed=changed, msg='done')


if __name__ == '__main__':
    main()
