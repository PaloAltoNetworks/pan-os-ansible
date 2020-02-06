#!/usr/bin/env python
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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: panos_registered_ip_facts
short_description: Retrieve facts about registered IPs on PAN-OS devices.
description:
    - Retrieves tag information about registered IPs on PAN-OS devices.
author: "Michael Richardson (@mrichardson03)"
version_added: "2.7"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is not supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.vsys
options:
    tags:
        description:
            - List of tags to retrieve facts for.  If not specified, retrieve all tags.
    ips:
        description:
            - List of IP addresses to retrieve facts for.  If not specified, retrieve all addresses.
'''

EXAMPLES = '''
- name: Get facts for all registered IPs
  panos_registered_ip_facts:
    provider: '{{ provider }}'
  register: registered_ip_facts

- name: Get facts for specific tag
  panos_registered_ip_facts:
    provider: '{{ provider }}'
    tags: ['First_Tag']
  register: first_tag_registered_ip_facts

- name: Get facts for a specific IP address
  panos_registered_ip_facts:
    provider: '{{ provider }}'
    ips: ['192.168.1.1']
  register: ipaddress_registered_ip_facts
'''

RETURN = '''
results:
    description: IP addresses as keys, tags as values.
    returned: always
    type: dict
    sample: { '1.1.1.1': ['First_Tag', 'Second_Tag'] }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def main():
    helper = get_connection(
        vsys=True,
        with_classic_provider_spec=True,
        panorama_error='Panorama is not supported for this module.',
        argument_spec=dict(
            tags=dict(type='list'),
            ips=dict(type='list')
        )
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        required_one_of=helper.required_one_of
    )

    tags = module.params['tags']
    ips = module.params['ips']

    device = helper.get_pandevice_parent(module)

    try:
        registered_ips = device.userid.get_registered_ip(tags=tags, ip=ips)

    except PanDeviceError as e:
        module.fail_json(msg='Failed get_registered_ip: {0}'.format(e))

    module.exit_json(changed=False, results=registered_ips)


if __name__ == '__main__':
    main()
