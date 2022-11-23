#!/usr/bin/env bash

ansible-galaxy collection build
ansible-galaxy collection publish paloaltonetworks-panos-*
ansible-galaxy collection publish --server https://console.redhat.com/api/automation-hub/content/inbound-paloaltonetworks/ paloaltonetworks-panos-*