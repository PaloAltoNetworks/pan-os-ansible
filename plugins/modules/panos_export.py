#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2020 Palo Alto Networks, Inc
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
module: panos_export
short_description: export file from PAN-OS devices
description:
    - Export files from PAN-OS device
author:
    - Michael Richardson (@mrichardson03)
version_added: '2.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
    - xmltodict
notes:
    - Checkmode is NOT supported.
    - Panorama is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
options:
    category:
        description:
            - Element type to export.
        type: str
        choices:
            - application-block-page
            - application-pcap
            - captive-portal-text
            - certificate
            - configuration
            - credential-block-page
            - credential-coach-text
            - data-filter-block-page
            - device-state
            - dlp-pcap
            - file-block-continue-page
            - file-block-page
            - filter-pcap
            - global-protect-portal-custom-help-page
            - global-protect-portal-custom-home-page
            - global-protect-portal-custom-login-page
            - global-protect-portal-custom-welcome-page
            - mfa-login-page
            - safe-search-block-page
            - ssl-cert-status-page
            - ssl-optout-text
            - stats-dump
            - tech-support
            - threat-pcap
            - url-block-page
            - url-coach-text
            - virus-block-page
        default: 'configuration'
    certificate_name:
        description:
            - Name of the certificate to export.
        type: str
    certificate_format:
        description:
            - Format for the certificate.
        type: str
        choices:
            - pem
            - pkcs10
            - pkcs12
    certificate_include_keys:
        description:
            - Whether to include the private key in the export.
        type: bool
        default: False
    certificate_passphrase:
        description:
            - Passphrase used to encrypt the certificate and/or private key.
        type: str
    filename:
        description:
            - Local path to output file (if any).
        type: str
    application_pcap_name:
        description:
            - When I(category=application-pcap), this can be a blank string, a packet capture directory name,
              or a packet capture name.  If the value is either blank or a directory name, a list of directories or
              packet capture files will be returned.  If the value is a packet capture file name, the file will be
              written to I(filename).
        type: str
    dlp_pcap_name:
        description:
            - When I(category=dlp-pcap), this value can be a blank string, or a packet capture name.  If the value
              is blank, a list of packet capture files will be returned.  If the value is a packet capture file name,
              the file will be written to I(filename).
        type: str
    dlp_password:
        description:
            - Password used to decrypt DLP packet capture.
        type: str
    filter_pcap_name:
        description:
            - When I(category=filter-pcap), this value can be a blank string, or a packet capture name.  If the
              value is blank, a list of packet capture files will be returned.  If the value is a packet capture file
              name, the file will be written to I(filename).
        type: str
    threat_pcap_id:
        description:
            - When I(category=threat-pcap), this value is a unique identifier for the packet capture, and can be
              obtained from the 'pcap_id' field in the THREAT log.
        type: str
    threat_pcap_search_time:
        description:
            - When I(category=threat-pcap), this value is is used to narrow the search for the 'pcap_id' and is
              used to set a time window in the range -5 minutes to +2 hours of the time specified. The search time is
              typically set to the **receive_time** field in the THREAT log. The PAN-OS log time string format is used,
              for example '2015/01/20 10:51:09'.  If the value is not specified, it will be set to the threat epoch time
              which is part of the 'pcap_id'.
        type: str
    threat_pcap_serial:
        description:
            - When I(category=threat-pcap), this value is required when exporting from Panorama and is used to
              specify the device to fetch the packet capture from.
        type: str
    timeout:
        description:
            - When category is set to 'tech-support', 'stats-dump', or 'device-state', the operating can take a while
              to complete.  This is the maximum amount of time to wait, in seconds.
        type: int
        default: 600
'''

EXAMPLES = '''
- name: Export configuration
  panos_export:
    provider: '{{ provider }}'
    category: 'configuration'
    filename: 'running-config.xml'

- name: Export application block page
  panos_export:
    provider: '{{ provider }}'
    category: 'application-block-page'
    filename: 'application-block-page.html'

- name: Export tech support (module will wait until file is ready)
  panos_export:
    provider: '{{ provider }}'
    category: 'tech-support'
    filename: 'tech-support.tgz'

- name: Export threat packet capture
  panos_export:
    provider: '{{ provider }}'
    category: 'threat-pcap'
    threat_pcap_id: '1206450340254187521'
    threat_pcap_search_time: '2020/07/20 18:20:19'
    filename: 'threat.pcap'
'''

RETURN = '''
stdout:
    description: If the output gives a directory listing, give the listing as JSON formatted string
    returned: success
    type: str
    sample: "{'dir-listing': {'file': ['/capture-rx', '/capture-tx', '/capture-fw']}}"
stdout_xml:
    description: If the output gives a directory listing, give the listing as XML formatted string
    returned: success
    type: str
    sample: "<dir-listing><file>/capture-rx</file><file>/capture-tx</file><file>/capture-fw</file></dir-listing>"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from panos.panorama import Panorama
    from panos.errors import PanDeviceError
except ImportError:
    try:
        from pandevice.panorama import Panorama
        from pandevice.errors import PanDeviceError
    except ImportError:
        pass

try:
    import pan.xapi
    import xmltodict
    HAS_LIB = True
except ImportError:
    HAS_LIB = False

import json
import time
import os
import xml.etree.ElementTree as ET


def export_text(module, xapi, category, filename):
    xapi.export(category=category)

    f = None

    try:
        f = open(filename, 'w')
    except IOError as msg:
        module.fail_json(msg=msg)
    else:
        if category == 'configuration':
            f.write(xapi.xml_root())
        elif category in HTML_EXPORTS:
            f.write(xapi.text_document)

        f.close()


def export_binary(module, xapi, filename):
    f = None

    try:
        f = open(filename, 'wb')
    except IOError as msg:
        module.fail_json(msg=msg)
    else:
        content = xapi.export_result['content']

        if content is not None:
            f.write(content)

        f.close()


def export_async(module, xapi, category, filename, interval=60, timeout=600):

    # Submit job, get resulting job id
    xapi.export(category=category)
    job_result = ET.fromstring(xapi.xml_root())

    job_id = None
    if job_result.find('.//job') is not None:
        job_id = job_result.find('.//job').text

    end_time = time.time() + timeout

    while True:
        # Check job progress
        xapi.export(category=category, extra_qs={'action': 'status', 'job-id': job_id})
        poll_result = ET.fromstring(xapi.xml_root())

        status = poll_result.find('.//status')
        if status.text == "FIN":
            break

        if time.time() > end_time:
            module.fail_json(msg='Timeout')

        time.sleep(interval)

    # Get completed job
    xapi.export(category=category, extra_qs={'action': 'get', 'job-id': job_id})
    export_binary(module, xapi, filename)


HTML_EXPORTS = [
    'application-block-page',
    'captive-portal-text',
    'credential-block-page',
    'credential-coach-text',
    'data-filter-block-page',
    'file-block-continue-page',
    'file-block-page',
    'global-protect-portal-custom-help-page',
    'global-protect-portal-custom-home-page',
    'global-protect-portal-custom-login-page',
    'global-protect-portal-custom-welcome-page',
    'mfa-login-page',
    'safe-search-block-page',
    'ssl-cert-status-page',
    'ssl-optout-text',
    'url-block-page',
    'url-coach-text',
    'virus-block-page'
]

FILE_EXPORTS = [
    'device-state', 'tech-support', 'stats-dump'
]


def main():
    helper = get_connection(
        with_classic_provider_spec=True,
        argument_spec=dict(
            category=dict(default='configuration', choices=sorted(
                ['configuration', 'certificate'] + HTML_EXPORTS + FILE_EXPORTS +
                ['application-pcap', 'filter-pcap', 'dlp-pcap', 'threat-pcap']),
            ),
            filename=dict(type='str'),

            certificate_name=dict(type='str'),
            certificate_format=dict(type='str', choices=['pem', 'pkcs10', 'pkcs12']),
            certificate_include_keys=dict(type='bool', default=False),
            certificate_passphrase=dict(type='str', no_log=True),

            application_pcap_name=dict(type='str'),

            dlp_pcap_name=dict(type='str'),
            dlp_password=dict(type='str', no_log=True),

            filter_pcap_name=dict(type='str'),

            threat_pcap_id=dict(type='str'),
            threat_pcap_search_time=dict(type='str'),
            threat_pcap_serial=dict(type='str'),

            timeout=dict(type='int', default=600),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=False,
        required_one_of=helper.required_one_of,
        required_together=[
            ['certificate_name', 'certificate_format'],
            ['dlp_pcap_name', 'dlp_password'],
        ]
    )

    if not HAS_LIB:
        module.fail_json(msg='pan-python, pandevice, and xmltodict are required for this module')

    category = module.params['category']
    filename = module.params['filename']
    timeout = module.params['timeout']

    parent = helper.get_pandevice_parent(module)
    xapi = parent.xapi

    if category in (['configuration'] + HTML_EXPORTS):
        if filename is None:
            module.fail_json(msg='filename is required for export')

        export_text(module, xapi, category, filename)

    elif category in FILE_EXPORTS:
        if filename is None:
            module.fail_json(msg='filename is required for export')

        if category == 'stats-dump' and isinstance(parent, Panorama):
            module.fail_json(msg='stats-dump is not supported on Panorama')

        export_async(module, xapi, category, filename, timeout=timeout)

    elif category == 'certificate':
        if filename is None:
            module.fail_json(msg='filename is required for export')

        cert_name = module.params['certificate_name']
        cert_format = module.params['certificate_format']
        cert_include_keys = 'yes' if module.params['certificate_include_keys'] else 'no'
        cert_passphrase = module.params['certificate_passphrase']

        params = {
            'certificate-name': cert_name,
            'format': cert_format,
            'include-keys': cert_include_keys
        }

        if cert_include_keys == 'yes' and cert_passphrase is None:
            module.exit_json(msg='certificate_passphrase is required when certificate_include_keys is yes')

        if cert_passphrase is not None:
            params['passphrase'] = cert_passphrase

        xapi.export(category='certificate', extra_qs=params)
        export_binary(module, xapi, filename)

    elif category == 'application-pcap':

        # When exporting an application pcap, from_name can be:
        #   - nothing, which gets you a list of directories
        #   - a directory name, which gets you a list of pcaps in that directory
        #   - a filename, which gets you the pcap file
        from_name = module.params['application_pcap_name']
        xapi.export(category='application-pcap', from_name=from_name)

        if from_name is None or '.pcap' not in from_name:
            xml_result = xapi.xml_result()

            obj_dict = xmltodict.parse(xml_result)
            json_output = json.dumps(obj_dict)

            module.exit_json(changed=False, stdout=json_output, stdout_xml=xml_result)
        else:
            if filename is None:
                module.fail_json(msg='filename is required for export')

            export_binary(module, xapi, filename)

    elif category == 'filter-pcap':

        # When exporting a filter pcap, from_name can be:
        #   - nothing, which gets you a list of files
        #   - a filename, which gets you the pcap file
        from_name = module.params['filter_pcap_name']
        xapi.export(category='filter-pcap', from_name=from_name)

        if from_name is None:
            xml_result = xapi.xml_result()

            obj_dict = xmltodict.parse(xml_result)
            json_output = json.dumps(obj_dict)

            module.exit_json(changed=False, stdout=json_output, stdout_xml=xml_result)
        else:
            if filename is None:
                module.fail_json(msg='filename is required for export')

            export_binary(module, xapi, filename)

    elif category == 'dlp-pcap':
        from_name = module.params['dlp_pcap_name']
        dlp_password = module.params['dlp_password']
        xapi.export(category='dlp-pcap', from_name=from_name, extra_qs={'dlp-password': dlp_password})

        # When exporting a dlp pcap, from_name can be:
        #   - nothing, which gets you a list of files
        #   - a filename, which gets you the pcap file
        if from_name is None:
            xml_result = xapi.xml_result()

            obj_dict = xmltodict.parse(xml_result)
            json_output = json.dumps(obj_dict)

            module.exit_json(changed=False, stdout=json_output, stdout_xml=xml_result)
        else:
            if filename is None:
                module.fail_json(msg='filename is required for export')

            export_binary(module, xapi, filename)

    elif category == 'threat-pcap':
        if filename is None:
            module.fail_json(msg='filename is required for export')

        pcap_id = module.params['threat_pcap_id']
        search_time = module.params['threat_pcap_search_time']

        # pan-python says serial number is not required on certain PAN-OS releases (not required on 9.0 or 10.0)
        serial = module.params['threat_pcap_serial']

        if isinstance(parent, Panorama) and serial is None:
            module.fail_json(msg='threat_pcap_serial is required when connecting to Panorama')

        xapi.export(category='threat-pcap', pcapid=pcap_id, search_time=search_time, serialno=serial)
        export_binary(module, xapi, filename)

    module.exit_json(changed=False)


if __name__ == '__main__':
    main()
