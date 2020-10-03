PAN-OS Ansible Collection
=========================

![CI/CD](https://github.com/PaloAltoNetworks/pan-os-ansible/workflows/CI/CD/badge.svg?branch=develop)

Ansible collection that automates the configuration and operational tasks on
Palo Alto Networks Next Generation Firewalls, both physical and virtualized form
factors, using the PAN-OS API.

-   Free software: Apache 2.0 License
-   Documentation:
    <https://paloaltonetworks.github.io/pan-os-ansible/>
-   PANW community supported live page:
    <http://live.paloaltonetworks.com/ansible>
-   Repo:
    <https://github.com/PaloAltoNetworks/pan-os-ansible>
-   Example Playbooks:
    <https://github.com/PaloAltoNetworks/ansible-playbooks>

Tested Ansible Versions
-----------------------

This collection is tested with the most current Ansible 2.9 and 2.10 releases.  Ansible versions
before 2.9.10 are **not supported**.

Installation
------------

Install this collection using the Ansible Galaxy CLI:

```bash
ansible-galaxy collection install paloaltonetworks.panos
```

Usage
-----

Either refer to modules by their full FQCN or use the `collections`
specification in your playbooks:

```yaml
  collections:
    - paloaltonetworks.panos

  tasks:
  - name: Get the system info
    panos_op:
      provider: '{{ provider }}'
      cmd: 'show system info'
    register: res

  - debug:
      msg: '{{ res.stdout }}'
```

Role / Collection Compatibility
-------------------------------

The Palo Alto Networks PAN-OS Ansible modules were previously distributed as an
Ansible Galaxy role (<https://galaxy.ansible.com/paloaltonetworks/paloaltonetworks>).
Since Ansible 2.9, RedHat has urged developers to migrate to `collections` to
organize and distribute their integrations.

The 1.0 version of this collection is a straight port of the Ansible Galaxy
role v2.4.0.  If you are using Ansible 2.9 or later and you are using the
role, then you can safely use this instead with no change in functionality.  Just
specify the `collections` spec (as mentioned above in the Usage section), remove
`PaloAltoNetworks.paloaltonetworks` from the `roles` spec, and you're done!

Python Compatibility
--------------------

As Ansible still wants to support python2, this collection will still work
under python2.

Support
-------

This template/solution is released under an as-is, best effort, support
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
