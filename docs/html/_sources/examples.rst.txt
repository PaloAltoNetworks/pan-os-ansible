========
Examples
========

**Note**: You can see complete examples [here](https://github.com/PaloAltoNetworks/ansible-pan/tree/master/examples)

Add security policy to Firewall or Panorama
===========================================

Security policies allow you to enforce rules and take action, and can
be as general or specific as needed. The policy rules are compared
against the incoming traffic in sequence, and because the first rule
that matches the traffic is applied, the more specific rules must
precede the more general ones.

Firewall
--------

.. code-block:: yaml

  - name: Add test rule 1 to the firewall
    panos_security_rule:
      provider: '{{ provider }}'
      rule_name: 'Ansible test 1'
      description: 'An Ansible test rule'
      source_zone: ['internal']
      destination_zone: ['external']
      source_ip: ['1.2.3.4']
      source_user: ['any']
      destination_ip: ['any']
      category: ['any']
      application: ['any']
      service: ['service-http']
      hip_profiles: ['any']
      action: 'allow'
      commit: 'False'


Panorama
--------

.. code-block:: yaml

  - name: Add test pre-rule to Panorama
    panos_security_rule:
      provider: '{{ provider }}'
      rule_name: 'Ansible test 1'
      description: 'An Ansible test pre-rule'
      source_zone: ['internal']
      destination_zone: ['external']
      source_ip: ['1.2.3.4']
      source_user: ['any']
      destination_ip: ['any']
      category: ['any']
      application: ['any']
      service: ['service-http']
      hip_profiles: ['any']
      action: 'allow'
      device_group: 'DeviceGroupA'
      commit: False


Add NAT policy to Firewall or Panorama
======================================

If you define Layer 3 interfaces on the firewall, you can configure a
Network Address Translation (NAT) policy to specify whether source or
destination IP addresses and ports are converted between public and
private addresses and ports. For example, private source addresses can
be translated to public addresses on traffic sent from an internal
(trusted) zone to a public (untrusted) zone. NAT is also supported on
virtual wire interfaces.

Firewall
--------

.. code-block:: yaml

  - name: Add the service object to the firewall first
    panos_service_object:
      provider: '{{ provider }}'
      name: 'service-tcp-221'
      protocol: 'tcp'
      destination_port: '221'
      description: 'SSH on port 221'
      commit: false

  - name: Create dynamic NAT rule on the firewall
    panos_nat_rule:
      provider: '{{ provider }}'
      rule_name: 'Web SSH inbound'
      source_zone: ['external']
      destination_zone: 'external'
      source_ip: ['any']
      destination_ip: ['10.0.0.100']
      service: 'service-tcp-221'
      snat_type: 'dynamic-ip-and-port'
      snat_interface: ['ethernet1/2']
      dnat_address: '10.0.1.101'
      dnat_port: '22'


Panorama
--------

.. code-block:: yaml

  - name: Add the necessary service object to Panorama first
    panos_object:
      provider: '{{ provider }}'
      name: 'service-tcp-221'
      protocol: 'tcp'
      destination_port: '221'
      description: 'SSH on port 221'
      commit: false
      device_group: 'shared_services_11022'

  - name: Create dynamic NAT rule on Panorama
    panos_nat_rule:
      provider: '{{ provider }}'
      rule_name: 'Web SSH inbound'
      source_zone: ['external']
      destination_zone: 'external'
      source_ip: ['any']
      destination_ip: ['10.0.0.100']
      service: 'service-tcp-221'
      snat_type: 'dynamic-ip-and-port'
      snat_interface: ['ethernet1/2']
      dnat_address: '10.0.1.101'
      dnat_port: '22'
      device_group: 'shared_services_11022'

Change firewall admin password using SSH
========================================

Change admin password of PAN-OS device using SSH with SSH key. This is
used in particular when NGFW is deployed in the cloud (such as AWS).

.. code-block:: yaml

  - name: Change user password using ssh protocol
    panos_admpwd:
      ip_address: '{{ ip_address }}'
      password: '{{ password }}'
      newpassword: '{{ new_password }}'
      key_filename: '{{ key_filename }}'


Generates self-signed certificate
=================================

This module generates a self-signed certificate that can be used by
GlobalProtect client, SSL connector, or otherwise. Root certificate
must be preset on the system first. This module depends on paramiko
for ssh.

.. code-block:: yaml

  - name: generate self signed certificate
    panos_cert_gen_ssh:
      ip_address: "{{ ip_address }}"
      username: "{{ username }}"
      password: "{{ password }}"
      cert_cn: "{{ cn }}"
      cert_friendly_name: "{{ friendly_name }}"
      signed_by: "{{ signed_by }}"


Check if FW is ready
====================

Check if PAN-OS device is ready for being configured (no pending
jobs). The check could be done once or multiple times until the device
is ready.

.. code-block:: yaml

  - name: Wait for FW reboot
    panos_check:
      provider: '{{ provider }}'
    register: result
    until: not result|failed
    retries: 50
    delay: 5


Import configuration
====================

Import file into PAN-OS device.

.. code-block:: yaml

    - name: import configuration file into PAN-OS
      panos_import:
        ip_address: "{{ ip_address }}"
        username: "{{ username }}"
        password: "{{ password }}"
        file: "{{ config_file }}"
        category: "configuration"


DHCP on data port
=================

Configure data-port (DP) network interface for DHCP. By default DP
interfaces are static.

.. code-block:: yaml

    - name: enable DHCP client on ethernet1/1 in zone external
      panos_interface:
        provider: '{{ provider }}'
        if_name: "ethernet1/1"
        zone_name: "external"
        create_default_route: "yes"
        commit: False


Load configuration
==================

This is example playbook that imports and loads firewall
configuration from a configuration file

.. code-block:: yaml

    - name: import config
      hosts: my-firewall
      connection: local
      gather_facts: False

      vars:
        cfg_file: candidate-template-empty.xml

      roles:
        - role: PaloAltoNetworks.paloaltonetworks

      tasks:
      - name: Grab the credentials from ansible-vault
        include_vars: 'firewall-secrets.yml'
        no_log: 'yes'

      - name: wait for SSH (timeout 10min)
        wait_for: port=22 host='{{ provider.ip_address }}' search_regex=SSH timeout=600

      - name: checking if device ready
        panos_check:
          provider: '{{ provider }}'
        register: result
        until: not result|failed
        retries: 10
        delay: 10

      - name: import configuration
        panos_import:
          ip_address: '{{ provider.ip_address }}'
          username: '{{ provider.username }}'
          password: '{{ provider.password }}'
          file: '{{cfg_file}}'
          category: 'configuration'
        register: result

      - name: load configuration
        panos_loadcfg:
          ip_address: '{{ provider.ip_address }}'
          username: '{{ provider.username }}'
          password: '{{ provider.password }}'
          file: '{{result.filename}}'
          commit: False

      - name: set admin password
        panos_administrator:
          provider: '{{ provider }}'
          admin_username: 'admin'
          admin_password: '{{ provider.password }}'
          superuser: True
          commit: False

      - name: commit (blocks until finished)
        panos_commit:
          provider: '{{ provider }}'
