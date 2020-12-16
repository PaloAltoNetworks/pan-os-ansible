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
module: panos_loadcfg
short_description: load configuration on PAN-OS device
description:
    - Load configuration on PAN-OS device
author:
    - Luigi Mori (@jtschichold)
    - Ivan Bojer (@ivanbojer)
    - Patrik Malinen (@pmalinen)
version_added: '1.0.0'
requirements:
    - pan-python
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
options:
    file:
        description:
            - configuration file to load
        type: str
        required: false
    commit:
        description:
            - commit if changed
        type: bool
        required: false
        default: false
'''

EXAMPLES = '''
# Import and load config file from URL
  - name: import configuration
    panos_import:
      provider: '{{ device }}'
      url: "{{ ConfigURL }}"
      category: "configuration"
    register: result
  - name: load configuration
    panos_loadcfg:
      provider: '{{ device }}'
      file: "{{ result.filename }}"
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    import pan.xapi
    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def load_cfgfile(xapi, module, file_):
    # load configuration file
    cmd = '<load><config><from>%s</from></config></load>' %\
          file_

    xapi.op(cmd=cmd)

    return True


def main():
    helper = get_connection(
        with_classic_provider_spec=True,
        argument_spec=dict(
            file=dict(),
            commit=dict(type='bool', default=False)
        )
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of
    )
    if not HAS_LIB:
        module.fail_json(msg='pan-python is required for this module')

    commit = module.params['commit']
    file_ = module.params['file']

    parent = helper.get_pandevice_parent(module)
    xapi = parent.xapi

    changed = False

    try:
        if not module.check_mode:
            load_cfgfile(xapi, module, file_)
        changed = True

    except Exception as e:
        module.fail_json(msg='Failed: {0}'.format(e))

    if commit and changed:
        helper.commit(module)

    module.exit_json(changed=changed, msg="okey dokey")


if __name__ == '__main__':
    main()
