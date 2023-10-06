#!/usr/bin/python

#  Copyright 2021 Palo Alto Networks, Inc
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
module: panos_dynamic_updates
short_description: Install dynamic updates on PAN-OS devices.
description:
    - Installs the latest content update on PAN-OS devices.
author: "Michael Richardson (@mrichardson03)"
version_added: '2.6.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pan-os-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-os-python)
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.provider
options:
    update_type:
        description:
            - Type of dynamic update to install.
        type: str
        default: content
        choices: ['content']
    sync_to_peer:
        description:
            - If device is a member of a HA pair, install this update on the
              peer device as well.
        type: bool
        default: False
"""

EXAMPLES = """
- name: Update content to latest version
  paloaltonetworks.panos.panos_dynamic_updates:
    provider: '{{ provider }}'
"""

RETURN = """
content:
    description: Content version installed
    returned: success
    type: str
    sample: "8372-6534"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    get_connection,
)

try:
    from panos import PanOSVersion
    from panos.errors import PanDeviceError
except ImportError:
    pass


def needs_download(device, version):
    device.content.info()

    return not device.content.versions[str(version)]["downloaded"]


def needs_install(device, version):
    device.content.info()

    return not device.content.versions[str(version)]["current"]


def main():
    helper = get_connection(
        with_classic_provider_spec=False,
        argument_spec=dict(
            update_type=dict(type="str", default="content", choices=["content"]),
            sync_to_peer=dict(type="bool", default=False),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        required_one_of=helper.required_one_of,
        supports_check_mode=True,
    )

    # Verify libs are present, get parent object.
    device = helper.get_pandevice_parent(module)

    update_type = module.params["update_type"]
    sync_to_peer = module.params["sync_to_peer"]

    changed = False

    try:
        device.content.check()
        versions = map(PanOSVersion, device.content.versions.keys())
        latest = max(versions)

        if needs_download(device, latest):
            if not module.check_mode:
                device.content.download(sync_to_peer=sync_to_peer, sync=True)
            changed = True

        if needs_install(device, latest):
            if not module.check_mode:
                device.content.install(sync_to_peer=sync_to_peer, sync=True)
            changed = True

    except PanDeviceError as e:
        module.fail_json(msg=e.message)

    module.exit_json(changed=changed, content=str(latest))


if __name__ == "__main__":
    main()
