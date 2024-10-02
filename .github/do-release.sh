#!/usr/bin/env bash

ansible-galaxy collection build
ansible-galaxy collection publish paloaltonetworks-panos-* --server release_galaxy
ansible-galaxy collection publish paloaltonetworks-panos-* --server automation_hub
