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

DOCUMENTATION = """
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
    - When installing PAN-OS software, checking is performed by this module to
      ensure the upgrade/downgrade path is valid. When using this module to only
      download and not install PAN-OS software, the valid upgrade/downgrade path
      checking is bypassed (in order to allow pre-downloading of PAN-OS software
      images ahead of the installation time for multiple stage upgrades/downgrades).
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
              M(paloaltonetworks.panos.panos_check) to determine when firewall is ready
              again.
        type: bool
        default: False
    timeout:
        description:
            - Timeout value in seconds to wait for the device operation to complete
        type: int
        default: 1200
    named_config:
        description:
            - A name of a existing named config to be loaded after restart.
              If a non-existing file name is given the module will fail.
        type: str
        required: False
    perform_software_check:
        description:
            - Do a software check before doing the upgrade.
        type: bool
        default: True
"""

EXAMPLES = """
- name: Install PAN-OS 8.1.6 and restart
  paloaltonetworks.panos.panos_software:
    provider: '{{ provider }}'
    version: '8.1.6'
    restart: true

- name: Download PAN-OS 9.0.0 base image only
  paloaltonetworks.panos.panos_software:
    provider: '{{ provider }}'
    version: '9.0.0'
    install: false
    restart: false

- name: Download PAN-OS 9.0.1 and sync to HA peer
  paloaltonetworks.panos.panos_software:
    provider: '{{ provider }}'
    version: '9.0.1'
    sync_to_peer: true
    install: false
    restart: false

- name: Downgrade to 9.1.10 with named config load
  paloaltonetworks.panos.panos_software:
    provider: '{{ device }}'
    version: 9.1.10
    named_config: '9.1.10_backup_named_config.xml'
    install: true
    restart: true
"""

RETURN = """
version:
    description: After performing the software install, returns the version installed on the device.
    type: str
    returned: on success
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    get_connection,
)

try:
    from panos import PanOSVersion
    from panos.errors import PanDeviceError
except ImportError:
    try:
        from pandevice import PanOSVersion
        from pandevice.errors import PanDeviceError
    except ImportError:
        pass


def needs_download(device, version):
    device.software.info()

    return not device.software.versions[str(version)]["downloaded"]


def is_valid_sequence(current, target):
    # PAN-OS version sequence for Skip Software Version Upgrade supported from 10.1
    # It is recommended to skip at most 2 major/minor release from 10.1 and 3 major/minor release from 11.0
    version_sequence = [
        PanOSVersion("10.1"),
        PanOSVersion("10.2"),
        PanOSVersion("11.0"),
        PanOSVersion("11.1"),
        PanOSVersion("11.2"),
        PanOSVersion("12.1"),
    ]

    # Patch version change (major and minor versions match)
    if (current.major == target.major) and (current.minor == target.minor):
        return True

    # Upgrade minor version (9.0.0 -> 9.1.0)
    elif (current.major == target.major) and (current.minor + 1 == target.minor):
        return True

    # Upgrade major version (9.1.0 -> 10.0.0)
    elif (current.major + 1 == target.major) and (target.minor == 0):
        return True

    # Downgrade minor version (9.1.0 -> 9.0.0)
    elif (current.major == target.major) and (current.minor - 1 == target.minor):
        return True

    # Downgrade major version (10.0.3 -> 9.1.6)
    elif current.major - 1 == target.major:
        return True

    # Skip Software Version Upgrade version logic for >= 10.1
    elif current >= PanOSVersion("10.1.0"):
        try:
            current_index = -1
            target_index = -1

            # Find the indices of current and target versions in the sequence
            for i, version in enumerate(version_sequence):
                if current.major == version.major and current.minor == version.minor:
                    current_index = i
                if target.major == version.major and target.minor == version.minor:
                    target_index = i

            # fail if either version is not in our sequence
            if current_index == -1 or target_index == -1:
                return False

            # Calculate version distance based on the sequence
            version_distance = target_index - current_index
            abs_version_distance = abs(version_distance)

            # Downgrade path
            if version_distance < 0:
                if target < PanOSVersion("10.1.0"):
                    # downgrades supported to min 10.1 for Skip Software Version
                    return False

                # For all versions >= 10.1, allow skipping at most 3 versions in downgrade
                # (11.2 -> 10.1) or (12.1 -> 10.2)
                return (
                    abs_version_distance <= 4
                )  # Distance of 4 means skipping 3 versions

            # Upgrade path
            else:
                # For all versions >= 10.1, allow skipping at most 3 versions in upgrade
                # (10.1 -> 11.2) or (10.2 -> 12.1)
                return (
                    abs_version_distance <= 4
                )  # Distance of 4 means skipping 3 versions

        except (ValueError, TypeError):  # If there's any issue with version comparisons
            return False

    # if nothing matched so far
    return False


def main():
    helper = get_connection(
        with_classic_provider_spec=True,
        argument_spec=dict(
            version=dict(type="str", required=True),
            sync_to_peer=dict(type="bool", default=False),
            named_config=dict(type="str", required=False),
            download=dict(type="bool", default=True),
            install=dict(type="bool", default=True),
            restart=dict(type="bool", default=False),
            timeout=dict(type="int", default=1200),
            perform_software_check=dict(type="bool", default=True),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        required_one_of=helper.required_one_of,
        supports_check_mode=True,
    )

    # Verify libs are present, get parent object.
    device = helper.get_pandevice_parent(module)

    # Module params.
    target = PanOSVersion(module.params["version"])
    sync_to_peer = module.params["sync_to_peer"]
    named_config = module.params.get("named_config", None)
    download = module.params["download"]
    install = module.params["install"]
    restart = module.params["restart"]
    timeout = module.params["timeout"]

    device.refresh_version()
    current = PanOSVersion(device.version)

    changed = False

    try:
        device.timeout = timeout
        if module.params["perform_software_check"]:
            device.software.check()

        if target != current:
            if not is_valid_sequence(current, target) and install:
                module.fail_json(
                    msg="Version Sequence is invalid: {0} -> {1}".format(
                        current, target
                    )
                )

            # try to check if the config specified in the module invocation actually exists
            # in case it does not, the module will simply fail
            if named_config:
                try:
                    device.op(
                        "<show><config><saved>"
                        + named_config
                        + "</saved></config></show>",
                        xml=True,
                        cmd_xml=False,
                    )
                except PanDeviceError as e1:
                    module.fail_json(
                        msg="Error fetching specified named configuration, file {0}".format(
                            e1
                        )
                    )

            # Download new base version if needed.
            if download and (
                (current.major != target.major) or (current.minor != target.minor)
            ):
                base = PanOSVersion("{0}.{1}.0".format(target.major, target.minor))

                if needs_download(device, base) and not module.check_mode:
                    device.software.download(base, sync_to_peer, sync=True)
                    changed = True

            if download:
                if needs_download(device, target) and not module.check_mode:
                    device.software.download(
                        target, sync_to_peer=sync_to_peer, sync=True
                    )
                    changed = True

            if install:
                if not module.check_mode:
                    if named_config:
                        device.software.install(
                            version=target, load_config=named_config, sync=True
                        )
                    else:
                        device.software.install(version=target, sync=True)

                changed = True

            if restart:
                if not module.check_mode:
                    device.restart()
                changed = True

    except PanDeviceError as e:
        module.fail_json(msg=e.message)

    module.exit_json(changed=changed, version=str(target))


if __name__ == "__main__":
    main()
