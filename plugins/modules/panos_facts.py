#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Tomi Raittinen <tomi.raittinen@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: panos_facts
short_description: Collects facts from Palo Alto Networks device
description:
    - Collects fact information from Palo Alto Networks firewall running PanOS.
author:
    - Tomi Raittinen (@traittinen)
    - Garfield Lee Freeman (@shinmog)
notes:
    - Tested on PanOS 8.0.5
    - Checkmode is not supported.
    - Panorama is not supported.
requirements:
    - pan-python
version_added: 2.8
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
options:
    host:
        description:
            - B(Removed)
            - Use I(provider) instead.
    gather_subset:
        description:
            - Scopes what information is gathered from the device.
              Possible values for this argument include all, system, session,
              interfaces, ha, routing, vr, vsys and config. You can specify a
              list of values to include a larger subset. Values can also be used
              with an initial ! to specify that a specific subset should not be
              collected. Certain subsets might be supported by Panorama.
        required: false
        default: ['!config']
'''

EXAMPLES = '''
# Gather facts
- name: Get facts
  panos_facts:
    provider: '{{ provider }}'
    gather_subset: ['config']
'''

RETURN = '''
ansible_net_hostname:
    description: Hostname of the local node.
    returned: When C(system) is specified in C(gather_subset).
    type: str
ansible_net_serial:
    description: Serial number of the local node.
    returned: When C(system) is specified in C(gather_subset).
    type: str
ansible_net_model:
    description: Device model of the local node.
    returned: When C(system) is specified in C(gather_subset).
    type: str
ansible_net_version:
    description: PanOS version of the local node.
    returned: When C(system) is specified in C(gather_subset).
    type: str
ansible_net_uptime:
    description: Uptime of the local node.
    returned: When C(system) is specified in C(gather_subset).
    type: str
    sample: 469 days, 19:30:16
ansible_net_full_commit_required:
    description: Specifies whether full commit is required to apply changes.
    returned: When C(system) is specified in C(gather_subset).
    type: bool
ansible_net_uncommitted_changes:
    description: Specifies if commit is required to apply changes.
    returned: When C(system) is specified in C(gather_subset).
    type: bool
ansible_net_multivsys:
    description: Specifies whether multivsys mode is enabled on local node.
    returned: When C(system) is specified in C(gather_subset).
    type: str
    sample: on
ansible_net_session_usage:
    description: Current number of active sessions on local node
    returned: When C(session) is specified in C(gather_subset).
    type: int
ansible_net_session_max:
    description: Maximum number of sessions on local node.
    returned: When C(session) is specified in C(gather_subset).
    type: int
ansible_net_pps:
    description: Current packets/s throughput.
    returned: When C(session) is specified in C(gather_subset).
    type: int
ansible_net_kbps:
    description: Current kb/s throughput.
    returned: When C(session) is specified in C(gather_subset).
    type: int
ansible_net_ha_enabled:
    description: Specifies whether HA is enabled or not.
    returned: When C(ha) is specified in C(gather_subset).
    type: bool
ansible_net_ha_localmode:
    description: Specifies the HA mode on local node.
    returned: When C(ha) is specified in C(gather_subset).
    type: str
    sample: Active-Passive
ansible_net_ha_localstate:
    description: Specifies the HA state on local node.
    returned: When C(ha) is specified in C(gather_subset).
    type: str
    sample: active
ansible_net_config:
    description: Device confiration in XML format.
    returned: When C(config) is specified in C(gather_subset).
    type: str
ansible_net_interfaces:
    description: Network interface information.
    returned: When C(interface) is specified in C(gather_subset).
    type: complex
    contains:
        name:
            description: Interface name.
            type: str
            sample: ae1.23
        comment:
            description: Interface description/comment.
            type: str
        ip:
            description: List of interface IP addresses in CIDR format.
            type: list
            sample: 192.0.2.1/24
        ipv6:
            description: List of interface IPv6 addresses in CIDR format.
            type: list
            sample: 2001:db8::0000:1/64
        tag:
            description: VLAN tag for the subinterface.
            type: int
            sample: 23
ansible_net_virtual_routers:
    description: Virtual Router information.
    returned: When C(vr) is specified in C(gather_subset).
    type: complex
    contains:
        vr_name:
            description: Name of the virtual router.
            type: str
        vr_routerid:
            description: BGP router ID.
            type: str
            sample: 192.0.2.1
        vr_asn:
            description: BGP autonomous system number.
            type: int
            sample: 65001
        vr_iflist:
            description: List interfaces in the VR.
            type: list
            sample:
                - ae2.12
                - ae2.14
ansible_net_virtual_systems:
    description: Virtual System information.
    returned: When C(vsys) is specified in C(gather_subset).
    type: complex
    contains:
        vsys_description:
            description: VSYS description/name.
            type: str
        vsys_id:
            description: VSYS ID.
            type: int
        vsys_name:
            description: VSYS name.
            type: int
            sample: vsys1
        vsys_currentsessions:
            description: Number of active sessions on VSYS.
            type: int
        vsys_vsys_maxsessions:
            description: Number of configured maximum sessions on VSYS. 0 for unlimited.
            type: int
        vsys_vrlist:
            description: List of virtual routers attached to the VSYS.
            type: list
        vsys_iflist:
            description: List of interfaces attached to the VSYS.
            type: list
        vsys_zonelist:
            description: List of security zones attached to the VSYS.
            type: list
ansible_net_routing_table:
    description: Routing Table information.
    returned: When C(routing) is specified in C(gather_subset).
    type: complex
    contains:
        age:
            description: Age of the route entry in the routing table.
            type: str
        destination:
            description: IP prefix of the destination.
            type: str
        flags:
            description: Flags for the route entry in the routing table.
            type: str
        interface:
            description: Egress interface the router will use to reach the next hop.
            type: str
        metric:
            description: Metric for the route.
            type: str
        nexthop:
            description: Address of the device at the next hop toward the destination network.
            type: str
        route_table:
            description: Unicast or multicast route table.
            type: str
        virtual_router:
            description: Virtual router the route belongs to.
            type: str
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection
from ansible.module_utils.six import iteritems


try:
    from pandevice.device import Vsys
    from pandevice.errors import PanDeviceError
    from pandevice.network import AggregateInterface
    from pandevice.network import EthernetInterface
    from pandevice.network import Layer3Subinterface
    from pandevice.network import Layer2Subinterface
    from pandevice.network import IPv6Address
    from pandevice.network import VlanInterface
    from pandevice.network import LoopbackInterface
    from pandevice.network import TunnelInterface
    from pandevice.network import VirtualRouter
    from pandevice.network import Bgp
    from pandevice.network import Zone
except ImportError:
    pass


class Factbase(object):
    def __init__(self, module, parent):
        self.module = module
        self.parent = parent

        self.facts = dict()


class System(Factbase):
    def populate_facts(self):
        xapi = self.parent
        root = xapi.op('show system info').find('./result/system')

        self.facts.update({
            'hostname': root.findtext('hostname'),
            'model': root.findtext('model'),
            'serial': root.findtext('serial'),
            'version': root.findtext('sw-version'),
            'uptime': root.findtext('uptime'),
            'multivsys': root.findtext('multi-vsys')
        })

        # Check uncommitted changes
        result = xapi.op('check pending-changes').find('./result').text

        if result == "yes":
            uncommitted_changes = True
        else:
            uncommitted_changes = False

        # Check if full commit is required
        if uncommitted_changes:
            result = xapi.op('check full-commit-required').find('./result').text

            if result == "yes":
                full_commit_required = True
            else:
                full_commit_required = False
        else:
            full_commit_required = False

        self.facts.update({
            'uncommitted_changes': uncommitted_changes,
            'full_commit_required': full_commit_required
        })


class Session(Factbase):
    def populate_facts(self):
        root = self.parent.op('show session info')

        self.facts.update({
            'session_usage': root.find('./result/num-active').text,
            'session_max': root.find('./result/num-max').text,
            'pps': root.find('./result/pps').text,
            'kbps': root.find('./result/kbps').text
        })


class Routing(Factbase):
    def populate_facts(self):
        entries = self.parent.op('show routing route').findall('./result/entry')
        routing_table = [
            {route.tag.replace('-', '_'): route.text for route in entry}
            for entry in entries
        ]

        self.facts.update({
            'routing_table': routing_table
        })


class Interfaces(Factbase):
    def populate_facts(self):
        interfaces = []
        cls_types = (AggregateInterface, EthernetInterface, VlanInterface, LoopbackInterface, TunnelInterface)

        for cls_type in cls_types:
            listing = cls_type.refreshall(self.parent, add=False)
            for elm in listing:
                iface_info = {
                    'name': elm.name,
                    'comment': elm.comment,
                    'ip': getattr(elm, 'ip', []),
                    'ipv6': [],
                }
                for child in elm.children:
                    if isinstance(child, IPv6Address):
                        iface_info['ipv6'].append(child.uid)
                    elif isinstance(child, Layer3Subinterface) or isinstance(child, Layer2Subinterface):
                        child_info = {
                            'name': child.name,
                            'comment': child.comment,
                            'tag': child.tag,
                            'ip': getattr(child, 'ip', []),
                            'ipv6': [],
                        }
                        for sub_child in child.children:
                            if isinstance(child, IPv6Address):
                                child_info['ipv6'].append(sub_child.name)
                        interfaces.append(child_info)
                interfaces.append(iface_info)

        newlist = sorted(interfaces, key=lambda k: k['name'])
        self.facts.update({
            'interfaces': newlist
        })


class Ha(Factbase):
    def populate_facts(self):
        root = self.parent.op('show high-availability all')

        if root.find('./result/enabled').text == 'yes':
            ha_enabled = True
            ha_localmode = root.find('./result/group/local-info/mode').text
            ha_localstate = root.find('./result/group/local-info/state').text
        else:
            ha_enabled = False
            ha_localmode = "standalone"
            ha_localstate = "active"

        self.facts.update({
            'ha_enabled': ha_enabled,
            'ha_localmode': ha_localmode,
            'ha_localstate': ha_localstate
        })


class Vr(Factbase):
    def populate_facts(self):
        listing = VirtualRouter.refreshall(self.parent, add=False)

        virtual_routers = []
        for vr in listing:
            info = {
                'vr_name': vr.name,
                'vr_iflist': vr.interface or [],
                'vr_asn': None,
                'vr_routerid': None,
            }
            for child in vr.children:
                if isinstance(child, Bgp):
                    info['vr_asn'] = child.local_as
                    info['vr_routerid'] = child.router_id
            virtual_routers.append(info)

        self.facts.update({
            'virtual_routers': virtual_routers
        })


class VsysFacts(Factbase):
    def populate_facts(self):
        # Get session usage XML
        session_root = self.parent.op('show session meter')

        # Loop through all VSYS
        virtual_systems = []
        vsys_list = Vsys.refreshall(self.parent, name_only=True)
        for vsys in vsys_list:
            for var in ('display_name', 'interface', 'virtual_routers'):
                vsys.refresh_variable(var)

            zones = [x.name for x in Zone.refreshall(vsys, name_only=True)]
            vsys_id = vsys.name[4:]
            vsys_sessions = session_root.find(".//entry/[vsys='" + vsys_id + "']")
            vsys_currentsessions = vsys_sessions.find('.//current').text
            vsys_maxsessions = vsys_sessions.find('.//maximum').text

            virtual_systems.append({
                'vsys_id': vsys_id,
                'vsys_name': vsys.name,
                'vsys_description': vsys.display_name,
                'vsys_iflist': vsys.interface,
                'vsys_vrlist': vsys.virtual_routers,
                'vsys_zonelist': zones,
                'vsys_maxsessions': vsys_maxsessions,
                'vsys_currentsessions': vsys_currentsessions,
            })

        self.facts.update({
            'virtual-systems': virtual_systems
        })


class Config(Factbase):
    def populate_facts(self):
        self.parent.xapi.show()
        config = self.parent.xapi.xml_result().encode('utf-8')

        self.facts.update({
            'config': config
        })


FACT_SUBSETS = dict(
    system=System,
    session=Session,
    interfaces=Interfaces,
    ha=Ha,
    vr=Vr,
    vsys=VsysFacts,
    config=Config,
    routing=Routing,
)

VALID_SUBSETS = frozenset(FACT_SUBSETS.keys())


def main():
    helper = get_connection(
        with_classic_provider_spec=True,
        panorama_error='This module is for firewall facts only',
        argument_spec=dict(
            gather_subset=dict(default=['!config'], type='list'),

            # TODO(gfreeman) - remove in a later version.
            host=dict(),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=False,
        required_one_of=helper.required_one_of,
    )

    # TODO(gfreeman) - remove in a later version.
    if module.params['host'] is not None:
        module.fail_json(msg='Param "host" is removed; use "provider" instead')

    parent = helper.get_pandevice_parent(module)

    gather_subset = module.params['gather_subset']

    runable_subsets = set()
    exclude_subsets = set()

    for subset in gather_subset:
        if subset == 'all':
            runable_subsets.update(VALID_SUBSETS)
            continue

        if subset.startswith('!'):
            subset = subset[1:]
            if subset == 'all':
                exclude_subsets.update(VALID_SUBSETS)
                continue
            exclude = True
        else:
            exclude = False

        if subset not in VALID_SUBSETS:
            module.fail_json(msg='Subset must be one of [%s], got %s' %
                             (', '.join(VALID_SUBSETS), subset))

        if exclude:
            exclude_subsets.add(subset)
        else:
            runable_subsets.add(subset)

    if not runable_subsets:
        runable_subsets.update(VALID_SUBSETS)

    runable_subsets.difference_update(exclude_subsets)
    runable_subsets.add('system')

    facts = dict()
    facts['gather_subset'] = list(runable_subsets)

    # Create instance classes, e.g. System, Session etc.
    instances = list()

    for key in runable_subsets:
        instances.append(FACT_SUBSETS[key](module, parent))

    # Populate facts for instances
    for inst in instances:
        inst.populate_facts()
        facts.update(inst.facts)

    ansible_facts = dict()

    for key, value in iteritems(facts):
        key = 'ansible_net_%s' % key
        ansible_facts[key] = value

    module.exit_json(ansible_facts=ansible_facts)


if __name__ == '__main__':
    main()
