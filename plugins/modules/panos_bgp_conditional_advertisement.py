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
module: panos_bgp_conditional_advertisement
short_description: Configures a BGP conditional advertisement.
description:
    - Use BGP to publish and consume routes from disparate networks.
    - In the PAN-OS GUI, this resource cannot be created without also creating at least
      one non-exist filter and one advertise filter. The API behaves a little differently;
      you can create the conditional advertisement itself, but the API will start throwing
      errors if you try to update it and there is not at least one non-exist filter and
      one advertise filter.
    - In order for a conditional advertisement to be valid, you must specify at least one
      non-exist and one advertise filter.
    - When modifying a BGP conditional advertisement, any filters attached are left as-is,
      unless I(advertise_filter) or I(non_exist_filter) are specified.
author:
    - Joshua Colson (@freakinhippie)
    - Garfield Lee Freeman (@shinmog)
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is supported.
    - Panorama is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.full_template_support
    - paloaltonetworks.panos.fragments.state
    - paloaltonetworks.panos.fragments.deprecated_commit
options:
    vr_name:
        description:
            - Name of the virtual router; it must already exist and have BGP configured.
            - See M(panos_virtual_router).
        type: str
        default: default
    advertise_filter:
        description:
            - B(Deprecated)
            - Use M(panos_bgp_policy_filter) to define filters after creation.
            - HORIZONTALLINE
            - Advertisement filter object returned by M(panos_bgp_policy_filter).
        type: str
    non_exist_filter:
        description:
            - B(Deprecated)
            - Use M(panos_bgp_policy_filter) to define filters after creation.
            - HORIZONTALLINE
            - Non-Exist filter object returned by M(panos_bgp_policy_filter).
        type: str
    enable:
        description:
            - Enable this policy.
        type: bool
    name:
        description:
            - Name of Conditional Advertisement policy.
        type: str
        required: True
    used_by:
        description:
            - List of Peer Groups using this policy.
        type: list
        elements: str
'''

EXAMPLES = '''
- name: Create BGP Conditional Advertisement Rule
  panos_bgp_conditional_advertisement:
    provider: '{{ provider }}'
    name: 'cond-rule-01'
    enable: true
    non_exist_filter: '{{ non_exist.panos_obj }}'
    advertise_filter: '{{ advertise.panos_obj }}'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from panos.errors import PanDeviceError
    from panos.network import VirtualRouter
    from panos.network import Bgp
    from panos.network import BgpPolicyConditionalAdvertisement
except ImportError:
    try:
        from pandevice.errors import PanDeviceError
        from pandevice.network import VirtualRouter
        from pandevice.network import Bgp
        from pandevice.network import BgpPolicyConditionalAdvertisement
    except ImportError:
        pass

import pickle
from base64 import b64decode


def setup_args():
    return dict(
        commit=dict(type='bool', default=False),
        vr_name=dict(default='default'),
        non_exist_filter=dict(type='str'),
        advertise_filter=dict(type='str'),
        name=dict(type='str', required=True),
        enable=dict(type='bool'),
        used_by=dict(type='list', elements='str'),
    )


def main():
    helper = get_connection(
        template=True,
        template_stack=True,
        with_state=True,
        with_classic_provider_spec=True,
        argument_spec=setup_args(),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    parent = helper.get_pandevice_parent(module)

    vr = VirtualRouter(module.params['vr_name'])
    parent.add(vr)
    try:
        vr.refresh()
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    bgp = vr.find('', Bgp)
    if bgp is None:
        module.fail_json(msg='BGP is not configured on virtual router {0}'.format(vr.name))

    listing = bgp.findall(BgpPolicyConditionalAdvertisement)

    spec = {
        'name': module.params['name'],
        'enable': module.params['enable'],
        'used_by': module.params['used_by'],
    }
    obj = BgpPolicyConditionalAdvertisement(**spec)
    bgp.add(obj)

    # TODO(gfreeman) - Remove this in 2.12.
    for ansible_param in ('non_exist_filter', 'advertise_filter'):
        val = module.params[ansible_param]
        if val is not None:
            module.deprecate(
                'Param {0} is deprecated'.format(ansible_param),
                version='3.0.0', collection_name='paloaltonetworks.panos'
            )
            filter_obj = pickle.loads(b64decode(val))
            obj.add(filter_obj)

    changed, diff = helper.apply_state(obj, listing, module)
    if changed and module.params['commit']:
        helper.commit(module)

    module.exit_json(changed=changed, diff=diff, msg='done')


if __name__ == '__main__':
    main()
