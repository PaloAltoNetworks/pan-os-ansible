#!/usr/bin/env python

# Taken from: https://raw.githubusercontent.com/sensu/sensu-go-ansible/master/fix-pytest-ini.py

from __future__ import absolute_import, division, print_function

import os.path

from ansible_test._internal.util import ANSIBLE_TEST_DATA_ROOT

__metaclass__ = type


with open(os.path.join(ANSIBLE_TEST_DATA_ROOT, "pytest.ini")) as fd:
    lines = fd.readlines(True)

with open(os.path.join(ANSIBLE_TEST_DATA_ROOT, "pytest.ini"), "w") as fd:
    fd.writelines(line for line in lines if line.strip()[0] != "#")
