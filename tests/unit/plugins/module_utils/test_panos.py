# Copyright 2021 Palo Alto Networks, Inc
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

__metaclass__ = type

from unittest.mock import MagicMock, PropertyMock, patch

import pytest
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    get_connection,
)

from panos.errors import PanDeviceError
from panos.firewall import Firewall
from panos.panorama import DeviceGroup, Panorama, Template, TemplateStack
from panos.policies import PostRulebase, PreRulebase, Rulebase


# Run all tests with mocked firewall unless specified.
@pytest.fixture(autouse=True)
def firewall_mock(mocker):
    fw = Firewall("192.168.1.1", "admin", "password", "API_KEY")
    fw._version_info = (10, 0, 0)

    create_from_device_mock = mocker.patch(
        "panos.base.PanDevice.create_from_device", return_value=fw
    )
    return create_from_device_mock.return_value


@pytest.fixture
def panorama_mock(mocker):
    pano = Panorama("192.168.2.1", "admin", "password", "API_KEY")
    pano._version_info = (10, 0, 0)

    create_from_device_mock = mocker.patch(
        "panos.base.PanDevice.create_from_device", return_value=pano
    )

    the_dg = DeviceGroup(name="the_dg")
    the_template = Template(name="the_template")
    the_stack = TemplateStack(name="the_stack")

    mocker.patch("panos.panorama.DeviceGroup.refreshall", return_value=[the_dg])
    mocker.patch("panos.panorama.Template.refreshall", return_value=[the_template])
    mocker.patch("panos.panorama.TemplateStack.refreshall", return_value=[the_stack])

    return create_from_device_mock.return_value


class AnsibleFailJson(Exception):
    pass


def fail_json_exception(*args, **kwargs):
    raise AnsibleFailJson(kwargs["msg"])


@pytest.fixture(autouse=True)
def module_mock(mocker):
    module = MagicMock(spec=AnsibleModule)

    params = PropertyMock()

    params.return_value = {
        "provider": {
            "ip_address": "192.168.1.1",
            "username": "admin",
            "password": "password",
            "api_key": None,
            "port": "443",
            "serial_number": None,
        }
    }

    type(module).params = params

    # Make 'fail_json()' throw an execption instead for easy tracking.
    module.fail_json = fail_json_exception

    return module


# get_pandevice_parent()

# General Tests


# Happy path: module requires (very) low pan-os-python and PAN-OS versions, and
# we're connecting to a firewall.  Should not error or have deprecation
# warnings.
def test_get_connection(module_mock):
    helper = get_connection(
        min_pandevice_version=(0, 0, 1),
        min_panos_version=(0, 0, 1),
        argument_spec=dict(),
    )
    parent = helper.get_pandevice_parent(module_mock)

    assert isinstance(parent, Firewall)
    assert module_mock.deprecate.call_count == 0


# Error if pan-os-python is not found.
@patch(
    "ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos.HAS_PANDEVICE",
    False,
)
def test_missing_pandevice(module_mock):
    helper = get_connection(
        argument_spec=dict(),
    )

    with pytest.raises(AnsibleFailJson) as e:
        parent = helper.get_pandevice_parent(module_mock)

    assert e.match("Missing required library")


# Show deprecation warning if the installed version of pan-os-python is less
# than 1.0.0.
@patch("panos.__version__", "0.0.1")
def test_old_pandevice(module_mock):
    helper = get_connection(
        argument_spec=dict(),
    )
    parent = helper.get_pandevice_parent(module_mock)

    assert module_mock.deprecate.call_count == 1


# Error if installed version of pan-os-python is too low to run the module.
def test_min_pandevice_version(module_mock):
    helper = get_connection(
        min_pandevice_version=(9999, 0, 0),
        argument_spec=dict(),
    )

    with pytest.raises(AnsibleFailJson) as e:
        parent = helper.get_pandevice_parent(module_mock)

    assert e.match("< minimum version")


# Error if no provider parameters are provided.
def test_no_provider(module_mock):
    helper = get_connection(argument_spec=dict())
    module_mock.params.update({"provider": None})

    with pytest.raises(AnsibleFailJson) as e:
        parent = helper.get_pandevice_parent(module_mock)

    assert e.match("Provider params are required")


# Error if bad values for timeout are given.
@pytest.mark.parametrize(
    "timeout,msg", [("blah", "must be an int"), (-1, "greater than or equal to 0")]
)
def test_bad_timeout(module_mock, timeout, msg):
    helper = get_connection(argument_spec=dict())

    with pytest.raises(ValueError) as e:
        parent = helper.get_pandevice_parent(module_mock, timeout=timeout)

    assert e.match(msg)


# Error if the connection to the device fails or times out.
@patch("panos.base.PanDevice.create_from_device", side_effect=PanDeviceError())
@pytest.mark.parametrize(
    "timeout,msg", [(0, "Failed connection"), (1, "Connection timeout")]
)
def test_connection_timeout(create_from_device_mock, module_mock, timeout, msg):
    helper = get_connection(argument_spec=dict())

    with pytest.raises(AnsibleFailJson) as e:
        parent = helper.get_pandevice_parent(module_mock, timeout=timeout)

    assert e.match(msg)


# Error if the version of PAN-OS is too low to run the module against.
def test_min_panos_version(module_mock):
    helper = get_connection(min_panos_version=(9999, 0, 0), argument_spec=dict())

    with pytest.raises(AnsibleFailJson) as e:
        parent = helper.get_pandevice_parent(module_mock)

    assert e.match("< minimum version")


# Show a deprecation warning if the 'commit' option is specified.
def test_commit_deprecate(module_mock):
    helper = get_connection(argument_spec=dict())
    module_mock.params.update({"commit": True})

    parent = helper.get_pandevice_parent(module_mock)

    assert module_mock.deprecate.call_count == 1


# Panorama Tests


# Test that specifying a serial number in 'provider' will return a firewall
# object.
def test_firewall_via_panorama(module_mock, panorama_mock):
    helper = get_connection(argument_spec=dict())
    module_mock.params["provider"].update({"serial_number": "1234"})
    parent = helper.get_pandevice_parent(module_mock)

    assert isinstance(parent, Firewall)


# Error if 'panorama_error' is set and the connected device is Panorama.
def test_panorama_error(module_mock, panorama_mock):
    helper = get_connection(panorama_error="PANORAMA ERROR", argument_spec=dict())

    with pytest.raises(AnsibleFailJson) as e:
        parent = helper.get_pandevice_parent(module_mock)

    assert e.match("PANORAMA ERROR")


# Test that specifying 'template' will return that template, if it exists.
@pytest.mark.parametrize("template_stack", [True, False, None])
@pytest.mark.parametrize("template_is_optional", [True, False, None])
def test_template(module_mock, panorama_mock, template_stack, template_is_optional):
    helper = get_connection(
        argument_spec=dict(),
        template=True,
        template_is_optional=template_is_optional,
    )
    module_mock.params.update({"template": "the_template", "template_stack": None})

    parent = helper.get_pandevice_parent(module_mock)

    assert isinstance(parent, Template)
    assert parent.name == "the_template"


# Error if the template specified by 'template' is not found.
@patch("panos.panorama.Template.refreshall", return_value=[])
@pytest.mark.parametrize("template_stack", [True, False])
def test_template_not_found(
    refreshall_mock, module_mock, panorama_mock, template_stack
):
    helper = get_connection(
        argument_spec=dict(), template=True, template_stack=template_stack
    )
    module_mock.params.update({"template": "the_template", "template_stack": None})

    with pytest.raises(AnsibleFailJson) as e:
        parent = helper.get_pandevice_parent(module_mock)

    assert e.match('Template "the_template" is not present.')


# Test that specifying 'template_stack' will return that template stack, if it
# exists.
def test_template_stack(module_mock, panorama_mock):
    helper = get_connection(argument_spec=dict(), template_stack=True)
    module_mock.params.update({"template_stack": "the_stack", "template": None})

    parent = helper.get_pandevice_parent(module_mock)

    assert isinstance(parent, TemplateStack)
    assert parent.name == "the_stack"


# Error if the template stack specified by 'template_stack' is not found.
@patch("panos.panorama.TemplateStack.refreshall", return_value=[])
def test_template_stack_not_found(refreshall_mock, module_mock, panorama_mock):
    helper = get_connection(argument_spec=dict(), template_stack=True)
    module_mock.params.update({"template_stack": "the_stack"})

    with pytest.raises(AnsibleFailJson) as e:
        parent = helper.get_pandevice_parent(module_mock)

    assert e.match('Template stack "the_stack" is not present')


# Test when 'template' and 'template_stack' are not provided.
@pytest.mark.parametrize("template", [True, False, None])
@pytest.mark.parametrize("template_stack", [True, False, None])
@pytest.mark.parametrize("template_is_optional", [True, False])
def test_template_or_template_stack_not_provided(
    module_mock, panorama_mock, template, template_stack, template_is_optional
):
    helper = get_connection(
        argument_spec=dict(),
        template=template,
        template_stack=template_stack,
        template_is_optional=template_is_optional,
    )
    module_mock.params.update({"template": None, "template_stack": None})

    # This should succeed in two different scenarios:
    # 1. When neither were specified as required by the module.
    if template is None and template_stack is None:
        parent = helper.get_pandevice_parent(module_mock)
        assert isinstance(parent, Panorama)

    # 2. When they were marked as optional by the module.
    elif template_is_optional is True:
        parent = helper.get_pandevice_parent(module_mock)
        assert isinstance(parent, Panorama)

    # All others should fail.
    else:
        with pytest.raises(AnsibleFailJson) as e:
            parent = helper.get_pandevice_parent(module_mock)


# Error if both 'template' and 'template_stack' are specified.
def test_both_template_and_template_stack(module_mock, panorama_mock):
    helper = get_connection(
        template=True,
        template_stack=True,
        template_is_optional=False,
        argument_spec=dict(),
    )
    module_mock.params.update(
        {"template": "the_template", "template_stack": "the_stack"}
    )

    with pytest.raises(AnsibleFailJson) as e:
        parent = helper.get_pandevice_parent(module_mock)

    assert e.match("Specify either the template or the template stack, not both.")


# Test that specifying 'device_group' will return that device group, if it
# exists.
def test_device_group(module_mock, panorama_mock):
    helper = get_connection(
        device_group=True,
        argument_spec=dict(),
    )
    module_mock.params.update({"device_group": "the_dg"})

    parent = helper.get_pandevice_parent(module_mock)

    assert isinstance(parent, DeviceGroup)


# Error if the device group specified by 'device_group' is not found.
@patch("panos.panorama.DeviceGroup.refreshall", return_value=[])
def test_device_group_not_found(device_group_mock, module_mock, panorama_mock):
    helper = get_connection(
        device_group=True,
        argument_spec=dict(),
    )
    module_mock.params.update({"device_group": "the_dg"})

    with pytest.raises(AnsibleFailJson) as e:
        parent = helper.get_pandevice_parent(module_mock)

    assert e.match('Device group "the_dg" is not present.')


# Test that specifying 'rulebase' will yield the desired rulebase.
@pytest.mark.parametrize(
    "rulebase_str,rulebase_class",
    [
        ("pre-rulebase", PreRulebase),
        ("rulebase", Rulebase),
        ("post-rulebase", PostRulebase),
    ],
)
@pytest.mark.parametrize("device_group_name", [("the_dg"), (None)])
def test_panorama_rulebases(
    module_mock, panorama_mock, rulebase_str, rulebase_class, device_group_name
):
    helper = get_connection(device_group=True, rulebase=True, argument_spec=dict())
    module_mock.params.update(
        {"device_group": device_group_name, "rulebase": rulebase_str}
    )

    rulebase = helper.get_pandevice_parent(module_mock)

    assert isinstance(rulebase, rulebase_class)

    if device_group_name:
        assert rulebase.parent.name == device_group_name
        assert isinstance(rulebase.parent, DeviceGroup)
    else:
        assert isinstance(rulebase.parent, Panorama)


# Error if the rulebase specified by 'rulebase' is not found.
def test_panorama_rulebase_error(module_mock, panorama_mock):
    helper = get_connection(rulebase=True, argument_spec=dict())
    module_mock.params.update({"rulebase": "doesntexist"})

    with pytest.raises(AnsibleFailJson) as e:
        parent = helper.get_pandevice_parent(module_mock)

    assert e.match('Rulebase "doesntexist" is not present.')


# Firewall Tests


# Specifying a rulebase using the 'rulebase' parameter should only ever get
# the main rulebase when connecting to a firewall.
@pytest.mark.parametrize(
    "rulebase_name",
    ["pre-rulebase", "rulebase", "post-rulebase", "doesnt-exist"],
)
def test_firewall_rulebase(module_mock, rulebase_name):
    helper = get_connection(rulebase=True, argument_spec=dict())
    module_mock.params.update({"rulebase": rulebase_name})

    rulebase = helper.get_pandevice_parent(module_mock)

    assert isinstance(rulebase, Rulebase)
    assert isinstance(rulebase.parent, Firewall)


# Error if 'firewall_error' is set and the connected device is a firewall.
def test_firewall_error(module_mock):
    helper = get_connection(firewall_error="FIREWALL ERROR", argument_spec=dict())

    with pytest.raises(AnsibleFailJson) as e:
        parent = helper.get_pandevice_parent(module_mock)

    assert e.match("FIREWALL ERROR")
