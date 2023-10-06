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

DOCUMENTATION = """
---
module: panos_administrator
short_description: Manage PAN-OS administrator user accounts.
description:
    - Manages PAN-OS administrator user accounts.
author: "Garfield Lee Freeman (@shinmog)"
version_added: '1.0.0'
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
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.full_template_support
    - paloaltonetworks.panos.fragments.deprecated_commit
    - paloaltonetworks.panos.fragments.gathered_filter
options:
    admin_username:
        description:
            - Admin name.
        type: str
        default: "admin"
    authentication_profile:
        description:
            - The authentication profile.
        type: str
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
        elements: str
    vsys_read_only:
        description:
            - This is for multi-vsys physical firewalls only.
            - The list of vsys this read only admin should manage.
        type: list
        elements: str
    ssh_public_key:
        description:
            - Use public key authentication (ssh)
        type: str
    role_profile:
        description:
            - The role based profile.
        type: str
    admin_password:
        description:
            - New plain text password for the I(admin_username) user.
            - If this is not specified, then the password is left as-is.
            - Takes priority over I(admin_phash)
        type: str
    admin_phash:
        description:
            - New password hash for the I(admin_username) user
            - If this is not specified, then the phash is left as-is.
        type: str
    password_profile:
        description:
            - The password profile for this user.
        type: str
"""

EXAMPLES = """
# Configure user "foo"
- name: configure foo administrator
  paloaltonetworks.panos.panos_administrator:
    provider: '{{ provider }}'
    admin_username: 'foo'
    admin_password: 'secret'
    superuser: true
"""

RETURN = """
status:
    description: success status
    returned: success
    type: str
    sample: "done"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    ConnectionHelper,
    get_connection,
    to_sdk_cls,
)


class Helper(ConnectionHelper):
    def pre_state_handling(self, obj, result, module):
        Administrator = to_sdk_cls("device", "Administrator")
        PanDeviceError = to_sdk_cls("errors", "PanDeviceError")
        password = module.params["admin_password"]

        if password is not None:
            try:
                obj.password_hash = self.device.request_password_hash(password)
            except PanDeviceError as e:
                module.fail_json(msg="Failed to get phash: {0}".format(e))
        elif obj.password_hash is None:
            o2 = Administrator(obj.name)
            o2.parent = obj.parent
            try:
                o2.refresh()
            except PanDeviceError:
                pass
            else:
                obj.password_hash = o2.password_hash

    def post_state_handling(self, obj, result, module):
        PanDeviceError = to_sdk_cls("errors", "PanDeviceError")
        password = module.params["admin_password"]
        phash = module.params["admin_phash"]

        if self.device._api_username == obj.name:
            if password is not None:
                self.device._api_key = None
                self.device._api_password = password
                try:
                    self.device.refresh_system_info()
                except PanDeviceError as e:
                    module.fail_json(msg="Failed API key refresh: {0}".format(e))
            elif phash is not None:
                msg = [
                    "Password of current user was changed by hash.",
                    "Exiting module as API key cannot be determined.",
                ]
                module.warn(" ".join(msg))
                module.exit_json(**result)


def main():
    helper = get_connection(
        helper_cls=Helper,
        template=True,
        template_stack=True,
        template_is_optional=True,
        with_network_resource_module_state=True,
        with_commit=True,
        with_classic_provider_spec=True,
        with_gathered_filter=True,
        min_pandevice_version=(0, 8, 0),
        sdk_cls=("device", "Administrator"),
        sdk_params=dict(
            admin_username=dict(default="admin", sdk_param="name"),
            authentication_profile=dict(),
            web_client_cert_only=dict(type="bool"),
            superuser=dict(type="bool"),
            superuser_read_only=dict(type="bool"),
            panorama_admin=dict(type="bool"),
            device_admin=dict(type="bool"),
            device_admin_read_only=dict(type="bool"),
            vsys=dict(type="list", elements="str"),
            vsys_read_only=dict(type="list", elements="str"),
            ssh_public_key=dict(),
            role_profile=dict(),
            admin_phash=dict(no_log=True, sdk_param="password_hash"),
            password_profile=dict(no_log=False),
        ),
        extra_params=dict(
            admin_password=dict(no_log=True),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    helper.process(module)


if __name__ == "__main__":
    main()
