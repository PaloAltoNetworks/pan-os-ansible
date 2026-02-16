#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2017 Palo Alto Networks, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: panos_security_rule
short_description: Manage security rule policy on PAN-OS devices or Panorama management console.
description: >
    Following rules apply for security policies:

        - Security policies allow you to enforce rules and take action, and can be as
        general or specific as needed.

        - The policy rules are compared against the incoming traffic in sequence, and
        because the first rule that matches the traffic is applied, the more specific
        rules must precede the more general ones.

        - Defaults in spec descriptions apply when I(state=present)/I(state=replaced),
        or when creating a new resource with I(state=merged).
author:
    - Ivan Bojer (@ivanbojer)
    - Robert Hagen (@stealthllama)
    - Michael Richardson (@mrichardson03)
    - Garfield Lee Freeman (@shinmog)
    - Alp Eren Kose (@alperenkose)
version_added: '1.0.0'
requirements:
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is supported.
    - Panorama is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
    - paloaltonetworks.panos.fragments.device_group
    - paloaltonetworks.panos.fragments.vsys
    - paloaltonetworks.panos.fragments.rulebase
    - paloaltonetworks.panos.fragments.deprecated_commit
    - paloaltonetworks.panos.fragments.uuid
    - paloaltonetworks.panos.fragments.target
    - paloaltonetworks.panos.fragments.movement
    - paloaltonetworks.panos.fragments.audit_comment
options:
    rule_name:
        description:
            - Name of the security rule.
        type: str
    source_zone:
        description:
            - List of source zones. Defaults to I(["any"]).
        type: list
        elements: str
    source_ip:
        description:
            - List of source addresses. Defaults to I(["any"]).
            - This can be an IP address, an address object/group, etc.
            - When referencing predefined EDLs, use config names of the EDLS not
              their full names. The config names can be found with the CLI...
              request system external-list show type predefined-ip name <tab>
                panw-bulletproof-ip-list   panw-bulletproof-ip-list
                panw-highrisk-ip-list      panw-highrisk-ip-list
                panw-known-ip-list         panw-known-ip-list
                panw-torexit-ip-list       panw-torexit-ip-list
        type: list
        elements: str
    source_user:
        description:
            - Use users to enforce policy for individual users or a group of users.
              Defaults to I(["any"]).
        type: list
        elements: str
    hip_profiles:
        description:
            - If you are using GlobalProtect with host information profile (HIP)
              enabled, you can also base the policy on information collected by
              GlobalProtect. For example, the user access level can be determined
              HIP that notifies the firewall about the user's local configuration.
            - NOTE If I(state=present) or I(state=replaced), and you're running
              PAN-OS < 10.0.0, then this will have a default of I(["any"]).
            - If you are using PAN-OS >= 10.0.0, please do not use this
              parameter as it was removed from PAN-OS in 10.0.0.
        type: list
        elements: str
    destination_zone:
        description:
            - List of destination zones. Defaults to I(["any"]).
        type: list
        elements: str
    destination_ip:
        description:
            - List of destination addresses. Defaults to I(["any"]).
            - This can be an IP address, an address object/group, etc.
            - When referencing predefined EDLs, use config names of the EDLS not
              their full names. The config names can be found with the CLI...
              request system external-list show type predefined-ip name <tab>
                panw-bulletproof-ip-list   panw-bulletproof-ip-list
                panw-highrisk-ip-list      panw-highrisk-ip-list
                panw-known-ip-list         panw-known-ip-list
                panw-torexit-ip-list       panw-torexit-ip-list
        type: list
        elements: str
    application:
        description:
            - List of applications, application groups, and/or application filters.
              Defaults to I(["any"]).
        type: list
        elements: str
    service:
        description:
            - List of services and/or service groups. Defaults to I(["application-default"]).
        type: list
        elements: str
    category:
        description:
            - List of destination URL categories. Defaults to I(["any"]).
            - When referencing predefined EDLs, use config names of the EDLS not
              their full names. The config names can be found with the CLI...
              request system external-list show type predefined-url name <tab>
                panw-auth-portal-exclude-list   panw-auth-portal-exclude-list
        type: list
        elements: str
    action:
        description:
            - Action to apply to the rule. Defaults to I("allow").
        type: str
        choices:
            - allow
            - deny
            - drop
            - reset-client
            - reset-server
            - reset-both
    log_setting:
        description:
            - Log forwarding profile.
        type: str
    log_start:
        description:
            - Whether to log at session start. Defaults to I(false).
        type: bool
    log_end:
        description:
            - Whether to log at session end. Defaults to I(true).
        type: bool
    description:
        description:
            - Description of the security rule.
        type: str
    rule_type:
        description:
            - Type of security rule (version 6.1 of PanOS and above). Defaults to I("universal").
        type: str
        choices:
            - universal
            - intrazone
            - interzone
    tag_name:
        description:
            - List of tags associated with the rule.
        type: list
        elements: str
    negate_source:
        description:
            - Match on the reverse of the 'source_ip' attribute. Defaults to I(false).
        type: bool
    negate_destination:
        description:
            - Match on the reverse of the 'destination_ip' attribute. Defaults to I(false).
        type: bool
    disabled:
        description:
            - Disable this rule. Defaults to I(false).
        type: bool
    schedule:
        description:
            - Schedule in which this rule is active.
        type: str
    icmp_unreachable:
        description:
            - Send 'ICMP Unreachable'. Used with 'deny', 'drop', and 'reset' actions.
        type: bool
    disable_server_response_inspection:
        description:
            - Disables packet inspection from the server to the client. Useful under heavy server load conditions.
              Defaults to I(false).
        type: bool
    group_profile:
        description:
            - Security profile group that is already defined in the system. This property supersedes antivirus,
              vulnerability, spyware, url_filtering, file_blocking, data_filtering, and wildfire_analysis properties.
        type: str
    antivirus:
        description:
            - Name of the already defined antivirus profile.
        type: str
    vulnerability:
        description:
            - Name of the already defined vulnerability profile.
        type: str
    spyware:
        description:
            - Name of the already defined spyware profile.
        type: str
    url_filtering:
        description:
            - Name of the already defined url_filtering profile.
        type: str
    file_blocking:
        description:
            - Name of the already defined file_blocking profile.
        type: str
    data_filtering:
        description:
            - Name of the already defined data_filtering profile.
        type: str
    wildfire_analysis:
        description:
            - Name of the already defined wildfire_analysis profile.
        type: str
    devicegroup:
        description:
            - B(Deprecated)
            - Use I(device_group) instead.
            - HORIZONTALLINE
            - Device groups are logical groups of firewalls in Panorama.
        type: str
    group_tag:
        description:
            - The group tag.
        type: str
"""

EXAMPLES = """
- name: add SSH inbound rule to Panorama device group
  paloaltonetworks.panos.panos_security_rule:
    provider: '{{ provider }}'
    device_group: 'Cloud Edge'
    rule_name: 'SSH permit'
    description: 'SSH rule test'
    tag_name: ['production']
    source_zone: ['public']
    source_ip: ['any']
    destination_zone: ['private']
    destination_ip: ['1.1.1.1']
    application: ['ssh']
    action: 'allow'

- name: add a rule to allow HTTP multimedia only to CDNs
  paloaltonetworks.panos.panos_security_rule:
    provider: '{{ provider }}'
    rule_name: 'HTTP Multimedia'
    description: 'Allow HTTP multimedia only to host at 1.1.1.1'
    source_zone: ['private']
    destination_zone: ['public']
    category: ['content-delivery-networks']
    application: ['http-video', 'http-audio']
    service: ['service-http', 'service-https']
    action: 'allow'

- name: add a more complex rule that uses security profiles
  paloaltonetworks.panos.panos_security_rule:
    provider: '{{ provider }}'
    rule_name: 'Allow HTTP'
    source_zone: ['public']
    destination_zone: ['private']
    log_start: false
    log_end: true
    action: 'allow'
    antivirus: 'strict'
    vulnerability: 'strict'
    spyware: 'strict'
    url_filtering: 'strict'
    wildfire_analysis: 'default'

- name: disable a Panorama pre-rule
  paloaltonetworks.panos.panos_security_rule:
    provider: '{{ provider }}'
    device_group: 'Production edge'
    rule_name: 'Allow telnet'
    source_zone: ['public']
    destination_zone: ['private']
    source_ip: ['any']
    destination_ip: ['1.1.1.1']
    log_start: false
    log_end: true
    action: 'allow'
    disabled: true

- name: delete a device group security rule
  paloaltonetworks.panos.panos_security_rule:
    provider: '{{ provider }}'
    state: 'absent'
    device_group: 'DC Firewalls'
    rule_name: 'Allow telnet'

- name: add a rule at a specific location in the rulebase
  paloaltonetworks.panos.panos_security_rule:
    provider: '{{ provider }}'
    rule_name: 'SSH permit'
    description: 'SSH rule test'
    source_zone: ['untrust']
    destination_zone: ['trust']
    source_ip: ['any']
    source_user: ['any']
    destination_ip: ['1.1.1.1']
    category: ['any']
    application: ['ssh']
    service: ['application-default']
    action: 'allow'
    location: 'before'
    existing_rule: 'Allow MySQL'
"""

RETURN = """
# Default return values
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    ConnectionHelper,
    get_connection,
)


class Helper(ConnectionHelper):
    def initial_handling(self, module):
        # TODO(gfreeman) - remove when devicegroup is removed.
        if module.params["devicegroup"] is not None:
            module.deprecate(
                'Param "devicegroup" is deprecated; use "device_group"',
                version="4.0.0",
                collection_name="paloaltonetworks.panos",
            )
            if module.params["device_group"] is not None:
                msg = [
                    'Both "devicegroup" and "device_group" are specified',
                    "Specify one or the other, not both.",
                ]
                module.fail_json(msg=". ".join(msg))
            module.params["device_group"] = module.params["devicegroup"]

    def spec_handling(self, spec, module):
        if module.params["state"] not in ("present", "replaced"):
            return

        # The hip-profiles was removed somewhere in PAN-OS v10, either
        # v10.1.5 or before (one user says it's gone for them in v10.0.0),
        # and it is gone in pan-os-python, but the Ansible collection needs
        # to have some extra code so as to maintain functionality (read:
        # default values) for uses who are running older PAN-OS versions so
        # as to not create regressions in their automation.
        if self.device._version_info < (10, 0, 0) and spec["hip_profiles"] is None:
            spec["hip_profiles"] = [
                "any",
            ]


def main():
    helper = get_connection(
        helper_cls=Helper,
        vsys=True,
        device_group=True,
        rulebase=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        with_classic_provider_spec=True,
        error_on_firewall_shared=True,
        min_pandevice_version=(1, 5, 0),
        with_uuid=True,
        with_commit=True,
        with_target=True,
        with_movement=True,
        with_audit_comment=True,
        sdk_cls=("policies", "SecurityRule"),
        sdk_params=dict(
            rule_name=dict(required=True, sdk_param="name"),
            source_zone=dict(type="list", elements="str", sdk_param="fromzone"),
            source_ip=dict(type="list", elements="str", sdk_param="source"),
            source_user=dict(type="list", elements="str"),
            hip_profiles=dict(type="list", elements="str"),
            destination_zone=dict(type="list", elements="str", sdk_param="tozone"),
            destination_ip=dict(type="list", elements="str", sdk_param="destination"),
            application=dict(type="list", elements="str"),
            service=dict(type="list", elements="str"),
            category=dict(type="list", elements="str"),
            action=dict(
                choices=[
                    "allow",
                    "deny",
                    "drop",
                    "reset-client",
                    "reset-server",
                    "reset-both",
                ],
            ),
            log_setting=dict(),
            log_start=dict(type="bool"),
            log_end=dict(type="bool"),
            description=dict(),
            rule_type=dict(
                choices=["universal", "intrazone", "interzone"],
                sdk_param="type",
            ),
            tag_name=dict(type="list", elements="str", sdk_param="tag"),
            negate_source=dict(type="bool"),
            negate_destination=dict(type="bool"),
            disabled=dict(type="bool"),
            schedule=dict(),
            icmp_unreachable=dict(type="bool"),
            disable_server_response_inspection=dict(type="bool"),
            group_profile=dict(sdk_param="group"),
            antivirus=dict(sdk_param="virus"),
            spyware=dict(),
            vulnerability=dict(),
            url_filtering=dict(),
            file_blocking=dict(),
            wildfire_analysis=dict(),
            data_filtering=dict(),
            group_tag=dict(),
        ),
        extra_params=dict(
            # TODO(gfreeman) - remove this in the next role release.
            devicegroup=dict(),
        ),
        default_values=dict(
            source_zone=["any"],
            source_ip=["any"],
            source_user=["any"],
            destination_zone=["any"],
            destination_ip=["any"],
            application=["any"],
            service=["application-default"],
            category=["any"],
            action="allow",
            log_start=False,
            log_end=True,
            rule_type="universal",
            negate_source=False,
            negate_destination=False,
            disabled=False,
            disable_server_response_inspection=False,
        ),
        preset_values=dict(
            source_zone=["any"],
            source_ip=["any"],
            source_user=["any", "pre-logon", "known-user", "unknown"],
            destination_zone=["any", "multicast"],
            destination_ip=["any"],
            application=["any"],
            service=["application-default", "any"],
            category=["any"],
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    helper.process(module)


if __name__ == "__main__":
    main()
