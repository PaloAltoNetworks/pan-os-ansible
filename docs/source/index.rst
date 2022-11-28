=====================================
Palo Alto Networks Ansible Collection
=====================================

Version: 2.12.1

The Palo Alto Networks Ansible collection is a collection of modules that
automate configuration and operational tasks on Palo Alto Networks Next
Generation Firewalls (both physical and virtualized) and Panorama.  The
underlying protocol uses API calls that are wrapped within the Ansible
framework.

This is a **community supported project**. You can find the community
supported live page at https://live.paloaltonetworks.com/ansible.


Installation
============

This collection has the following environment requirements:

* Python 3.8 or higher
* Ansible 2.9 or higher

Install the collection using `ansible-galaxy`:

.. code-block:: bash

    ansible-galaxy collection install paloaltonetworks.panos

Then in your playbooks you can specify that you want to use the
`panos` collection like so:

.. code-block:: yaml

    collections:
        - paloaltonetworks.panos

* Ansible Galaxy: https://galaxy.ansible.com/PaloAltoNetworks/panos
* GitHub repo:  https://github.com/PaloAltoNetworks/pan-os-ansible


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   gatheredfilter
   examples
   modules
   history
   contributing
   authors
   license


Collection Dependencies
=======================

* pan-python
* pan-os-python
* xmltodict (certain modules only)

If you believe you have installed these dependencies but Ansible is not finding them, it is likely a
problem with where your local shell is searching for installed dependencies and where Ansible is
searching for them.  Try running a simple `panos_op` playbook to run the command 'show system info",
and if that errors out, compare the `sys.path` in the output against where you think Ansible looking
for dependencies at.

Configuring `ANSIBLE_PYTHON_INTERPRETER` is probably the solution to this issue:

https://docs.ansible.com/ansible/latest/reference_appendices/python_3_support.html#using-python-3-on-the-managed-machines-with-commands-and-playbooks


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
