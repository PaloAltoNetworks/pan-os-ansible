#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2019 Palo Alto Networks, Inc
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
module: panos_virtual_wire
short_description: Configures Virtual Wires (vwire).
description:
    - Manage PAN-OS Virtual Wires (vwire).
author: "Patrick Avery (@unknown)"
version_added: '1.0.0'
requirements:
    - pan-python
    - pandevice
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.state
    - paloaltonetworks.panos.fragments.vsys_import
    - paloaltonetworks.panos.fragments.full_template_support
notes:
    - Checkmode is supported.
    - Panorama is supported.
options:
    name:
        description:
            -  Name of the Virtual Wire
        type: str
        required: True
    interface1:
        description:
            - First interface of Virtual Wire
        type: str
        required: True
    interface2:
        description:
            - Second interface of Virtual Wire
        type: str
        required: True
    tag:
        description:
            - Set tag that is allowed over Virtual Wire.  Currently
              pandevice only supports all (default) or 1 tag.
        type: int
    multicast:
        description:
            - Enable multicast firewalling
        type: bool
    pass_through:
        description:
            - Enable link state pass through
        type: bool
'''

EXAMPLES = '''
- name: Create Vwire
  panos_virtual_wire:
    provider: '{{ provider }}'
    name: 'vwire1'
    interface1: 'ethernet1/1'
    interface2: 'ethernet1/2'
    tag: 100
    multicast: 'true'
    pass_through: 'true'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection


try:
    from panos.network import VirtualWire
    from panos.errors import PanDeviceError
except ImportError:
    try:
        from pandevice.network import VirtualWire
        from pandevice.errors import PanDeviceError
    except ImportError:
        pass


def main():
    helper = get_connection(
        vsys_importable=True,
        template=True,
        template_stack=True,
        with_state=True,
        with_classic_provider_spec=True,
        argument_spec=dict(
            name=dict(type='str', required=True, ),
            interface1=dict(type='str', required=True),
            interface2=dict(type='str', required=True),
            tag=dict(type='int'),
            multicast=dict(type='bool'),
            pass_through=dict(type='bool'),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    parent = helper.get_pandevice_parent(module)

    spec = {
        'name': module.params['name'],
        'interface1': module.params['interface1'],
        'interface2': module.params['interface2'],
        'tag': module.params['tag'],
        'multicast': module.params['multicast'],
        'pass_through': module.params['pass_through']
    }
    obj = VirtualWire(**spec)

    try:
        listing = VirtualWire.refreshall(parent, matching_vsys=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    reference_params = {
        'refresh': True,
        'update': not module.check_mode,
        'return_type': 'bool',
    }
    parent.add(obj)

    changed = False
    if module.params['state'] == 'present':
        for vwire in listing:
            if vwire.name != obj.name:
                continue
            if not vwire.equal(obj, compare_children=False):
                changed = True
                obj.extend(vwire.children)
                if not module.check_mode:
                    try:
                        obj.apply()
                    except PanDeviceError as e:
                        module.fail_json(msg='Failed apply: {0}'.format(e))
            break
        else:
            changed = True
            if not module.check_mode:
                try:
                    obj.create()
                except PanDeviceError as e:
                    module.fail_json(msg='Failed create: {0}'.format(e))
        try:
            changed |= obj.set_vsys(module.params['vsys'], **reference_params)
        except PanDeviceError as e:
            module.fail_json(msg='Failed setref: {0}'.format(e))
    elif module.params['state'] == 'absent':
        try:
            changed |= obj.set_vsys(None, **reference_params)
        except PanDeviceError as e:
            module.fail_json(msg='Failed setref: {0}'.format(e))
        if obj.name in [x.name for x in listing]:
            changed = True
            if not module.check_mode:
                try:
                    obj.delete()
                except PanDeviceError as e:
                    module.fail_json(msg='Failed delete: {0}'.format(e))

    module.exit_json(changed=changed, msg='done')


if __name__ == '__main__':
    main()
