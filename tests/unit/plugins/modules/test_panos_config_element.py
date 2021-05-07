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

__metaclass__ = type

import xml.etree.ElementTree

import pytest
from ansible_collections.mrichardson03.panos.plugins.modules import panos_config_element
from ansible_collections.mrichardson03.panos.plugins.modules.panos_config_element import (
    xml_compare,
    xml_contained,
)

from .common.utils import ModuleTestCase

XPATH_ALL = "/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/address"

GET_ADDRESS_EMPTY = """
<response status="success" code="7">
    <result/>
</response>
"""

XPATH_TEST_ONE = "/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/address/entry[@name='Test-One']"

GET_ADDRESS_TEST_ONE = """
<response status="success" code="19">
    <result total-count="1" count="1">
        <entry name="Test-One">
            <ip-netmask>1.1.1.1</ip-netmask>
        </entry>
    </result>
</response>
"""

TEST_ONE = """
<entry name="Test-One">
    <ip-netmask>1.1.1.1</ip-netmask>
</entry>
"""

TEST_ONE_MOD = """
<entry name="Test-One">
    <ip-netmask>2.2.2.2</ip-netmask>
</entry>
"""

XPATH_SYSTEM = (
    "/config/devices/entry[@name='localhost.localdomain']/deviceconfig/system"
)

GET_EMPTY_SYSTEM = """
<response status="success" code="19">
    <result total-count="1" count="1">
        <system>
            <type>
                <static/>
            </type>
        </system>
    </result>
</response>
"""

SIMPLE_SET = """
<login-banner>You have accessed a protected system.
Log off immediately if you are not an authorized user.</login-banner>
"""

GET_SYSTEM = """
<response status="success" code="19">
    <result total-count="1" count="1">
        <system>
            <login-banner>Help!  I'm trapped in a firewall factory!</login-banner>
            <timezone>UTC</timezone>
        </system>
    </result>
</response>
"""


def make_etree(xml_string):
    return xml.etree.ElementTree.fromstring(xml_string) if xml_string else None


@pytest.mark.parametrize(
    "one_xml,two_xml,result",
    [
        # Identity
        ("<one/>", "<one/>", True),
        # Comparison with None
        ("<one/>", None, False),
        # Tag doesn't match
        ("<one/>", "<two/>", False),
        # Attributes are successfully ignored
        ("<one admin='admin' dirtyId='1' time='modify time'/>", "<one/>", True),
        (
            "<one/>",
            "<one admin='admin' dirtyId='1' time='modify time'/>",
            True,
        ),
        # Attributes are checked
        ("<one foo='bar'/>", "<one foo='bar'/>", True),
        # Check attributes not in other document
        ("<one foo='bar'/>", "<one/>", False),
        ("<one/>", "<one foo='bar'/>", False),
        # Attributes not equal
        ("<one foo='bar'/>", "<one foo='baz'/>", False),
        # Text not equal
        ("<one>two</one>", "<one>three</one>", False),
        # Check number of children
        ("<one><two/></one>", "<one><two/></one>", True),
        ("<one><two/></one>", "<one><two/><three/></one>", False),
        # Child documents are equal
        ("<one><two>two</two></one>", "<one><two>three</two></one>", False),
    ],
)
def test_xml_compare(one_xml, two_xml, result):
    one = make_etree(one_xml)
    two = make_etree(two_xml)

    assert xml_compare(one, two) is result


BIG_XML = """
<one>
    <two>
        <three>three text</three>
        <four>four text</four>
        <five>
            <six>six text</six>
        </five>
    </two>
    <entry name="one">
        <one>
            <member>member1</member>
            <member>member2</member>
        </one>
    </entry>
    <entry name="two">
        <two>
            <member>member3</member>
        </two>
    </entry>
</one>
"""

# True
SMALL_ONE = """
<one>
    <two>
        <three>three text</three>
        <four>four text</four>
    </two>
</one>
"""

# True
SMALL_TWO = """
<one>
    <two>
        <five>
            <six>six text</six>
        </five>
    </two>
</one>
"""

# False - keys match, but wrong place in tree
SMALL_THREE = """
<one>
    <three>three text</three>
</one>
"""

# True - member tags match exactly
SMALL_FOUR = """
<one>
    <entry name="one">
        <one>
            <member>member1</member>
            <member>member2</member>
        </one>
    </entry>
</one>
"""

# False - member counts don't match exactly
SMALL_FIVE = """
<one>
    <entry name="one">
        <one>
            <member>member1</member>
        </one>
    </entry>
</one>
"""


@pytest.mark.parametrize(
    "small_xml,result",
    [
        (None, False),
        (SMALL_ONE, True),
        (SMALL_TWO, True),
        (SMALL_THREE, False),
        (SMALL_FOUR, True),
        (SMALL_FIVE, False),
    ],
)
def test_xml_contained(small_xml, result):
    big = make_etree(BIG_XML)
    small = make_etree(small_xml)

    assert xml_contained(big, small) is result


class TestPanosConfigElement(ModuleTestCase):
    module = panos_config_element

    def test_create(self, connection_mock):
        connection_mock.get.return_value = GET_ADDRESS_EMPTY

        args = {"xpath": XPATH_TEST_ONE, "element": TEST_ONE, "edit": True}

        result = self._run_module(args)

        assert result["changed"]
        assert connection_mock.edit.call_count == 1

    def test_create_fail(self, connection_mock):
        connection_mock.get.return_value = GET_ADDRESS_EMPTY

        args = {"xpath": XPATH_TEST_ONE, "edit": True}

        result = self._run_module_fail(args)

        assert "'element' is required" in result["msg"]

    def test_create_idempotent(self, connection_mock):
        connection_mock.get.return_value = GET_ADDRESS_TEST_ONE

        args = {"xpath": XPATH_TEST_ONE, "element": TEST_ONE, "edit": True}

        result = self._run_module(args)

        assert not result["changed"]
        assert connection_mock.set.call_count == 0

    def test_modify(self, connection_mock):
        connection_mock.get.return_value = GET_ADDRESS_TEST_ONE

        args = {"xpath": XPATH_TEST_ONE, "element": TEST_ONE_MOD, "edit": True}

        result = self._run_module(args)

        assert result["changed"]
        assert connection_mock.edit.call_count == 1

    def test_delete(self, connection_mock):
        connection_mock.get.return_value = GET_ADDRESS_TEST_ONE

        args = {"xpath": XPATH_TEST_ONE, "state": "absent"}

        result = self._run_module(args)

        assert result["changed"]
        assert connection_mock.delete.call_count == 1

    def test_delete_idempotent(self, connection_mock):
        connection_mock.get.return_value = GET_ADDRESS_EMPTY

        args = {"xpath": XPATH_TEST_ONE, "state": "absent"}

        result = self._run_module(args)

        assert not result["changed"]
        assert connection_mock.delete.call_count == 0

    def test_set(self, connection_mock):
        connection_mock.get.return_value = GET_EMPTY_SYSTEM

        args = {
            "xpath": XPATH_SYSTEM,
            "element": SIMPLE_SET,
        }

        result = self._run_module(args)

        assert result["changed"] is True
        assert connection_mock.set.call_count == 1

    def test_set_modify(self, connection_mock):
        connection_mock.get.return_value = GET_SYSTEM

        args = {"xpath": XPATH_SYSTEM, "element": "<login-banner>foo</login-banner>"}

        result = self._run_module(args)

        assert result["changed"] is True
        assert connection_mock.set.call_count == 1

    def test_set_multi(self, connection_mock):
        connection_mock.get.return_value = GET_SYSTEM

        args = {
            "xpath": XPATH_SYSTEM,
            "element": "<login-banner>foo</login-banner><timezone>EST</timezone>",
        }

        result = self._run_module(args)

        assert result["changed"] is True
        assert connection_mock.set.call_count == 1

    def test_set_multi_idempotent(self, connection_mock):
        connection_mock.get.return_value = GET_SYSTEM

        args = {
            "xpath": XPATH_SYSTEM,
            "element": "<login-banner>Help!  I'm trapped in a firewall factory!</login-banner><timezone>UTC</timezone>",
        }

        result = self._run_module(args)

        assert result["changed"] is False
        assert connection_mock.set.call_count == 0
