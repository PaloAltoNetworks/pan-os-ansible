# pan-os-ansible - paloaltonetworks.panos Ansible Collection

![CI](https://github.com/PaloAltoNetworks/pan-os-ansible/workflows/CI/badge.svg?branch=develop)
![Version on Galaxy](https://img.shields.io/badge/dynamic/json?style=flat&label=Ansible+Galaxy&prefix=v&url=https://galaxy.ansible.com/api/v2/collections/paloaltonetworks/panos/&query=latest_version.version)

Ansible collection for easy automation of Palo Alto Networks next generation firewalls and Panorama, in both physical and virtual form factors.

Documentation: [https://paloaltonetworks.github.io/pan-os-ansible/](https://paloaltonetworks.github.io/pan-os-ansible/)

## About this project

- `paloaltonetworks.panos` is an open source project, maintained by the Palo Alto Networks Automation Consulting Engineering team and volunteers from Palo Alto Networks and the community.  We hope you will find it useful for daily automation needs and as the basis for projects of your own.
- There is **no support** through Palo Alto Networks TAC for these modules.  If you require a supported automation solution, please use the [official APIs](https://docs.paloaltonetworks.com/pan-os/10-0/pan-os-panorama-api.html).
- We are always interested in hearing how these modules are being used, and ways we can make them better.  Let us hear from you the the [GitHub Discussions forum](https://github.com/PaloAltoNetworks/pan-os-ansible/discussions)!
- We welcome contributions from the community!  [Here is how](https://github.com/PaloAltoNetworks/pan-os-ansible/wiki/Contributing) you can get started.

## Features

- Modify PAN-OS configuration: [interfaces](https://paloaltonetworks.github.io/pan-os-ansible/modules/panos_interface.html), [zones](https://paloaltonetworks.github.io/pan-os-ansible/modules/panos_zone.html#), [address objects](https://paloaltonetworks.github.io/pan-os-ansible/modules/panos_address_object.html), [service objects](https://paloaltonetworks.github.io/pan-os-ansible/modules/panos_service_object.html), [security rules](https://paloaltonetworks.github.io/pan-os-ansible/modules/panos_security_rule.html), [NAT rules](https://paloaltonetworks.github.io/pan-os-ansible/modules/panos_nat_rule.html).
- Perform operational commands: [check device status](https://paloaltonetworks.github.io/pan-os-ansible/modules/panos_check.html), [show interface statistics](https://paloaltonetworks.github.io/pan-os-ansible/modules/panos_op.html), [upgrade software](https://paloaltonetworks.github.io/pan-os-ansible/modules/panos_software.html), [perform dynamic updates](https://paloaltonetworks.github.io/pan-os-ansible/modules/panos_dynamic_updates.html).
- [Import](https://paloaltonetworks.github.io/pan-os-ansible/modules/panos_import.html) and [export](https://paloaltonetworks.github.io/pan-os-ansible/modules/panos_export.html): configuration, certificates, packet captures, response pages.

## Using this collection

### Requirements

The following libraries must be installed in your Python environment:

- [pan-os-python](https://github.com/PaloAltoNetworks/pan-os-python)
- [requests](https://docs.python-requests.org/en/master/)
- [xmltodict](https://github.com/martinblech/xmltodict)

Download the supplied [requirements.txt](https://github.com/PaloAltoNetworks/pan-os-ansible/blob/develop/requirements.txt) file and install using `pip`:

```
pip3 install —user -r requirements.txt
```

`pip` can also pull the requirements file directly from this repository:

`pip3 install —user https://github.com/PaloAltoNetworks/pan-os-ansible/blob/develop/requirements.txt`

### Installation

Use Ansible Galaxy to install this collection:

```bash
ansible-galaxy collection install paloaltonetworks.panos
```

## Sample Playbook


```yaml
—-
- hosts: fw
  connection: local
  
  collections:
    - paloaltonetworks.panos
    
  vars:
    device:
      ip_address: '192.168.1.1'
      username: 'admin'
      password: 'password'

  tasks:
    - name: Run show system info
      panos_op:
        provider: '{{ device }}'
        cmd: 'show system info'
      register: result

    - name: Display the result
      debug:
        msg: '{{ result.stdout }}'
      
```

For more examples, see the [ansible-playbooks](https://github.com/PaloAltoNetworks/ansible-playbooks) repository.

## Maintainers

- Michael Richardson ([@mrichardson03](https://github.com/mrichardson03))
- James Holland ([@jamesholland-uk](https://github.com/jamesholland-uk))

## Contributors

- Garfield Freeman ([@shinmog](https://github.com/shinmog))
- Nathan Embrey ([@nembery](https://github.com/nembery))