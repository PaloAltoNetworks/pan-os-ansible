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
module: panos_mgtconfig
short_description: Module used to configure some of the device management.
description:
    - Configure management settings of device. Not all configuration options are configurable at this time.
author: "Luigi Mori (@jtschichold), Ivan Bojer (@ivanbojer), Patrik Malinen (@pmalinen), Francesco Vigo (@fvigo)"
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is supported.
    - Panorama is supported
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.deprecated_commit
options:
    dns_server_primary:
        description:
            - IP address of primary DNS server.
        type: str
    dns_server_secondary:
        description:
            - IP address of secondary DNS server.
        type: str
    panorama_primary:
        description:
            - IP address (or hostname) of primary Panorama server.
        type: str
    panorama_secondary:
        description:
            - IP address (or hostname) of secondary Panorama server.
        type: str
    ntp_server_primary:
        description:
            - IP address (or hostname) of primary NTP server.
        type: str
    ntp_server_secondary:
        description:
            - IP address (or hostname) of secondary NTP server.
        type: str
    timezone:
        description:
            - Device timezone.
        type: str
    login_banner:
        description:
            - Login banner text.
        type: str
    update_server:
        description:
            - IP or hostname of the update server.
        type: str
    hostname:
        description:
            - The hostname of the device.
        type: str
    domain:
        description:
            - The domain of the device
        type: str
    verify_update_server:
        description:
            - Verify the identify of the update server.
        type: bool
'''

EXAMPLES = '''
- name: set dns and panorama
  panos_mgtconfig:
    provider: '{{ provider }}'
    dns_server_primary: "1.1.1.1"
    dns_server_secondary: "1.1.1.2"
    panorama_primary: "1.1.1.3"
    panorama_secondary: "1.1.1.4"
    ntp_server_primary: "1.1.1.5"
    ntp_server_secondary: "1.1.1.6"
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from panos.errors import PanDeviceError
    from panos.device import SystemSettings
    from panos.device import NTPServerPrimary
    from panos.device import NTPServerSecondary
except ImportError:
    try:
        from pandevice.errors import PanDeviceError
        from pandevice.device import SystemSettings
        from pandevice.device import NTPServerPrimary
        from pandevice.device import NTPServerSecondary
    except ImportError:
        pass


def main():
    helper = get_connection(
        with_classic_provider_spec=True,
        argument_spec=dict(
            hostname=dict(),
            domain=dict(),
            dns_server_primary=dict(),
            dns_server_secondary=dict(),
            timezone=dict(),
            panorama_primary=dict(),
            panorama_secondary=dict(),
            login_banner=dict(),
            update_server=dict(),
            verify_update_server=dict(type='bool'),
            ntp_server_primary=dict(),
            ntp_server_secondary=dict(),
            commit=dict(type='bool', default=False),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    parent = helper.get_pandevice_parent(module)

    obj = SystemSettings()
    parent.add(obj)
    try:
        obj.refresh()
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    param_relationships = {
        'hostname': 'hostname',
        'domain': 'domain',
        'dns_server_primary': 'dns_primary',
        'dns_server_secondary': 'dns_secondary',
        'timezone': 'timezone',
        'panorama_primary': 'panorama',
        'panorama_secondary': 'panorama2',
        'login_banner': 'login_banner',
        'update_server': 'update_server',
        'verify_update_server': 'verify_update_server',
    }

    changed = False
    for ansible_param, obj_param in param_relationships.items():
        value = module.params[ansible_param]
        if value is not None and getattr(obj, obj_param) != value:
            changed = True
            setattr(obj, obj_param, value)
            if not module.check_mode:
                try:
                    obj.update(obj_param)
                except PanDeviceError as e:
                    module.fail_json(msg='Failed to update {0}: {1}'.format(
                        obj_param, e))

    ntp_relationships = {
        'ntp_server_primary': NTPServerPrimary,
        'ntp_server_secondary': NTPServerSecondary,
    }

    for ansible_param, ntp_obj_cls in ntp_relationships.items():
        value = module.params[ansible_param]
        if value is not None:
            ntp_obj = None
            # As of pandevice v0.8.0, can't use .find() here as NTP objects
            # erroneously have cls.NAME != None.
            for ntp_obj in obj.children:
                if isinstance(ntp_obj, ntp_obj_cls):
                    break
            else:
                ntp_obj = ntp_obj_cls()
                obj.add(ntp_obj)
            if ntp_obj.address != value:
                changed = True
                ntp_obj.address = value
                if not module.check_mode:
                    try:
                        ntp_obj.apply()
                    except PanDeviceError as e:
                        module.fail_json(msg='Failed to set {0}: {1}'.format(
                            ansible_param, e))

    # Optional commit.
    if changed and module.params['commit'] and not module.check_mode:
        helper.commit(module)

    module.exit_json(changed=changed, msg='done')


if __name__ == '__main__':
    main()
