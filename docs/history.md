Release History
===============

v1.1.0
------

- *Released*: 2020-03-10

New Modules:

* `panos_ipv6_address`

Enhancements:

* Added `diff` support for checkmode

Bug Fixes:

* `panos_l2_subinterface` works with aggregate interface parents now
* `panos_facts` can now pull IPv6 address information

v1.0.3
------

- *Released*: 2020-02-27

New Modules:

* `panos_vm_auth_key`

Bug Fixes:

* `panos_aggregate_interface`
* `panos_match_rule`

v1.0.2
------

- *Released*: 2020-02-11

This is the initial version of the `panos` collection. This is a straight port
of <https://galaxy.ansible.com/paloaltonetworks/paloaltonetworks> v2.4.0.
