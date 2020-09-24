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
module: panos_http_profile_param
short_description: Manage HTTP params for a HTTP profile.
description:
    - Manages HTTP params for a HTTP profile.
author: "Garfield Lee Freeman (@shinmog)"
version_added: '1.0.0'
requirements:
    - pan-python
    - pandevice >= 0.11.1
    - PAN-OS >= 8.0
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.vsys_shared
    - paloaltonetworks.panos.fragments.device_group
    - paloaltonetworks.panos.fragments.state
options:
    http_profile:
        description:
            - Name of the http server profile.
        type: str
        required: True
    log_type:
        description:
            - The log type for this parameter.
        type: str
        choices:
            - config
            - system
            - threat
            - traffic
            - hip match
            - url
            - data
            - wildfire
            - tunnel
            - user id
            - gtp
            - auth
            - sctp
            - iptag
        required: True
    param:
        description:
            - The param name.
        type: str
        required: True
    value:
        description:
            - The value to assign the param.
        type: str
'''

EXAMPLES = '''
- name: Add a param to the config log type
  panos_http_profile_param:
    provider: '{{ provider }}'
    http_profile: 'my-profile'
    log_type: 'user id'
    param: 'serial'
    value: '$serial'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from panos.device import HttpServerProfile
    from panos.device import HttpConfigParam
    from panos.device import HttpSystemParam
    from panos.device import HttpThreatParam
    from panos.device import HttpTrafficParam
    from panos.device import HttpHipMatchParam
    from panos.device import HttpUrlParam
    from panos.device import HttpDataParam
    from panos.device import HttpWildfireParam
    from panos.device import HttpTunnelParam
    from panos.device import HttpUserIdParam
    from panos.device import HttpGtpParam
    from panos.device import HttpAuthParam
    from panos.device import HttpSctpParam
    from panos.device import HttpIpTagParam
    from panos.errors import PanDeviceError
except ImportError:
    try:
        from pandevice.device import HttpServerProfile
        from pandevice.device import HttpConfigParam
        from pandevice.device import HttpSystemParam
        from pandevice.device import HttpThreatParam
        from pandevice.device import HttpTrafficParam
        from pandevice.device import HttpHipMatchParam
        from pandevice.device import HttpUrlParam
        from pandevice.device import HttpDataParam
        from pandevice.device import HttpWildfireParam
        from pandevice.device import HttpTunnelParam
        from pandevice.device import HttpUserIdParam
        from pandevice.device import HttpGtpParam
        from pandevice.device import HttpAuthParam
        from pandevice.device import HttpSctpParam
        from pandevice.device import HttpIpTagParam
        from pandevice.errors import PanDeviceError
    except ImportError:
        pass


def main():
    helper = get_connection(
        vsys_shared=True,
        device_group=True,
        with_state=True,
        with_classic_provider_spec=True,
        min_pandevice_version=(0, 11, 1),
        min_panos_version=(8, 0, 0),
        argument_spec=dict(
            http_profile=dict(required=True),
            log_type=dict(required=True, choices=[
                'config', 'system', 'threat', 'traffic', 'hip match', 'url',
                'data', 'wildfire', 'tunnel', 'user id', 'gtp', 'auth',
                'sctp', 'iptag']
            ),
            param=dict(required=True),
            value=dict(),
        ),
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # Verify imports, build pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    sp = HttpServerProfile(module.params['http_profile'])
    parent.add(sp)
    try:
        sp.refresh()
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    cls_map = {
        'config': HttpConfigParam,
        'system': HttpSystemParam,
        'threat': HttpThreatParam,
        'traffic': HttpTrafficParam,
        'hip match': HttpHipMatchParam,
        'url': HttpUrlParam,
        'data': HttpDataParam,
        'wildfire': HttpWildfireParam,
        'tunnel': HttpTunnelParam,
        'user id': HttpUserIdParam,
        'gtp': HttpGtpParam,
        'auth': HttpAuthParam,
        'sctp': HttpSctpParam,
        'iptag': HttpIpTagParam,
    }

    cls = cls_map[module.params['log_type']]

    listing = sp.findall(cls)

    spec = {
        'name': module.params['param'],
        'value': module.params['value'],
    }
    obj = cls(**spec)
    sp.add(obj)

    changed, diff = helper.apply_state(obj, listing, module)
    module.exit_json(changed=changed, diff=diff, msg='Done')


if __name__ == '__main__':
    main()
