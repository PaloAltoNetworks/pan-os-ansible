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
module: panos_tunnel
short_description: configure tunnel interfaces
description:
    - Configure tunnel interfaces on PanOS
author: "Joshua Colson (@freakinhippie)"
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPi U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPi U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is supported.
    - Panorama is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.state
    - paloaltonetworks.panos.fragments.vsys_import
    - paloaltonetworks.panos.fragments.template_only
    - paloaltonetworks.panos.fragments.deprecated_commit
options:
    if_name:
        description:
            - Name of the interface to configure.
        type: str
        required: true
    ip:
        description:
            - List of static IP addresses.
        type: list
        elements: str
    ipv6_enabled:
        description:
            - Enable IPv6.
        type: bool
    management_profile:
        description:
            - Interface management profile name; it must already exist.
        type: str
    mtu:
        description:
            - MTU for tunnel interface.
        type: int
    netflow_profile:
        description:
            - Netflow profile for tunnel interface.
        type: str
    comment:
        description:
            - Interface comment.
        type: str
    zone_name:
        description:
            - Name of the zone for the interface. If the zone does not exist it is created but
              if the zone exists and it is not of the correct mode the operation will fail.
        type: str
    vr_name:
        description:
            - Name of the virtual router; it must already exist.
        type: str
    vsys_dg:
        description:
            - B(Deprecated)
            - Use I(vsys) to specify the vsys instead.
            - HORIZONTALLINE
            - Name of the vsys (if firewall) or device group (if panorama) to put this object.
        type: str
'''

EXAMPLES = '''
# Create tunnel.1
- name: create tunnel.1
  panos_tunnel:
    provider: '{{ provider }}'
    if_name: "tunnel.1"
    ip: ["10.1.1.1/32"]

# Update tunnel comment.
- name: update tunnel.1 comment
  panos_tunnel:
    provider: '{{ provider }}'
    if_name: "tunnel.1"
    ip: ["10.1.1.1/32"]
    comment: "tunnel interface"
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection, eltostr


try:
    from panos.network import TunnelInterface
    from panos.errors import PanDeviceError
except ImportError:
    try:
        from pandevice.network import TunnelInterface
        from pandevice.errors import PanDeviceError
    except ImportError:
        pass


def main():
    helper = get_connection(
        vsys_importable=True,
        template=True,
        with_classic_provider_spec=True,
        with_state=True,
        min_pandevice_version=(0, 8, 0),
        argument_spec=dict(
            if_name=dict(required=True),
            ip=dict(type='list', elements='str'),
            ipv6_enabled=dict(type='bool'),
            management_profile=dict(),
            mtu=dict(type='int'),
            netflow_profile=dict(),
            comment=dict(),
            zone_name=dict(),
            vr_name=dict(),
            commit=dict(type='bool', default=False),

            # TODO(gfreeman) - remove this in 2.12
            vsys_dg=dict(),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # Get the object params.
    spec = {
        'name': module.params['if_name'],
        'ip': module.params['ip'],
        'ipv6_enabled': module.params['ipv6_enabled'],
        'management_profile': module.params['management_profile'],
        'mtu': module.params['mtu'],
        'netflow_profile': module.params['netflow_profile'],
        'comment': module.params['comment'],
    }

    # Get other info.
    state = module.params['state']
    zone_name = module.params['zone_name']
    vr_name = module.params['vr_name']
    vsys = module.params['vsys']
    vsys_dg = module.params['vsys_dg']
    commit = module.params['commit']

    # TODO(gfreeman) - Remove vsys_dg in 2.12, as well as this code chunk.
    # In the mean time, we'll need to do this special handling.
    if vsys_dg is not None:
        module.deprecate(
            'Param "vsys_dg" is deprecated, use "vsys"',
            version='3.0.0', collection_name='paloaltonetworks.panos'
        )

        if vsys is None:
            vsys = vsys_dg
        else:
            msg = [
                'Params "vsys" and "vsys_dg" both given',
                'Specify one or the other, not both.',
            ]
            module.fail_json(msg='.  '.join(msg))
    elif vsys is None:
        # TODO(gfreeman) - v2.12, just set the default for vsys to 'vsys1'.
        vsys = 'vsys1'

    # Make sure 'vsys' is set appropriately.
    module.params['vsys'] = vsys

    # Verify libs are present, get the parent object.
    parent = helper.get_pandevice_parent(module)

    # Retrieve the current config.
    try:
        interfaces = TunnelInterface.refreshall(
            parent, add=False, matching_vsys=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    # Build the object based on the user spec.
    obj = TunnelInterface(**spec)
    parent.add(obj)

    # Which action should we take on the interface?
    changed = False
    diff = None
    reference_params = {
        'refresh': True,
        'update': not module.check_mode,
        'return_type': 'bool',
    }
    if state == 'present':
        for item in interfaces:
            if item.name != obj.name:
                continue
            diff = dict(
                before=eltostr(item)
            )
            # Interfaces have children, so don't compare them.
            if not item.equal(obj, compare_children=False):
                changed = True
                obj.extend(item.children)
                diff['after'] = eltostr(obj)
                if not module.check_mode:
                    try:
                        obj.apply()
                    except PanDeviceError as e:
                        module.fail_json(msg='Failed apply: {0}'.format(e))
            break
        else:
            changed = True
            diff = dict(
                before="",
                after=eltostr(obj)
            )
            if not module.check_mode:
                try:
                    obj.create()
                except PanDeviceError as e:
                    module.fail_json(msg='Failed create: {0}'.format(e))

        # Set references.
        try:
            changed |= obj.set_vsys(vsys, **reference_params)
            changed |= obj.set_zone(zone_name, mode='layer3', **reference_params)
            changed |= obj.set_virtual_router(vr_name, **reference_params)
        except PanDeviceError as e:
            module.fail_json(msg='Failed setref: {0}'.format(e))
    elif state == 'absent':
        # Remove references.
        try:
            changed |= obj.set_virtual_router(None, **reference_params)
            changed |= obj.set_zone(None, mode='layer3', **reference_params)
            changed |= obj.set_vsys(None, **reference_params)
        except PanDeviceError as e:
            module.fail_json(msg='Failed setref: {0}'.format(e))

        # Remove the interface.
        if obj.name in [x.name for x in interfaces]:
            changed = True
            diff = dict(
                before=eltostr(obj),
                after=""
            )
            if not module.check_mode:
                try:
                    obj.delete()
                except PanDeviceError as e:
                    module.fail_json(msg='Failed delete: {0}'.format(e))

    # Commit if we were asked to do so.
    if changed and commit:
        helper.commit(module)

    # Done!
    module.exit_json(changed=changed, diff=diff, msg='Done')


if __name__ == '__main__':
    main()
