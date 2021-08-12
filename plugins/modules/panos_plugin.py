#!/usr/bin/python

# Copyright 2020 Palo Alto Networks, Inc
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


from __future__ import absolute_import, division, print_function
import xmltodict

__metaclass__ = type

DOCUMENTATION = """
---
module: panos_plugin
short_description: 'Install/Uninstall/Upgrade/Downgrade Plugins on PanOS Devices.'
description:
    - This module allows the user to manage lifecycle of plugins on PanOS Devices.
author:
    - 'Hardik Shah(@hsshah20)'
version_added: '2.8.0'
requirements: []
notes:
    - This module only supports the httpapi connection plugin.
    - Check mode is supported.
    - Panorama is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.state
options:
    plugin_name:
        description:
            - 'Name of Plugin (for example: vm_series, aws, kubernetes)'
        type: str
        required: true
    plugin_version:
        description:
            - 'Plugin Version (for example: 1.0.0, 2.1.0)'
        type: str
        required: true
"""

EXAMPLES = """
- name: Install VM Series Plugin
panos_plugin:
  plugin_name: 'vm_series'
  plugin_version: '2.1.1'
  state: present

- name: Uninstall AWS Plugin
panos_plugin:
  plugin_name: 'aws'
  plugin_version: '3.0.0'
  state: absent
"""

RETURN = """
changed:
    description: A boolean value indicating if the task had to make changes.
    returned: always
    type: bool
msg:
    description: A string with an error message, if any.
    returned: failure, always
    type: str
diff:
    description:
        - Information about the differences between the previous and current
          state.
        - Contains 'download_status', 'install_status', 'uninstall' keys.
    returned: success, when needed
    type: dict
    elements: str
"""

from ansible.module_utils.connection import ConnectionError
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    PanOSAnsibleModule,
)

def check_plugins(connection):
    cmd = '<request><plugins><check/></plugins></request>'
    connection.op(cmd)

def get_installed_plugins(connection):
    cmd = '<show><plugins><installed/></plugins></show>'
    response = connection.op(cmd)
    xml_plugins_list = xmltodict.parse(response)['response']['result']['list']
    installed_plugins = set()
    if xml_plugins_list:
        entries = xml_plugins_list['entry']
        if not isinstance(entries, list):
            entries = [entries]
        for plugin in entries:
            installed_plugins.add(plugin['version'])
    return installed_plugins

def download_plugin(connection, plugin):
    cmd = f'<request><plugins><download><file>{plugin}</file></download></plugins></request>'
    connection.op(cmd, poll=True)

def install_plugin(connection, plugin):
    cmd = f'<request><plugins><install>{plugin}</install></plugins></request>'
    connection.op(cmd, poll=True)
    connection.commit(force=True)

def uninstall_plugin(connection, plugin_name):
    cmd = f'<request><plugins><uninstall>{plugin_name}</uninstall></plugins></request>'
    connection.op(cmd)

def main():
    module = PanOSAnsibleModule(
        argument_spec=dict(
            plugin_name=dict(required=True),
            plugin_version=dict(required=True)
        ),
        supports_check_mode=True,
        with_state=True,
    )

    plugin_name = module.params["plugin_name"]
    plugin_version = module.params["plugin_version"]
    state = module.params["state"]
    plugin = f'{plugin_name}-{plugin_version}'
    try:
        changed = False
        diff = {}
        module.connection.op('<request><plugins><check/></plugins></request>')
        installed_plugins = get_installed_plugins(module.connection)
        if state == "present":
            #check if plugin is installed on not
            if plugin in installed_plugins:
                module.exit_json(changed=changed, diff=diff)
            # check plugins from update server
            check_plugins(module.connection)
            # download plugin
            download_plugin(module.connection, plugin)
            diff['download status'] = f'plugin : {plugin} downloaded successfully'
            # install plugin
            install_plugin(module.connection, plugin)
            diff['install status'] = f'plugin : {plugin} installed successfully'
            changed = True
        # state == "absent"
        else:
            if plugin not in installed_plugins:
                module.exit_json(changed=changed, diff=diff)
            uninstall_plugin(module.connection, plugin_name)
            changed= True
            diff['uninstall status'] = f'plugin : {plugin_name} uninstalled successfully'

        module.exit_json(changed=changed, diff=diff)

    except ConnectionError as e:  # pragma: no cover
        module.fail_json(msg="{0}".format(e))

if __name__ == "__main__":  # pragma: no cover
    main()
