#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2018 Palo Alto Networks, Inc
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
module: panos_software
short_description: Manage PAN-OS software versions.
description:
    - Install specific release of PAN-OS.
author: "Michael Richardson (@mrichardson03)"
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
options:
    version:
        description:
            - Desired PAN-OS release for target device.
        type: str
        required: true
    sync_to_peer:
        description:
            - If device is a member of a HA pair, perform actions on the peer
              device as well.  Only used when downloading software -
              installation must be performed on both devices.
        type: bool
        default: False
    download:
        description:
            - Download PAN-OS version to the device.
        type: bool
        default: True
    install:
        description:
            - Perform installation of the PAN-OS version on the device.
        type: bool
        default: True
    restart:
        description:
            - Restart device after installing desired version.  Use in conjunction with
              panos_check to determine when firewall is ready again.
        type: bool
        default: False
    timeout:
        description:
            - Timeout value in seconds to wait for the device operation to complete
        type: int
        default: 1200
'''

EXAMPLES = '''
- name: Install PAN-OS 8.1.6 and restart
  panos_software:
    provider: '{{ provider }}'
    version: '8.1.6'
    restart: true

- name: Download PAN-OS 9.0.0 base image only
  panos_software:
    provider: '{{ provider }}'
    version: '9.0.0'
    install: false
    restart: false

- name: Download PAN-OS 9.0.1 and sync to HA peer
  panos_software:
    provider: '{{ provider }}'
    version: '9.0.1'
    sync_to_peer: true
    install: false
    restart: false
'''

RETURN = '''
version:
    description: After performing the software install, returns the version installed on the device.
    type: str
    returned: on success
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from panos import PanOSVersion
    from panos.errors import PanDeviceError
except ImportError:
    try:
        from pandevice import PanOSVersion
        from pandevice.errors import PanDeviceError
    except ImportError:
        pass


def main():
    helper = get_connection(
        with_classic_provider_spec=True,
        argument_spec=dict(
            version=dict(type='str', required=True),
            sync_to_peer=dict(type='bool', default=False),
            download=dict(type='bool', default=True),
            install=dict(type='bool', default=True),
            restart=dict(type='bool', default=False),
            timeout=dict(type='int', default=1200)
        )
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        required_one_of=helper.required_one_of,
        supports_check_mode=True
    )

    # Verify libs are present, get parent object.
    device = helper.get_pandevice_parent(module)

    # Module params.
    version = module.params['version']
    sync_to_peer = module.params['sync_to_peer']
    download = module.params['download']
    install = module.params['install']
    restart = module.params['restart']
    timeout = module.params['timeout']

    changed = False

    try:
        device.timeout = timeout
        device.software.check()

        if PanOSVersion(version) != PanOSVersion(device.version):

            changed = True

            if not module.check_mode:
                if download:
                    cmd_string = 'request system software info'

                    try:
                        response = device.op(cmd=cmd_string)
                        downloaded = response.findtext('./result/sw-updates/versions/entry/version[.="{0}"]/../'
                                                       'downloaded'.format(version))

                        if downloaded != 'yes':
                            device.software.download(version, sync_to_peer=sync_to_peer, sync=True)
                        else:
                            changed = False

                    except PanDeviceError as e:
                        module.fail_json(msg='Failed "{0}": {1}'.format(cmd_string, e))

                if install:
                    device.software.install(version, sync=True)

                if restart:
                    device.restart()

    except PanDeviceError as e:
        module.fail_json(msg=e.message)

    module.exit_json(changed=changed, version=version)


if __name__ == '__main__':
    main()
