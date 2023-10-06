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

DOCUMENTATION = """
---
module: panos_import
short_description: import file on PAN-OS devices
description:
    - Import file on PAN-OS device
author:
    - 'Luigi Mori (@jtschichold)'
    - 'Ivan Bojer (@ivanbojer)'
    - 'Michael Richardson (@mrichardson03)'
version_added: '1.0.0'
requirements:
    - pan-python
    - requests
    - requests_toolbelt
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.full_template_support
notes:
    - I(category=certificate) is used for importing a certificate on its own from a file.
    - I(category=keypair) is used for importing a certificate and private key from a single file.
options:
    category:
        description:
            - Category of file to import.
        type: str
        choices:
            - anti-virus
            - application-block-page
            - captive-portal-text
            - certificate
            - configuration
            - content
            - credential-block-page
            - credential-coach-text
            - custom-logo
            - data-filter-block-page
            - device-state
            - file-block-continue-page
            - file-block-page
            - global-protect-client
            - global-protect-clientless-vpn
            - global-protect-portal-custom-help-page
            - global-protect-portal-custom-home-page
            - global-protect-portal-custom-login-page
            - global-protect-portal-custom-welcome-page
            - high-availability-key
            - idp-metadata
            - keypair
            - license
            - logdb
            - mfa-login-page
            - pandb-url-database
            - plugin
            - safe-search-block-page
            - saml-auth-internal-error-page
            - signed-url-database
            - software
            - ssl-cert-status-page
            - ssl-optout-text
            - url-block-page
            - url-coach-text
            - url-database
            - virus-block-page
            - wildfire
        default: software
    certificate_name:
        description:
            - When I(category=certificate), this is the name of the certificate object.
            - When I(category=keypair), the key pair will be associated with this certificate object.
        type: str
    format:
        description:
            - Format of the imported certifcate.
        type: str
        choices:
            - pem
            - pkcs12
    passphrase:
        description:
            - Passphrase used to decrypt the certificate and/or private key.
        type: str
    block_private_key_export:
        description:
            - When I(category=keypair), controls if the private key is allowed to be exported from PAN-OS in future.
            - If this parameter is left undefined, the effective value with be no.
        type: bool
    custom_logo_location:
        description:
            - When I(category=custom-logo), import this logo file here.
        type: str
        choices:
            - login-screen
            - main-ui
            - pdf-report-footer
            - pdf-report-header
    filename:
        description:
            - Location of the file to import into device.
        type: str
        aliases:
            - file
        required: false
    profile_name:
        description:
            - When I(category=idp-metadata), the name of the SAML profile to create.
        type: str
    url:
        description:
            - URL of the file that will be imported to device.
        type: str
        required: false
"""

EXAMPLES = """
- name: Import software image into PAN-OS
  paloaltonetworks.panos.panos_import:
    provider: '{{ provider }}'
    category: software
    file: /tmp/paloaltonetworks.panos.panos_vm-10.0.1

- name: Import certificate
  paloaltonetworks.panos.panos_import:
    provider: '{{ device }}'
    category: 'certificate'
    certificate_name: 'ISRG Root X1'
    format: 'pem'
    filename: '/tmp/isrgrootx1.pem'

- name: Import content
  paloaltonetworks.panos.panos_import:
    provider: '{{ device }}'
    category: 'content'
    filename: '/tmp/panupv2-all-contents-8322-6317'

- name: Import named configuration snapshot
  paloaltonetworks.panos.panos_import:
    provider: '{{ device }}'
    category: 'configuration'
    filename: '/tmp/config.xml'

- name: Import application block page
  paloaltonetworks.panos.panos_import:
    provider: '{{ device }}'
    category: 'application-block-page'
    filename: '/tmp/application-block-page.html'

- name: Import custom logo
  paloaltonetworks.panos.panos_import:
    provider: '{{ device }}'
    category: 'custom-logo'
    custom_logo_location: 'login-screen'
    filename: '/tmp/logo.jpg'

- name: Import SAML metadata profile
  paloaltonetworks.panos.panos_import:
    provider: '{{ device }}'
    category: 'idp-metadata'
    filename: '/tmp/saml_metadata.xml'
    profile_name: 'saml-profile'

- name: Import SAML metadata profile to template
  paloaltonetworks.panos.panos_import:
    provider: '{{ device }}'
    category: 'idp-metadata'
    filename: '/tmp/saml_metadata.xml'
    profile_name: 'saml-profile'
    template: firewall-template
"""

RETURN = """
# Default return values
"""

import os
import os.path
import shutil
import tempfile
import xml.etree

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    get_connection,
)

try:
    import requests

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def import_file(module, xapi, filename, params):
    params.update({"type": "import", "key": xapi.api_key})

    url = "https://{0}:{1}/api".format(xapi.hostname, xapi.port)
    files = {"file": open(filename, "rb")}

    r = requests.post(url, params=params, files=files, verify=False)
    response = xml.etree.ElementTree.fromstring(r.content)

    if r.status_code != 200 or response.attrib["status"] == "error":
        module.fail_json(msg=r.content)


def download_file(url):
    r = requests.get(url, stream=True)

    with tempfile.NamedTemporaryFile(prefix="ai", delete=False) as fo:
        shutil.copyfileobj(r.raw, fo)

    return fo.name


def delete_file(path):
    os.remove(path)


def main():
    helper = get_connection(
        template=True,
        template_stack=True,
        template_is_optional=True,
        with_classic_provider_spec=True,
        argument_spec=dict(
            category=dict(
                type="str",
                choices=[
                    "anti-virus",
                    "application-block-page",
                    "captive-portal-text",
                    "certificate",
                    "configuration",
                    "content",
                    "credential-block-page",
                    "credential-coach-text",
                    "custom-logo",
                    "data-filter-block-page",
                    "device-state",
                    "file-block-continue-page",
                    "file-block-page",
                    "global-protect-client",
                    "global-protect-clientless-vpn",
                    "global-protect-portal-custom-help-page",
                    "global-protect-portal-custom-home-page",
                    "global-protect-portal-custom-login-page",
                    "global-protect-portal-custom-welcome-page",
                    "high-availability-key",
                    "idp-metadata",
                    "keypair",
                    "license",
                    "logdb",
                    "mfa-login-page",
                    "pandb-url-database",
                    "plugin",
                    "safe-search-block-page",
                    "saml-auth-internal-error-page",
                    "signed-url-database",
                    "software",
                    "ssl-cert-status-page",
                    "ssl-optout-text",
                    "url-block-page",
                    "url-coach-text",
                    "url-database",
                    "virus-block-page",
                    "wildfire",
                ],
                default="software",
            ),
            certificate_name=dict(type="str"),
            format=dict(type="str", choices=["pem", "pkcs12"]),
            passphrase=dict(type="str", no_log=True),
            block_private_key_export=dict(type="bool"),
            custom_logo_location=dict(
                type="str",
                choices=[
                    "login-screen",
                    "main-ui",
                    "pdf-report-footer",
                    "pdf-report-header",
                ],
            ),
            profile_name=dict(type="str"),
            filename=dict(type="str", aliases=["file"]),
            url=dict(),
        ),
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    if not HAS_LIB:
        module.fail_json(
            msg="requests and requests_toolbelt are required for this module"
        )

    category = module.params["category"]
    filename = module.params["filename"]

    url = module.params["url"]

    # get_pandevice_parent will validate templates. The returned value, if a template, is not useable.
    parent = helper.get_pandevice_parent(module)
    xapi = (
        helper.device.xapi
    )  # This is why we get the xapi info from helper.device instead

    changed = False

    # we can get file from URL or local storage
    if url is not None:
        filename = download_file(url)

    params = {"category": module.params["category"]}

    if category == "certificate" or category == "keypair":
        params["certificate-name"] = module.params["certificate_name"]
        params["format"] = module.params["format"]
        params["passphrase"] = module.params["passphrase"]
        src = "block_private_key_export"
        dst = "block-private-key"
        if module.params[src] is None:
            params[dst] = None
        elif module.params[src]:
            params[dst] = "yes"
        else:
            params[dst] = "no"

    elif category == "custom-logo":
        params["where"] = module.params["custom_logo_location"]

    elif category == "idp-metadata":
        params["profile-name"] = module.params["profile_name"]

    if module.params["template_stack"] is not None:
        params["target-tpl"] = module.params["template_stack"]

    elif module.params["template"] is not None:
        params["target-tpl"] = module.params["template"]

    try:
        if not module.check_mode:
            import_file(module, xapi, filename, params)
        changed = True

    except Exception as e:
        module.fail_json(msg="Failed: {0}".format(e))

    # If the file was downloaded from a URL, clean up.
    if url is not None:
        delete_file(filename)

    module.exit_json(changed=changed, filename=filename, msg="okey dokey")


if __name__ == "__main__":
    main()
