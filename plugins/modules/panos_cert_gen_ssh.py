#!/usr/bin/env python
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

DOCUMENTATION = '''
---
module: panos_cert_gen_ssh
short_description: generates a self-signed certificate using SSH protocol with SSH key
description:
    - This module generates a self-signed certificate that can be used by GlobalProtect client, SSL connector, or
    - otherwise. Root certificate must be preset on the system first. This module depends on paramiko for ssh.
author: "Luigi Mori (@jtschichold), Ivan Bojer (@ivanbojer)"
version_added: "2.3"
requirements:
    - paramiko
notes:
    - Checkmode is not supported.
options:
    ip_address:
        description:
            - IP address (or hostname) of PAN-OS device being configured.
        required: true
        default: null
    key_filename:
        description:
            - Location of the filename that is used for the auth. Either I(key_filename) or I(password) is required.
        required: true
        default: null
    username:
        description:
            - User name to use for auth. Default is admin.
        required: false
        default: "admin"
    password:
        description:
            - Password credentials to use for auth. Either I(key_filename) or I(password) is required.
        required: true
        default: null
    cert_friendly_name:
        description:
            - Human friendly certificate name (not CN but just a friendly name).
        required: true
        default: null
    cert_cn:
        description:
            - Certificate CN (common name) embedded in the certificate signature.
        required: true
        default: null
    signed_by:
        description:
            - Undersigning authority (CA) that MUST already be presents on the device.
        required: true
        default: null
    rsa_nbits:
        description:
            - Number of bits used by the RSA algorithm for the certificate generation.
        required: false
        default: "2048"
'''

EXAMPLES = '''
# Generates a new self-signed certificate using ssh
- name: generate self signed certificate
  panos_cert_gen_ssh:
    ip_address: "192.168.1.1"
    username: "admin"
    password: "paloalto"
    cert_cn: "1.1.1.1"
    cert_friendly_name: "test123"
    signed_by: "root-ca"
'''

RETURN = '''
# Default return values
'''

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import get_exception
import time

try:
    import paramiko
    HAS_LIB = True
except ImportError:
    HAS_LIB = False

_PROMPTBUFF = 4096


def wait_with_timeout(module, shell, prompt, timeout=60):
    now = time.time()
    result = ""
    while True:
        if shell.recv_ready():
            result += shell.recv(_PROMPTBUFF)
            endresult = result.strip()
            if len(endresult) != 0 and endresult[-1] == prompt:
                break

        if time.time() - now > timeout:
            module.fail_json(msg="Timeout waiting for prompt")

    return result


def generate_cert(module, ip_address, username, key_filename, password,
                  cert_cn, cert_friendly_name, signed_by, rsa_nbits):
    stdout = ""

    client = paramiko.SSHClient()

    # add policy to accept all host keys, I haven't found
    # a way to retrieve the instance SSH key fingerprint from AWS
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if not key_filename:
        client.connect(ip_address, username=username, password=password)
    else:
        client.connect(ip_address, username=username, key_filename=key_filename)

    shell = client.invoke_shell()
    # wait for the shell to start
    buff = wait_with_timeout(module, shell, ">")
    stdout += buff

    # generate self-signed certificate
    if isinstance(cert_cn, list):
        cert_cn = cert_cn[0]
    cmd = ' '.join([
        'request certificate generate signed-by',
        signed_by,
        'certificate-name',
        cert_friendly_name,
        'name',
        cert_cn,
        'algorithm RSA rsa-nbits {0}\n'.format(rsa_nbits),
    ])
    shell.send(cmd)

    # wait for the shell to complete
    buff = wait_with_timeout(module, shell, ">")
    stdout += buff

    # exit
    shell.send('exit\n')

    if 'Success' not in buff:
        module.fail_json(msg="Error generating self signed certificate: " + stdout)

    client.close()
    return stdout


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        username=dict(default='admin'),
        key_filename=dict(),
        password=dict(no_log=True),
        cert_cn=dict(required=True),
        cert_friendly_name=dict(required=True),
        rsa_nbits=dict(default='2048'),
        signed_by=dict(required=True)

    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False,
                           required_one_of=[['key_filename', 'password']])
    if not HAS_LIB:
        module.fail_json(msg='paramiko is required for this module')

    ip_address = module.params["ip_address"]
    username = module.params["username"]
    key_filename = module.params["key_filename"]
    password = module.params["password"]
    cert_cn = module.params["cert_cn"]
    cert_friendly_name = module.params["cert_friendly_name"]
    signed_by = module.params["signed_by"]
    rsa_nbits = module.params["rsa_nbits"]

    try:
        generate_cert(module, ip_address, username, key_filename,
                      password, cert_cn, cert_friendly_name,
                      signed_by, rsa_nbits)
    except Exception:
        exc = get_exception()
        module.fail_json(msg=exc.message)

    module.exit_json(changed=True, msg="okey dokey")


if __name__ == '__main__':
    main()
