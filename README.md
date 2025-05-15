PAN-OS Ansible Collection
=========================

![CI](https://github.com/PaloAltoNetworks/pan-os-ansible/workflows/CI/badge.svg?branch=develop)
![Version on Galaxy](https://img.shields.io/badge/dynamic/json?style=flat&label=Ansible+Galaxy+Latest+Version&prefix=v&url=https://galaxy.ansible.com/api/v3/plugin/ansible/content/published/collections/index/paloaltonetworks/panos/&query=highest_version.version)

Ansible collection that automates the configuration and operational tasks on
Palo Alto Networks Next Generation Firewalls, both physical and virtualized form
factors, using the PAN-OS API.

-   Free software: Apache 2.0 License
-   Documentation:
    <https://pan.dev/ansible/docs/panos>
-   Getting started tutorials, how-to guides and other background reading:
    <https://pan.dev/ansible/docs/panos>
-   Repo:
    <https://github.com/PaloAltoNetworks/pan-os-ansible>
-   Example Playbooks:
    <https://github.com/PaloAltoNetworks/ansible-playbooks>

Tested Ansible Versions
-----------------------

This collection is tested with the most current Ansible releases.  Ansible versions
before 2.16 are **not supported**.

Python Version
--------------

The minimum python version for this collection is python 3.10.

Installation
------------

Install this collection using the Ansible Galaxy CLI:

```bash
ansible-galaxy collection install paloaltonetworks.panos
```

Usage
-----

Refer to modules by their full FQCN:

```yaml
  tasks:
    - name: Get the system info
      paloaltonetworks.panos.panos_op:
        provider: '{{ device }}'
        cmd: 'show system info'
      register: res

    - name: Show the system info
      ansible.builtin.debug:
        msg: '{{ res.stdout }}'
```
(Note that [use of the `collections` key is now discouraged](https://ansible-lint.readthedocs.io/rules/fqcn/))

Releasing, changelogs, versioning and deprecation
-------------------------------------------------
There is currently no intended release frequency for major and minor versions. The intended frequency of patch versions is never, they are released for fixing issues or to address security concerns.

Changelog details are created automatically and more recently can be found [here](./CHANGELOG.md), but also the full history is [here](https://github.com/PaloAltoNetworks/pan-os-ansible/releases).

[Semantic versioning](https://semver.org/) is adhered to for this project.

Deprecations are done by version number, not by date or by age of release. Breaking change deprecations will only be made with major versions.

Support
-------

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
