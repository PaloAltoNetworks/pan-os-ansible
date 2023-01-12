PAN-OS Ansible Collection
=========================

![CI](https://github.com/PaloAltoNetworks/pan-os-ansible/workflows/CI/badge.svg?branch=develop)
![Version on Galaxy](https://img.shields.io/badge/dynamic/json?style=flat&label=Ansible+Galaxy&prefix=v&url=https://galaxy.ansible.com/api/v2/collections/paloaltonetworks/panos/&query=latest_version.version)

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

This collection is tested with the most current Ansible releases.  Ansible versions
before 2.9.10 are **not supported**.

Python Version
--------------

The minimum python version for this collection is python 3.8.

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

Support
-------

As of version 2.12.2, this Collection of Ansible Modules for PAN-OS is
[certified on Ansible Automation Hub](https://console.redhat.com/ansible/automation-hub/repo/published/paloaltonetworks/panos)
and officially supported for Ansible subscribers. Ansible subscribers can engage
for support through their usual route towards Red Hat.

For those who are not Ansible subscribers, this Collection of Ansible Modules is
also [published on Ansible Galaxy](https://galaxy.ansible.com/paloaltonetworks/panos)
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
