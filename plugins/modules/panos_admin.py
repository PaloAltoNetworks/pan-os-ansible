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

ANSIBLE_METADATA = {'status': ['deprecated'],
                    'supported_by': 'community',
                    'version': '1.0'}

DOCUMENTATION = '''
---
module: panos_admin
short_description: Add or modify PAN-OS user accounts password.
description:
    - PanOS module that allows changes to the user account passwords by doing
      API calls to the Firewall using pan-api as the protocol.
author: "Luigi Mori (@jtschichold), Ivan Bojer (@ivanbojer)"
version_added: "2.3"
deprecated:
    alternative: Use M(panos_administrator) instead.
    removed_in: '2.12'
    why: This module is a subset of M(panos_administrator)'s functionality.
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
notes:
    - Checkmode is not supported.
options:
    ip_address:
        description:
            - IP address (or hostname) of PAN-OS device being configured.
        required: true
    port:
        description:
            - Port used to connect to the PAN-OS device being configured.
        required: false
        default: 443
    username:
        description:
            - Username credentials to use for auth unless I(api_key) is set.
        default: "admin"
    password:
        description:
            - Password credentials to use for auth unless I(api_key) is set.
        required: true
    api_key:
        description:
            - API key that can be used instead of I(username)/I(password) credentials.
    admin_username:
        description:
            - Username that needs password change.
        required: false
        default: "admin"
    admin_password:
        description:
            - New password for I(admin_username) user
        required: true
    role:
        description:
            - role for admin user
        required: false
        default: null
    commit:
        description:
            - Commit configuration if changed.
        default: true
'''

EXAMPLES = '''
# Set the password of user admin to "badpassword"
# Doesn't commit the candidate config
  - name: set admin password
    panos_admin:
      ip_address: "192.168.1.1"
      password: "admin"
      admin_username: admin
      admin_password: "badpassword"
      commit: False
'''

RETURN = '''
status:
    description: success status
    returned: success
    type: string
    sample: "okey dokey"
'''
from ansible.module_utils.basic import AnsibleModule

try:
    import pan.xapi
    HAS_LIB = True
except ImportError:
    HAS_LIB = False

_ADMIN_XPATH = "/config/mgt-config/users/entry[@name='%s']"


def admin_exists(xapi, admin_username):
    xapi.get(_ADMIN_XPATH % admin_username)
    e = xapi.element_root.find('.//entry')
    return e


def admin_set(xapi, module, admin_username, admin_password, role):
    if admin_password is not None:
        xapi.op(cmd='request password-hash password "%s"' % admin_password,
                cmd_xml=True)
        r = xapi.element_root
        phash = r.find('.//phash').text
    if role is not None:
        rbval = "yes"
        if role != "superuser" and role != 'superreader':
            rbval = ""

    ea = admin_exists(xapi, admin_username)
    if ea is not None:
        # user exists
        changed = False

        if role is not None:
            rb = ea.find('.//role-based')
            if rb is not None:
                if rb[0].tag != role:
                    changed = True
                    xpath = _ADMIN_XPATH % admin_username
                    xpath += '/permissions/role-based/%s' % rb[0].tag
                    xapi.delete(xpath=xpath)

                    xpath = _ADMIN_XPATH % admin_username
                    xpath += '/permissions/role-based'
                    xapi.set(xpath=xpath,
                             element='<%s>%s</%s>' % (role, rbval, role))

        if admin_password is not None:
            xapi.edit(xpath=_ADMIN_XPATH % admin_username + '/phash',
                      element='<phash>%s</phash>' % phash)
            changed = True

        return changed

    # setup the non encrypted part of the monitor
    exml = []

    exml.append('<phash>%s</phash>' % phash)
    exml.append('<permissions><role-based><%s>%s</%s>'
                '</role-based></permissions>' % (role, rbval, role))

    exml = ''.join(exml)
    # module.fail_json(msg=exml)

    xapi.set(xpath=_ADMIN_XPATH % admin_username, element=exml)

    return True


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        port=dict(default=443),
        password=dict(no_log=True),
        username=dict(default='admin'),
        api_key=dict(no_log=True),
        admin_username=dict(default='admin'),
        admin_password=dict(no_log=True, required=True),
        role=dict(),
        commit=dict(type='bool', default=True)
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False,
                           required_one_of=[['api_key', 'password']])

    module.deprecate('This module is deprecated; use panos_administrator', '2.12')

    if not HAS_LIB:
        module.fail_json(msg='Missing required libraries.')

    ip_address = module.params["ip_address"]
    port = module.params['port']
    password = module.params["password"]
    username = module.params['username']
    api_key = module.params['api_key']
    admin_username = module.params['admin_username']
    admin_password = module.params['admin_password']
    role = module.params['role']
    commit = module.params['commit']

    xapi = pan.xapi.PanXapi(
        hostname=ip_address,
        api_username=username,
        api_password=password,
        api_key=api_key,
        port=port
    )

    changed = admin_set(xapi, module, admin_username, admin_password, role)

    if changed and commit:
        xapi.commit(cmd="<commit></commit>", sync=True, interval=1)

    module.exit_json(changed=changed, msg="okey dokey")


if __name__ == '__main__':
    main()
