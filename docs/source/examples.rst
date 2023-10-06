========
Examples
========

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
    paloaltonetworks.panos.panos_security_rule:
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
    paloaltonetworks.panos.panos_security_rule:
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
    paloaltonetworks.panos.panos_service_object:
      provider: '{{ provider }}'
      name: 'service-tcp-221'
      protocol: 'tcp'
      destination_port: '221'
      description: 'SSH on port 221'
      commit: false

  - name: Create dynamic NAT rule on the firewall
    paloaltonetworks.panos.panos_nat_rule:
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
    paloaltonetworks.panos.panos_object:
      provider: '{{ provider }}'
      name: 'service-tcp-221'
      protocol: 'tcp'
      destination_port: '221'
      description: 'SSH on port 221'
      commit: false
      device_group: 'shared_services_11022'

  - name: Create dynamic NAT rule on Panorama
    paloaltonetworks.panos.panos_nat_rule:
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
    paloaltonetworks.panos.panos_admpwd:
      ip_address: '{{ ip_address }}'
      username: '{{ username }}'
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
    paloaltonetworks.panos.panos_cert_gen_ssh:
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
    paloaltonetworks.panos.panos_check:
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
      paloaltonetworks.panos.panos_import:
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
      paloaltonetworks.panos.panos_interface:
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
        paloaltonetworks.panos.panos_check:
          provider: '{{ provider }}'
        register: result
        until: not result|failed
        retries: 10
        delay: 10

      - name: import configuration
        paloaltonetworks.panos.panos_import:
          ip_address: '{{ provider.ip_address }}'
          username: '{{ provider.username }}'
          password: '{{ provider.password }}'
          file: '{{cfg_file}}'
          category: 'configuration'
        register: result

      - name: load configuration
        paloaltonetworks.panos.panos_loadcfg:
          ip_address: '{{ provider.ip_address }}'
          username: '{{ provider.username }}'
          password: '{{ provider.password }}'
          file: '{{result.filename}}'
          commit: False

      - name: set admin password
        paloaltonetworks.panos.panos_administrator:
          provider: '{{ provider }}'
          admin_username: 'admin'
          admin_password: '{{ provider.password }}'
          superuser: True
          commit: False

      - name: commit (blocks until finished)
        paloaltonetworks.panos.panos_commit:
          provider: '{{ provider }}'

Event-Driven Ansible (EDA)
===========================================

Event-Driven Ansible is a responsive automation solution that can
process events containing discrete, actionable intelligence.
The `extensions/plugins/event_source/logs.py` plugin is capable of
receiving JSON structured messages from a PAN-OS firewall, restructures
the payload as a Python dictionary, determines the appropriate response
to the event, and then executes automated actions to address or remediate
based on the situation.

There are four components needed to implement this example EDA use case
with PAN-OS:

- HTTP server profile: A PAN-OS firewall configuration that defines
  how the PAN-OS firewall(s) should send events to the EDA server.
- EDA rulebook: A YAML file which describes events of interest, and how to
  EDA respond to them based on conditions.
- Inventory: A YAML file that defines the PAN-OS firewall(s) to be
  executed against when a condition is met.
- Ansible playbook: A YAML file that defines the Ansible tasks to be executed
  when a condition is met.

The four components are described here in the context of a use case of
detecting decryption issues based on the Decryption Logs, and responding
by placing the relevant URLs into a category used for decryption bypass.

HTTP Server Profile
-------------------

The following example shows what a Decryption HTTP server profile
would look like in PAN-OS. The HTTP server profile is configured to
send logs to the EDA server.

.. code-block:: json

    {
        "category": "network",
        "details": {
            "action": "$action",
            "app": "$app",
            "cn": "$cn",
            "dst": "$dst",
            "device_name": "$device_name",
            "error": "$error",
            "issuer_cn": "$issuer_cn",
            "root_cn": "$root_cn",
            "root_status": "$root_status",
            "sni": "$sni",
            "src": "$src",
            "srcuser": "$srcuser"
        },
        "receive_time": "$receive_time",
        "rule": "$rule",
        "rule_uuid": "$rule_uuid",
        "serial": "$serial",
        "sessionid": "$sessionid",
        "severity": "informational",
        "type": "decryption"
    }

This HTTP Server Profile could be configured in its entirety using the
following tasks in an Ansible playbook:

.. code-block:: yaml

    - name: Create a HTTP Server Profile for Decryption Logs
      paloaltonetworks.panos.panos_http_profile:
        provider: '{{ device }}'
        name: '{{ server_profile_name_decrypt }}'
        decryption_name: 'decryption-logs-to-eda'
        decryption_uri_format: 'https://test'
        decryption_payload: >
          {
              "category": "network",
              "details": {
                  "action": "$action",
                  "app": "$app",
                  "cn": "$cn",
                  "dst": "$dst",
                  "device_name": "$device_name",
                  "error": "$error",
                  "issuer_cn": "$issuer_cn",
                  "root_cn": "$root_cn",
                  "root_status": "$root_status",
                  "sni": "$sni",
                  "src": "$src",
                  "srcuser": "$srcuser"
              },
              "receive_time": "$receive_time",
              "rule": "$rule",
              "rule_uuid": "$rule_uuid",
              "serial": "$serial",
              "sessionid": "$sessionid",
              "severity": "informational",
              "type": "decryption"
          }

    - name: Create HTTP server
      paloaltonetworks.panos.panos_http_server:
        provider: '{{ device }}'
        http_profile: '{{ server_profile_name_decrypt }}'
        name: 'my-EDA-server'
        address: '192.168.1.5'
        http_method: 'GET'
        http_port: 5000

    - name: Add a HTTP header to HTTP Server Profile
      paloaltonetworks.panos.panos_http_profile_header:
        provider: '{{ device }}'
        http_profile: '{{ server_profile_name_decrypt }}'
        log_type: 'decryption'
        header: 'Content-Type'
        value: 'application/json'

    - name: Add a param to the config log type
      paloaltonetworks.panos.panos_http_profile_param:
        provider: '{{ device }}'
        http_profile: '{{ server_profile_name_decrypt }}'
        log_type: 'decryption'
        param: 'serial'
        value: '$serial'

The HTTP Server Profile would be used in a Log Forwarding Profile
with a filter for only forwarding Decryption Logs when there has
been an issue with decryption. Here are example Ansible tasks to
create a Log Forwarding Profile:

.. code-block:: yaml

    - name: Create log forwarding profile
      paloaltonetworks.panos.panos_log_forwarding_profile:
        provider: '{{ provider }}'
        name: 'EDA_LFP'
        enhanced_logging: true

    - name: Create log forwarding profile match list
      paloaltonetworks.panos.panos_log_forwarding_profile_match_list:
        provider: '{{ provider }}'
        log_forwarding_profile: 'EDA_LFP'
        name: 'eda-decryption-forwarding'
        log_type: 'decryption'
        filter: '( err_index neq None ) and ( proxy_type eq Forward )'
        http_profiles: ['{{ server_profile_name_decrypt }}']


Rulebook - rulebook.yml
-----------------------

This rulebook shows an example of how to configure EDA to receive
the decryption logs from PAN-OS, and execute a remediation playbook:

.. code-block:: yaml

    ---
    - name: "Receive logs sourced from HTTP Server Profile in PAN-OS"
      hosts: "localhost"

      ## Define how our plugin should listen for logs from PAN-OS
      sources:
        - paloaltonetworks.panos.logs:
            host: 0.0.0.0
            port: 5000
            type: decryption

      ## Define the conditions we are looking for. There are many types of logs
      ## in PAN-OS; we are looking just for decryption logs
      rules:
        - name: "Troubleshoot Decryption Failure"
          condition: event.meta.log_type == "decryption"

          ## Define the action we should take should the condition be met,
          ## when we find a decryption log, which is to execute the 
          ## remediation playbook
          action:
            run_playbook:
              name: "playbooks/decryption_remediation.yml"



Inventory
---------

The inventory for this example use case is one that defines all hosts
(firewalls) to be local connectivity, as this is how Ansible communicates
with PAN-OS:

.. code-block:: yaml

    all:
      hosts:
        localhost:
          ansible_connection: local



Playbook - decryption_remediation.yml
-------------------------------------

The playbook executed when the conditions in the rulebook are met, in
this example use case, performs tasks to add the relevant URL into a
category used to bypass decryption, thus remediating the problem:

.. code-block:: yaml

    ---
    - name: Decryption Remediation Playbook
      hosts: 'all'
      gather_facts: false
      connection: local

      vars:
        device:
          ip_address: "192.168.1.10"
          username: "admin"
          password: "redacted"

        bypass_category_name: 'decryption-bypass'


      ## When EDA calls this playbook for execution, it takes the SNI (Server Name Indication)
      ## from the decryption logs where a site failed to be decrypted properly, and adds the
      ## SNI to the list of domains in a URL category. This URL category is used as match
      ## criteria, therefore domains in this URL category will no longer be decrypted by the
      ## decryption policy rule.

      tasks:
        ## Gather up the list of domains currently in the URL category
        - name: Get current decryption bypass domains
          paloaltonetworks.panos.panos_custom_url_category:
            provider: "{{ device }}"
            state: "gathered"
            gathered_filter: "name == '{{ bypass_category_name }}'"
          register: bypass_category

        ## If the URL category already has some domains, add this SNI to the list ('url_value')
        - name: Update decryption bypass category with new domain, if category is currently not empty
          paloaltonetworks.panos.panos_custom_url_category:
            provider: '{{ device }}'
            name: '{{ bypass_category_name }}'
            url_value: '{{ bypass_category.gathered[0].url_value + [ansible_eda.event.payload.details.sni] }}'
          when:
            - bypass_category.gathered[0].url_value != None
            - ansible_eda.event.payload.details.sni not in bypass_category.gathered[0].url_value

        ## If the URL category is empty, create the list ('url_value') with this SNI
        - name: Create decryption bypass category with new domain, if category is currently empty
          paloaltonetworks.panos.panos_custom_url_category:
            provider: '{{ device }}'
            name: '{{ bypass_category_name }}'
            url_value: '{{ [ansible_eda.event.payload.details.sni] }}'
          when:
            - bypass_category.gathered[0].url_value == None

        ## Having added the site's SNI to the URL category, make this change live by performing a 'commit'
        - name: Commit configuration
          paloaltonetworks.panos.panos_commit_firewall:
            provider: "{{ device }}"
          register: results

        ## Output results of the commit
        - name: Output commit results
          ansible.builtin.debug:
            msg: "Commit with Job ID: {{ results.jobid }} had output: {{ results }}"

An alternative remediation if the web server hosting the URL is not presenting
the relevant intermediate certificate, would be to add the intermediate
certificate into the PAN-OS certificate store, and not use a bypass (which weakens
visibility by leaving more traffic encrypted) like the previous example:

.. code-block:: yaml

  tasks:
    - name: Get intermediate certificate URL
      ansible.builtin.set_fact:
        intermediate_cert_url: "{{ ansible_eda.event.payload.details.error | regex_search(regex_query, ignorecase=True) }}"
      vars:
        regex_query: '(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'

    - name: Get intermediate certificate filename
      ansible.builtin.set_fact:
        intermediate_cert_name: "{{ intermediate_cert_url | regex_search(regex_query, ignorecase=True) }}"
      vars:
        regex_query: '[^\/\\&\?]+\.\w{3,4}(?=([\?&].*$|$))'

    - name: Download intermediate certificate
      ansible.builtin.get_url:
        url: '{{ intermediate_cert_url }}'
        dest: '{{ intermediate_cert_name }}'

    - name: Convert intermediate certificate from DER format to PEM format
      ansible.builtin.command: openssl x509 -inform DER -outform PEM -in {{ intermediate_cert_name }} -out {{ intermediate_cert_name }}.pem
      register: output
      changed_when: output.rc != 0

    - name: Import intermediate certificate to NGFW
      paloaltonetworks.panos.panos_import:
        provider: '{{ device }}'
        category: 'certificate'
        certificate_name: '{{ intermediate_cert_name }}'
        format: 'pem'
        filename: '{{ intermediate_cert_name }}.pem'
