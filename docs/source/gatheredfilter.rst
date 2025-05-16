===============
Gathered Filter
===============

Starting in *v2.11.0*, the modules belonging to this collection that behave like
network resource modules all support a `gathered_filter` parameter.  Where present,
this parameter provides advanced filtering for PAN-OS objects beyond simple name
matching.


The `gathered_filter` Option
============================

The `gathered_filter` parameter is essentially a mini rules engine, allowing users to
specify potentially very complex logic to retrieve information on PAN-OS objects
present.  Features such as arbitrary field searching and regular expressions are all
supported.

The generic syntax for the value of this paramater looks likie this:

.. code-block:: bash

    CONDITION1 [and/or CONDITION2....]

Parenthesis between conditions are supported.

Each condition in the logic has the following format:

.. code-block:: bash

    [not] field [operator [value]]


Fields
======

Fields supported are the fields of the module itself supports, as is related to the
pan-os-python object being configured by the module.  Besides the object's fields, there
are a few other special fields that are supported.

* `true`: Always `True`.
* `false`: Always `False`.
* `*`: This is a shortcut that returns everything.

Attempting to match against a field name that is part of a parent (read: the XPATH)
will result in an error.  As an example, one could not retrieve all address objects
across all vsys.  The vsys, which is part of the parent XPATH, must be fixed, and the
searching happens underneath that.


Operators
=========

There are two scenarios:  an operator that expects a value and one that doesn't.


Operators - No Value
--------------------

* `is-none`: `True` if the field is python `None`
* `is-not-none`: `True` if the field is not python `None`
* `is-true`: `True` if the field evaluates to `True` in a boolean context in python.
* `is-false`: `True` if the field evaluates to `False` in a boolean context in python.


Operators - Requires a Value
----------------------------

For any of the regex operators, please refer to the python documentation on the `re` library.

https://docs.python.org/3/library/re.html

All regex searches are using `re.search()`, so use anchoring the limit the regex to the
front or end of the field's value as appropriate.

Note that the tokens in the `gathered_filter` parameter are split using `shlex`, so quotes
can be used if a literal space character needs to be matched in the value.

* `==`: `True` if `field` equals `value`
* `!=`: `True` if `field` does not equal `value`
* `<`: (int/float) `True` if `field` is less than `value` (value is cast to a float)
* `<=`: (int/float) `True` if `field` is less than or equal to `value` (value is cast to a float)
* `>`: (int/float) `True` if `field` is greater than `value` (value is cast to a float)
* `>=`: (int/float) `True` if `field` is greater than or equal to `value` (value is cast to a float)
* `contains`: (string/list) `True` if `value` is in `field`.
* `does-not-contain`: (string/list) `True` if `value` is not in `field`
* `starts-with`: (string) `True` if `field` starts with `value`
* `does-not-start-with`: (string) `True` if `field` does not start with `value`
* `ends-with`: (string) `True` if `field` ends with `value`
* `does-not-end-with`: (string) `True` if `field` does not end with `value`
* `matches-regex`: (string) `True` if `re.search(value, field)` finds a hit.
* `does-not-match-regex`: (string) `True` if `re.search(value, field)` finds nothing.
* `contains-regex`: (list) `True` if the `value` regex matches any item in `field`.
* `does-not-contain-regex`: (list) `True` if the `value` regex does not match any item in `field`.


Return Values
=============

The two return values of `gathered` and `gathered_xml` are still used, but `gathered` is now
a list of dicts instead of a dict, and `gathered_xml` is a list of strings instead of a string.

Even if the match criteria returns zero results, as long as there is no syntax error, this
module will not return an error.


Examples
========

Example - Match All
-------------------

These all do the same thing, listed from fastest to slowest.

.. code-block:: yaml

    gathered_filter: '*'

.. code-block:: yaml

    gathered_filter: 'true'

.. code-block:: yaml

    gathered_filter: 'name matches-regex .*?'


Example - Matching a Regex
--------------------------

It is possible to write regex in the following formats;

* Standard regex in single quotation marks(`'`)
* Escaped backslash in double quotation marks(`"`)
* Using folded block scalar followed by a dash (`>-`) without any quotation marks

See examples below which correspond to the same regex:

.. code-block:: yaml

    gathered_filter: 'name matches-regex \sPAN\s'

.. code-block:: yaml

    gathered_filter: "name matches-regex \\sPAN\\s"

.. code-block:: yaml

    gathered_filter: >-
      name matches-regex \sPAN\s


Example - Matching a Suffix
---------------------------

.. code-block:: yaml

    gathered_filter: 'description ends-with _sales'


Example - Matching Two Things
-----------------------------

.. code-block:: yaml

    gathered_filter: 'description starts-with DMZ or description ends-with " New Zealand"'


Example - Searching Within Listings
-----------------------------------

.. code-block:: yaml

    gathered_filter: 'interfaces contains ethernet1/1'


Example - Groupings
-------------------

.. code-block:: yaml

    gathered_filter: 'name ends-with _dmz and (tag is-false or description is-false)'
