# Integration Tests

## Setup

Test playbooks assume that firewalls have the following initial configuration:

- `ethernet1/1` in `untrust` zone
- `ethernet1/2` in `trust` zone
- DHCP management configuration

Add firewalls to `firewall` group in inventory, Panorama instances to
`panoramas` group (see `inventory.example`):

```
[firewalls]
panos-10        ip_address=192.168.55.10

[panoramas]
panorama-10     ip_address=192.168.55.5
```

Run the `setup.yml` playbook, which will wait until the PAN-OS device is fully
booted, and save a copy of the config into `blank.xml` on the device.

## Run Tests

### Run a single test

```
ansible-playbook -i inventory run_single_test.yml -e test=test_panos_address_object
```

### Run all tests

```
ansible-playbook -i inventory run_all_tests.yml
```

## Writing a test

`firewall/test_panos_address_object.yml` is a pretty basic example:

```yaml
---
- import_tasks: 'reset.yml'

- name: test_panos_address_object - Create
  panos_address_object:
    provider: '{{ device }}'
    name: 'Test-One'
    value: '1.1.1.1'
    description: 'Description One'
    device_group: '{{ device_group | default(omit) }}'
  register: result

- name: test_panos_address_object - Assert create was successful
  assert:
    that:
      - result is success
      - result is changed

- name: test_panos_address_object - Create (idempotence)
  panos_address_object:
    provider: '{{ device }}'
    name: 'Test-One'
    value: '1.1.1.1'
    description: 'Description One'
    device_group: '{{ device_group | default(omit) }}'
  register: result

- name: test_panos_address_object - Assert create (idempotence) was successful
  assert:
    that:
      - result is success
      - result is not changed

- name: test_panos_address_object - Modify
  panos_address_object:
    provider: '{{ device }}'
    name: 'Test-One'
    value: '2.2.2.2'
    device_group: '{{ device_group | default(omit) }}'
  register: result

- name: test_panos_address_object - Assert modify was successful
  assert:
    that:
      - result is success
      - result is changed

- name: test_panos_address_object - Delete
  panos_address_object:
    provider: '{{ device }}'
    name: 'Test-One'
    state: 'absent'
    device_group: '{{ device_group | default(omit) }}'
  register: result

- name: test_panos_address_object - Assert delete was successful
  assert:
    that:
      - result is success
      - result is changed

- name: test_panos_address_object - Make sure changes commit cleanly
  panos_commit:
    provider: '{{ device }}'
  register: result

- name: test_panos_address_object - Assert commit was successful
  assert:
    that:
      - result is success
```

First step is to reset the config to the initial `blank.xml` file using the
`reset.yml` playbook.

At a minimum, tests should:

- Create an element
- Create that same element over again (idempotence test)
- Modify an element
- Delete an element
- Make sure changes commit cleanly

Elements that belong in a device group should use the following:

```
device_group: '{{ device_group | default(omit) }}'
```

This will allow tests to easily be reused for Panorama instances, which will
define the `device_group` variable.  Similarly, tests for elements that can 
belong in a template should define the template option like this:

```
template: '{{ template | default(omit) }}'
```

The built-in Ansible module [assert](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/assert_module.html)
is used to check results.