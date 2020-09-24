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
author: "Luigi Mori (@jtschichold), Ivan Bojer (@ivanbojer)"
version_added: '1.0.0'
requirements:
    - pan-python
options:
    ip_address:
        description:
            - IP address (or hostname) of PAN-OS device
        type: str
        required: true
    password:
        description:
            - password for authentication
        type: str
        required: true
    username:
        description:
            - username for authentication
        type: str
        required: false
        default: "admin"
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
      ip_address: "192.168.1.1"
      password: "admin"
      url: "{{ConfigURL}}"
      category: "configuration"
    register: result
  - name: load configuration
    panos_loadcfg:
      ip_address: "192.168.1.1"
      password: "admin"
      file: "{{result.filename}}"
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule

try:
    import pan.xapi
    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def load_cfgfile(xapi, module, ip_address, file_):
    # load configuration file
    cmd = '<load><config><from>%s</from></config></load>' %\
          file_

    xapi.op(cmd=cmd)

    return True


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(required=True, no_log=True),
        username=dict(default='admin'),
        file=dict(),
        commit=dict(type='bool', default=False)
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if not HAS_LIB:
        module.fail_json(msg='pan-python is required for this module')

    ip_address = module.params["ip_address"]
    password = module.params["password"]
    username = module.params['username']
    file_ = module.params['file']
    commit = module.params['commit']

    xapi = pan.xapi.PanXapi(
        hostname=ip_address,
        api_username=username,
        api_password=password
    )

    changed = load_cfgfile(xapi, module, ip_address, file_)
    if changed and commit:
        xapi.commit(cmd="<commit></commit>", sync=True, interval=1)

    module.exit_json(changed=changed, msg="okey dokey")


if __name__ == '__main__':
    main()
