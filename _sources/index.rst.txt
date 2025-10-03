=====================================
Palo Alto Networks Ansible Collection
=====================================

Version: 3.2.0

The Palo Alto Networks Ansible collection is a collection of modules that
automate configuration and operational tasks on Palo Alto Networks Next
Generation Firewalls (both physical and virtualized) and Panorama.  The
underlying protocol uses API calls that are wrapped within the Ansible
framework.

This is the module reference documentation. Other documentation including
getting started tutorials, how-to guides and other background reading, can
be found at https://pan.dev/ansible/docs/panos/


Installation
============

This collection has the following environment requirements:

* Python 3.10 or higher
* ansible-core 2.16 or higher

Install the collection using `ansible-galaxy`:

.. code-block:: bash

    ansible-galaxy collection install paloaltonetworks.panos

Then in your playbooks you can specify that you want to use the
`panos` collection like so:

.. code-block:: yaml

    collections:
        - paloaltonetworks.panos

* Ansible Galaxy: https://galaxy.ansible.com/ui/repo/published/paloaltonetworks/panos
* Red Hat Catalog: https://catalog.redhat.com/software/collection/paloaltonetworks/panos
* GitHub repo:  https://github.com/PaloAltoNetworks/pan-os-ansible


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   gatheredfilter
   examples
   modules
   history
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


Support
=======
As of version 2.12.2, this Collection of Ansible Modules for PAN-OS is
[certified on Ansible Automation Hub](https://console.redhat.com/ansible/automation-hub/repo/published/paloaltonetworks/panos)
and officially supported for Ansible subscribers. Ansible subscribers can engage
for support through their usual route towards Red Hat.

For those who are not Ansible subscribers, this Collection of Ansible Modules is
also [published on Ansible Galaxy](https://galaxy.ansible.com/ui/repo/published/paloaltonetworks/panos)
to be freely used under an as-is, best effort, support
policy. These scripts should be seen as community supported and Palo
Alto Networks will contribute our expertise as and when possible. We do
not provide technical support or help in using or troubleshooting the
components of the project through our normal support options such as
Palo Alto Networks support teams, or ASC (Authorized Support Centers)
partners and backline support options. The underlying product used (the
VM-Series firewall) by the scripts or templates are still supported, but
the support is only for the product functionality and not for help in
deploying or using the template or script itself.

Unless explicitly tagged, all projects or work posted in our GitHub
repository (at <https://github.com/PaloAltoNetworks>) or sites other
than our official Downloads page on <https://support.paloaltonetworks.com>
are provided under the best effort policy.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
