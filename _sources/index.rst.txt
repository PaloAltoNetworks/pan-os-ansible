=====================================
Palo Alto Networks Ansible Collection
=====================================

Version: 2.2.0

The Palo Alto Networks Ansible collection is a collection of modules that
automate configuration and operational tasks on Palo Alto Networks Next
Generation Firewalls (both physical and virtualized) and Panorama.  The
underlying protocol uses API calls that are wrapped within the Ansible
framework.

This is a **community supported project**. You can find the community
supported live page at https://live.paloaltonetworks.com/ansible.


Installation
============

Ansible 2.9 is **required** for using collections.

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

   examples
   modules
   history
   contributing
   authors
   license


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
