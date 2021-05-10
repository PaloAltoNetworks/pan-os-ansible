from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

import pytest
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes

# Adapted from https://github.com/ansible/ansible/blob/devel/test/units/modules/utils.py
# Replicated here for out of band collection development.


def set_module_args(**args):
    if "_ansible_remote_tmp" not in args:
        args["_ansible_remote_tmp"] = "/tmp"
    if "_ansible_keep_remote_files" not in args:
        args["_ansible_keep_remote_files"] = False

    args = json.dumps({"ANSIBLE_MODULE_ARGS": args})
    basic._ANSIBLE_ARGS = to_bytes(args)


class AnsibleExitJson(Exception):
    pass


class AnsibleFailJson(Exception):
    pass


def exit_json(*args, **kwargs):
    if "changed" not in kwargs:
        kwargs["changed"] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    kwargs["failed"] = True
    raise AnsibleFailJson(kwargs)


class ModuleTestCase:
    @pytest.fixture(autouse=True)
    def module_mock(self, mocker):
        return mocker.patch.multiple(
            basic.AnsibleModule, exit_json=exit_json, fail_json=fail_json
        )

    @pytest.fixture
    def connection_mock(self, mocker):
        connection_class_mock = mocker.patch(
            "ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos.Connection"
        )

        connection_class_mock.return_value.api_key.return_value = "foo"

        connection_class_mock.return_value.get_device_info.return_value = {
            "hostname": "PA-VM",
            "model": "PA-VM",
            "serial": "serial",
            "version": "10.0.0",
            "uptime": "uptime",
            "multivsys": "multivsys",
        }

        return connection_class_mock.return_value

    def _run_module(self, module_args):
        set_module_args(**module_args)

        with pytest.raises(AnsibleExitJson) as ex:
            self.module.main()
        return ex.value.args[0]

    def _run_module_fail(self, module_args):
        set_module_args(**module_args)

        with pytest.raises(AnsibleFailJson) as ex:
            self.module.main()
        return ex.value.args[0]


def generate_name(test_case):
    return test_case["name"]
