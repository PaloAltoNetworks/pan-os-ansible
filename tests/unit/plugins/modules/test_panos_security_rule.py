# Copyright 2026 Palo Alto Networks, Inc
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

import copy
import xml.etree.ElementTree as ET

import pytest
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.modules import (
    panos_security_rule,
)
from panos.firewall import Firewall
from panos.panorama import DeviceGroup, Panorama

RULE_XML = """
<entry name="Test" uuid="12345678-1234-1234-1234-123456789abc">
  <from><member>inside</member><member>guest</member></from>
  <to><member>outside</member><member>dmz</member></to>
  <source><member>any</member></source>
  <destination><member>1.1.1.1</member></destination>
  <source-user><member>any</member></source-user>
  <source-hip><member>managed</member><member>contractor</member></source-hip>
  <destination-hip><member>server</member><member>printer</member></destination-hip>
  <application><member>ssh</member></application>
  <service><member>application-default</member></service>
  <category><member>any</member></category>
  <action>allow</action>
  <description>Keep these settings</description>
  <rule-type>universal</rule-type>
  <log-start>no</log-start>
  <log-end>yes</log-end>
  <negate-source>no</negate-source>
  <negate-destination>no</negate-destination>
  <disabled>no</disabled>
  <option><disable-server-response-inspection>no</disable-server-response-inspection></option>
</entry>
"""


class AnsibleExitJson(Exception):
    pass


@pytest.fixture(params=[Firewall, Panorama], ids=["firewall", "panorama"])
def device(request, mocker):
    device = request.param("192.0.2.1", api_key="test-key")
    device._version_info = (10, 0, 0)
    mocker.patch("panos.base.PanDevice.create_from_device", return_value=device)
    if isinstance(device, Panorama):
        group = device.add(DeviceGroup("Test-DG"))
        mocker.patch("panos.panorama.DeviceGroup.refreshall", return_value=[group])
    api = mocker.MagicMock()
    device._xapi_private = api
    response = ET.fromstring("<response><result /></response>")
    response.find("result").append(ET.fromstring(RULE_XML))
    api.get.side_effect = lambda *args, **kwargs: copy.deepcopy(response)
    return device


@pytest.fixture
def run_module(mocker, device):
    def exit_json(**kwargs):
        raise AnsibleExitJson(kwargs)

    mocker.patch.object(AnsibleModule, "exit_json", side_effect=exit_json)

    def run_module(**kwargs):
        params = dict(provider=dict(ip_address="192.0.2.1", api_key="test-key"))
        if isinstance(device, Panorama):
            params["device_group"] = "Test-DG"
        params.update(kwargs)
        mocker.patch("ansible.module_utils.basic._load_params", return_value=params)
        with pytest.raises(AnsibleExitJson) as result:
            panos_security_rule.main()
        return result.value.args[0]

    return run_module


@pytest.mark.parametrize(
    "field,remaining,path",
    [
        ("source_zone", ["inside"], "from"),
        ("destination_zone", ["outside"], "to"),
        ("source_device", ["managed"], "source-hip"),
        ("destination_device", ["server"], "destination-hip"),
    ],
)
@pytest.mark.parametrize("check_mode", [False, True])
def test_gather_replace_removes_member(
    run_module, device, field, remaining, path, check_mode
):
    gathered = run_module(rule_name="Test", state="gathered")
    assert gathered["changed"] is False
    assert gathered["gathered"]["source_device"] == ["managed", "contractor"]
    assert gathered["gathered"]["destination_device"] == ["server", "printer"]

    params = copy.deepcopy(gathered["gathered"])
    params[field] = remaining
    result = run_module(state="replaced", _ansible_check_mode=check_mode, **params)
    assert result["changed"] is True
    if check_mode:
        device.xapi.edit.assert_not_called()
        device.xapi.set.assert_not_called()
        return

    expected = ET.fromstring(RULE_XML)
    expected.find(path).remove(expected.find(path).findall("member")[1])
    actual = ET.fromstring(result["diff"]["after"])
    assert actual.attrib == expected.attrib
    assert {child.tag for child in actual} == {child.tag for child in expected}
    for child in expected:
        assert ET.canonicalize(
            ET.tostring(actual.find(child.tag), encoding="unicode"), strip_text=True
        ) == ET.canonicalize(ET.tostring(child, encoding="unicode"), strip_text=True)

    device.xapi.edit.assert_called_once()
    written_xml = device.xapi.edit.call_args.args[1]
    assert ET.fromstring(written_xml).find(path)[0].text == remaining[0]

    # The next refresh returns the configuration sent to the device.
    response = ET.fromstring("<response><result /></response>")
    response.find("result").append(ET.fromstring(written_xml))
    device.xapi.get.side_effect = lambda *args, **kwargs: copy.deepcopy(response)
    device.xapi.edit.reset_mock()
    repeated = run_module(state="replaced", **params)
    assert repeated["changed"] is False
    device.xapi.edit.assert_not_called()


@pytest.mark.parametrize(
    "field,path",
    [("source_device", "source-hip"), ("destination_device", "destination-hip")],
)
@pytest.mark.parametrize(
    "existing,requested,expected",
    [
        (["any"], ["managed"], ["managed"]),
        (["managed"], ["any"], ["any"]),
        (["managed"], ["contractor"], ["managed", "contractor"]),
    ],
)
def test_merge_device_members(
    run_module, device, field, path, existing, requested, expected
):
    response = ET.fromstring("<response><result /></response>")
    rule = ET.fromstring(RULE_XML)
    members = rule.find(path)
    members.clear()
    for value in existing:
        ET.SubElement(members, "member").text = value
    response.find("result").append(rule)
    device.xapi.get.side_effect = lambda *args, **kwargs: copy.deepcopy(response)

    result = run_module(rule_name="Test", state="merged", **{field: requested})
    assert result["changed"] is True
    assert result["after"][field] == expected
    assert len(device.xapi.edit.call_args_list) == 1
    assert device.xapi.edit.call_args.args[0].endswith("/" + path)


def test_merge_zone_preserves_devices(run_module, device):
    result = run_module(rule_name="Test", state="merged", source_zone=["vpn"])
    assert result["changed"] is True
    assert result["after"]["source_zone"] == ["inside", "guest", "vpn"]
    assert result["after"]["source_device"] == ["managed", "contractor"]
    assert result["after"]["destination_device"] == ["server", "printer"]
    device.xapi.edit.assert_called_once()
    assert device.xapi.edit.call_args.args[0].endswith("/from")


@pytest.mark.parametrize("version", [(9, 1, 0), (10, 0, 0), (11, 1, 0)])
@pytest.mark.parametrize("state", ["present", "replaced", "merged"])
@pytest.mark.parametrize("devices", [None, ["managed", "contractor"]])
def test_create_devices(run_module, device, version, state, devices):
    device._version_info = version
    device.xapi.get.side_effect = None
    device.xapi.get.return_value = ET.fromstring("<response><result /></response>")

    result = run_module(
        rule_name="Test", state=state, source_device=devices, destination_device=devices
    )
    assert result["changed"] is True
    device.xapi.set.assert_called_once()
    created = ET.fromstring(device.xapi.set.call_args.args[1])
    for path in ("source-hip", "destination-hip"):
        if version >= (10, 0, 0):
            assert [member.text for member in created.findall(path + "/member")] == (
                devices or ["any"]
            )
        else:
            assert created.find(path) is None
