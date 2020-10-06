# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c) 2018 Palo Alto Networks techbizdev, <techbizdev@paloaltonetworks.com>
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import absolute_import, division, print_function
__metaclass__ = type


import time


_MIN_VERSION_ERROR = '{0} version ({1}) < minimum version ({2})'
HAS_PANDEVICE = True
try:
    import panos
    from panos.base import PanDevice
    from panos.firewall import Firewall
    from panos.panorama import DeviceGroup, Template, TemplateStack
    from panos.policies import PreRulebase, PostRulebase, Rulebase
    from panos.device import Vsys
    from panos.errors import PanDeviceError
    from panos.errors import PanCommitNotNeeded
except ImportError:
    try:
        import pandevice as panos
        from pandevice.base import PanDevice
        from pandevice.firewall import Firewall
        from pandevice.panorama import DeviceGroup, Template, TemplateStack
        from pandevice.policies import PreRulebase, PostRulebase, Rulebase
        from pandevice.device import Vsys
        from pandevice.errors import PanDeviceError
        from pandevice.errors import PanCommitNotNeeded
    except ImportError:
        HAS_PANDEVICE = False


def _vstr(val):
    return '{0}.{1}.{2}'.format(*val)


def eltostr(obj):
    try:
        # Try pretty print first if pandevice supports it
        return obj.element_str(pretty_print=True)
    except TypeError:
        # Fall back to normal
        return obj.element_str()


class ConnectionHelper(object):
    def __init__(self, min_pandevice_version, min_panos_version,
                 error_on_firewall_shared, panorama_error, firewall_error,
                 template_is_optional):
        """Performs connection initialization and determines params."""
        # Params for AnsibleModule.
        self.argument_spec = {}
        self.required_one_of = []

        # Params for pandevice tree construction.
        self.vsys = None
        self.device_group = None
        self.vsys_dg = None
        self.rulebase = None
        self.template = None
        self.template_stack = None
        self.vsys_importable = None
        self.vsys_shared = None
        self.min_pandevice_version = min_pandevice_version
        self.min_panos_version = min_panos_version
        self.error_on_firewall_shared = error_on_firewall_shared
        self.panorama_error = panorama_error
        self.firewall_error = firewall_error
        self.template_is_optional = template_is_optional

        # The PAN-OS device.
        self.device = None

    def get_pandevice_parent(self, module, timeout=0):
        """Builds the pandevice object tree, returning the parent object.

        If pandevice is not installed, then module.fail_json() will be
        invoked.

        Arguments:
            * module(AnsibleModule): the ansible module.
            * timeout(int): Number of seconds to retry opening the connection to PAN-OS.

        Returns:
            * The parent pandevice object based on the spec given to
              get_connection().
        """
        # Sanity check.
        if not HAS_PANDEVICE:
            module.fail_json(msg='Missing required library "pandevice".')

        pdv = tuple(int(x) for x in panos.__version__.split('.'))

        # Inform people that they should upgrade to pan-os-python instead of pandevice.
        if pdv < (1, 0, 0):
            lum = [
                'Python library "pandevice" is now "pan-os-python" and is now 1.0!',
                'Please "pip install pan-os-python" at your earliest convenience.',
            ]
            module.deprecate(' '.join(lum), version='3.0.0', collection_name='paloaltonetworks.panos')

        # Verify pandevice minimum version.
        if self.min_pandevice_version is not None:
            if pdv < self.min_pandevice_version:
                module.fail_json(msg=_MIN_VERSION_ERROR.format(
                    'panos', panos.__version__,
                    _vstr(self.min_pandevice_version)))

        pan_device_auth, serial_number = None, None
        if module.params['provider'] and module.params['provider']['ip_address']:
            pan_device_auth = (
                module.params['provider']['ip_address'],
                module.params['provider']['username'],
                module.params['provider']['password'],
                module.params['provider']['api_key'],
                module.params['provider']['port'],
            )
            serial_number = module.params['provider']['serial_number']
        elif module.params.get('ip_address', None) is not None:
            pan_device_auth = (
                module.params['ip_address'],
                module.params['username'],
                module.params['password'],
                module.params['api_key'],
                module.params['port'],
            )
            msg = 'Classic provider params are deprecated; use "provider" instead'
            module.deprecate(msg, version='3.0.0', collection_name='paloaltonetworks.panos')
        else:
            module.fail_json(msg='Provider params are required.')

        # Create the connection object.
        if not isinstance(timeout, int):
            raise ValueError('Timeout must be an int')
        elif timeout < 0:
            raise ValueError('Timeout must greater than or equal to 0')
        end_time = time.time() + timeout
        while True:
            try:
                self.device = PanDevice.create_from_device(*pan_device_auth)
            except PanDeviceError as e:
                if timeout == 0:
                    module.fail_json(msg='Failed connection: {0}'.format(e))
                elif time.time() >= end_time:
                    module.fail_json(msg='Connection timeout: {0}'.format(e))
            else:
                break

        # Verify PAN-OS minimum version.
        if self.min_panos_version is not None:
            if self.device._version_info < self.min_panos_version:
                module.fail_json(msg=_MIN_VERSION_ERROR.format(
                    'PAN-OS', _vstr(self.device._version_info),
                    _vstr(self.min_panos_version)))

        # Optional: Firewall via Panorama connectivity specified.
        if hasattr(self.device, 'refresh_devices') and serial_number:
            fw = Firewall(serial=serial_number)
            self.device.add(fw)
            self.device = fw

        parent = self.device
        no_shared = 'Scope "shared" is not allowed'
        not_found = '{0} "{1}" is not present.'
        pano_mia_param = 'Param "{0}" is required for Panorama but not specified.'
        ts_error = 'Specify either the template or the template stack{0}.'
        if hasattr(self.device, 'refresh_devices'):
            # Panorama connection.
            templated = False

            # Error if Panorama is not supported.
            if self.panorama_error is not None:
                module.fail_json(msg=self.panorama_error)

            # Spec: template stack.
            tmpl_required = False
            added_template = False
            if self.template_stack is not None:
                name = module.params[self.template_stack]
                if name is not None:
                    templated = True
                    stacks = TemplateStack.refreshall(parent, name_only=True)
                    for ts in stacks:
                        if ts.name == name:
                            parent = ts
                            added_template = True
                            break
                    else:
                        module.fail_json(msg=not_found.format(
                            'Template stack', name,
                        ))
                elif self.template is not None:
                    tmpl_required = True
                elif not self.template_is_optional:
                    module.fail_json(msg=pano_mia_param.format(self.template_stack))

            # Spec: template.
            if self.template is not None:
                name = module.params[self.template]
                if name is not None:
                    templated = True
                    if added_template:
                        module.fail_json(msg=ts_error.format(', not both'))
                    templates = Template.refreshall(parent, name_only=True)
                    for t in templates:
                        if t.name == name:
                            parent = t
                            break
                    else:
                        module.fail_json(msg=not_found.format(
                            'Template', name,
                        ))
                elif self.template_is_optional:
                    pass
                elif tmpl_required:
                    module.fail_json(msg=ts_error.format(''))
                elif not added_template:
                    module.fail_json(msg=pano_mia_param.format(self.template))

            # Spec: vsys_dg or device_group.
            dg_name = self.vsys_dg or self.device_group
            if dg_name is not None:
                name = module.params[dg_name]
                if name not in (None, 'shared'):
                    groups = DeviceGroup.refreshall(parent, name_only=True)
                    for dg in groups:
                        if dg.name == name:
                            parent = dg
                            break
                    else:
                        module.fail_json(msg=not_found.format(
                            'Device group', name,
                        ))

            # Spec: vsys importable.
            vsys_name = self.vsys_importable or self.vsys or self.vsys_shared
            if dg_name is None and templated and vsys_name is not None:
                name = module.params[vsys_name]
                if name not in (None, 'shared'):
                    vo = Vsys(name)
                    parent.add(vo)
                    parent = vo

            # Spec: rulebase.
            if self.rulebase is not None:
                if module.params[self.rulebase] in (None, 'pre-rulebase'):
                    rb = PreRulebase()
                    parent.add(rb)
                    parent = rb
                elif module.params[self.rulebase] == 'rulebase':
                    rb = Rulebase()
                    parent.add(rb)
                    parent = rb
                elif module.params[self.rulebase] == 'post-rulebase':
                    rb = PostRulebase()
                    parent.add(rb)
                    parent = rb
                else:
                    module.fail_json(msg=not_found.format(
                        'Rulebase', module.params[self.rulebase]))
        else:
            # Firewall connection.
            # Error if firewalls are not supported.
            if self.firewall_error is not None:
                module.fail_json(msg=self.firewall_error)

            # Spec: vsys or vsys_dg or vsys_importable.
            vsys_name = self.vsys_dg or self.vsys or self.vsys_importable or self.vsys_shared
            if vsys_name is not None:
                parent.vsys = module.params[vsys_name]
                if parent.vsys == 'shared' and self.error_on_firewall_shared:
                    module.fail_json(msg=no_shared)

            # Spec: rulebase.
            if self.rulebase is not None:
                rb = Rulebase()
                parent.add(rb)
                parent = rb

        # If the module has the commit option set, show a deprecation warning.
        if module.params.get('commit'):
            module.deprecate(
                'Please use the commit modules instead of the commit option',
                version='3.0.0', collection_name='paloaltonetworks.panos'
            )

        # Done.
        return parent

    def apply_state(self, obj, listing, module, enabled_disabled_param=None,
                    invert_enabled_disabled=False):
        """Generic state handling.

        Note:  If module.check_mode is True, then this function returns
        True if a change is needed, but doesn't actually make the change.

        Args:
            obj: The pandevice object to be applied.
            listing(list): List of objects currently configured.
            module: The Ansible module.
            enabled_disabled_param: If this is set, then this function also
                supports a state of "enabled" or "disabled", and the pandevice
                param has the specified name.
            invert_enabled_disabled (bool): Set this to True if the param
                specified in "enabled_disabled_param" is a disabled flag
                instead of an enabled flag.

        Returns:
            bool: If a change was made or not.
        """
        supported_states = ['present', 'absent']
        if enabled_disabled_param is not None:
            supported_states.extend(['enabled', 'disabled'])

        # Sanity check.
        if 'state' not in module.params:
            module.fail_json(msg='No "state" present')
        elif module.params['state'] not in supported_states:
            module.fail_json(msg='Unsupported state: {0}'.format(
                module.params['state']))
        elif enabled_disabled_param is not None and not hasattr(obj, enabled_disabled_param):
            module.fail_json(msg='enabled/disabled param {0} not present'.format(enabled_disabled_param))

        # Apply the state.
        changed = False
        diff = None
        if module.params['state'] == 'present':
            for item in listing:
                if item.uid != obj.uid:
                    continue
                diff = dict(
                    before=eltostr(item)
                )
                obj_child_types = [x.__class__ for x in obj.children]
                other_children = []
                for x in item.children:
                    if x.__class__ in obj_child_types:
                        continue
                    other_children.append(x)
                    item.remove(x)
                if not item.equal(obj, compare_children=True):
                    changed = True
                    obj.extend(other_children)
                    diff['after'] = eltostr(obj)
                    if not module.check_mode:
                        try:
                            obj.apply()
                        except PanDeviceError as e:
                            module.fail_json(msg='Failed apply: {0}'.format(e))
                break
            else:
                changed = True
                diff = dict(
                    before="",
                    after=eltostr(obj)
                )
                if not module.check_mode:
                    try:
                        obj.create()
                    except PanDeviceError as e:
                        module.fail_json(msg='Failed create: {0}'.format(e))
        elif module.params['state'] == 'absent':
            if obj.uid in [x.uid for x in listing]:
                changed = True
                diff = dict(
                    before=eltostr(obj),
                    after=""
                )
                if not module.check_mode:
                    try:
                        obj.delete()
                    except PanDeviceError as e:
                        module.fail_json(msg='Failed delete: {0}'.format(e))
        else:
            for item in listing:
                if item.uid != obj.uid:
                    continue

                val = getattr(item, enabled_disabled_param)
                if invert_enabled_disabled:
                    val = not val

                if module.params['state'] == 'enabled' and not val:
                    changed = True
                elif module.params['state'] == 'disabled' and val:
                    changed = True

                if changed:
                    diff = dict(
                        before=eltostr(item)
                    )
                    setattr(item, enabled_disabled_param, not val)
                    diff['after'] = eltostr(item)
                    if not module.check_mode:
                        try:
                            item.update(enabled_disabled_param)
                        except PanDeviceError as e:
                            module.fail_json(msg='Failed toggle: {0}'.format(e))
                break
            else:
                module.fail_json(msg='Cannot enable/disable non-existing obj')

        return changed, diff

    def apply_position(self, obj, location, existing_rule, module):
        """Moves an object into the given location.

        This function invokes "obj"'s refreshall() on obj.parent, which
        removes both obj and all other obj.__class__ types from
        obj.parent.  Since moving a rule into place is likely the last
        step, the state of the pandevice object tree should be inconsequential.

        Note:  If module.check_mode is True, then this function returns
        True if a change is needed, but doesn't actually make the change.

        Args:
            obj: The pandevice object to be moved.
            location: Location keyword (before, after, top, bottom).
            existing_rule: The reference for before/after positioning.
            module: The Ansible module.

        Returns:
            bool: If a change was needed.
        """
        # Variables.
        uid = obj.uid
        rule = None
        changed = False
        obj_index = None
        ref_index = None

        # Sanity check the location / existing_rule params.
        improper_combo = False
        improper_combo |= location is None and existing_rule is not None
        improper_combo |= location in ('before', 'after') and existing_rule is None
        improper_combo |= location in ('top', 'bottom') and existing_rule is not None
        if improper_combo:
            module.fail_json(msg='Improper combination of "location" / "existing_rule".')
        elif location is None:
            return False

        # Retrieve the current rules.
        try:
            rules = obj.__class__.refreshall(obj.parent, name_only=True)
        except PanDeviceError as e:
            module.fail_json(msg='Failed move refresh: {0}'.format(e))

        listing = [x.uid for x in rules]
        try:
            obj_index = listing.index(uid)
            rule = rules[obj_index]
        except ValueError:
            module.fail_json(msg="Object {0} isn't present for move".format(uid))

        if location == 'top':
            if listing[0] != uid:
                changed = True
        elif location == 'bottom':
            if listing[-1] != uid:
                changed = True
        else:
            try:
                ref_index = listing.index(existing_rule)
            except ValueError:
                msg = [
                    'Cannot do relative rule placement',
                    '"{0}" does not exist.'.format(existing_rule),
                ]
                module.fail_json(msg='{0}'.format(msg))
            if location == 'before':
                if obj_index + 1 != ref_index:
                    changed = True
            elif location == 'after':
                if ref_index + 1 != obj_index:
                    changed = True

        # Perform the move (if not check mode).
        if changed and not module.check_mode:
            try:
                rule.move(location, existing_rule)
            except PanDeviceError as e:
                module.fail_json(msg='Failed move: {0}'.format(e))

        # Done.
        return changed

    def commit(self, module, include_template=False, admins=None):
        """Performs a commit.

        In the case where the device is Panorama, then a commit-all is
        executed after the commit.  The device group is taken from either
        vsys_dg or device_group.  The template is set to True if template
        is specified.  Returns True if the configuration was committed,
        False if not.

        Note:  If module.check_mode is True, then this function does not
        perform the commit.

        Args:
            include_template (bool): (Panorama only) Force include the template.
            admins (list): This is the list of admins whose changes will be committed to
                the firewall/Panorama. The admins argument works with PanOS 8.0+.
        """
        committed = False

        if module.check_mode:
            return

        try:
            self.device.commit(sync=True, exception=True, admins=admins)
            committed = True
        except PanCommitNotNeeded:
            pass
        except PanDeviceError as e:
            module.fail_json(msg='Failed commit: {0}'.format(e))

        if not hasattr(self.device, 'commit_all'):
            return committed

        dg_name = self.vsys_dg or self.device_group
        if dg_name is not None:
            dg_name = module.params[dg_name]

        if dg_name in (None, 'shared'):
            return committed

        if not include_template:
            if self.template:
                include_template = True

        try:
            self.device.commit_all(
                sync=True,
                sync_all=True,
                devicegroup=dg_name,
                include_template=include_template,
                exception=True,
            )
            committed = True
        except PanCommitNotNeeded:
            pass
        except PanDeviceError as e:
            module.fail_json(msg='Failed commit-all: {0}'.format(e))

        return committed

    def to_module_dict(self, element, renames=None):
        """Changes a pandevice object or list of objects into a dict / list of dicts.

        Args:
            element: Either a single pandevice object or a list of pandevice objects
            renames: If the names of the pandevice object is different from the
                Ansible param names, this is a iterable of two element tuples where
                the first element is the pandevice object name, and the second is
                the Ansible name.

        Returns:
            A dict if "element" was a single pandevice object, or a list of dicts
            if "element" was a list of pandevice objects.

        """
        if isinstance(element, list):
            ans = []
            for elm in element:
                spec = elm.about()
                if renames is not None:
                    for pandevice_param, ansible_param in renames:
                        spec[ansible_param] = spec.pop(pandevice_param)
                ans.append(spec)
        else:
            ans = element.about()
            if renames is not None:
                for pandevice_param, ansible_param in renames:
                    ans[ansible_param] = ans.pop(pandevice_param)

        return ans


def get_connection(vsys=None, vsys_shared=None, device_group=None,
                   vsys_dg=None, vsys_importable=None,
                   rulebase=None, template=None, template_stack=None,
                   with_classic_provider_spec=False,
                   with_state=False, with_enabled_state=False,
                   argument_spec=None, required_one_of=None,
                   min_pandevice_version=None, min_panos_version=None,
                   error_on_firewall_shared=False,
                   panorama_error=None, firewall_error=None,
                   template_is_optional=False):
    """Returns a helper object that handles pandevice object tree init.

    The `vsys`, `vsys_shared`, `device_group`, `vsys_dg`, `vsys_importable`, `rulebase`,
    `template`, and `template_stack` params can be any of the following types:

        * None - do not include this in the spec
        * True - use the default param name
        * string - use this string for the param name

    The `min_pandevice_version` and `min_panos_version` args expect a 3 element
    tuple of ints.  For example, `(0, 6, 0)` or `(8, 1, 0)`.

    If you are including template support (by defining either `template` and/or
    `template_stack`), and the thing the module is enabling the management of is
    an "importable", you should define either `vsys_importable` (whose default
    value is None) or `vsys` (whose default value is 'vsys1').

    Arguments:
        vsys: The vsys (default: 'vsys1').
        vsys_shared: The vsys (default: 'shared').
        device_group: Panorama only - The device group (default: 'shared').
        vsys_dg: The param name if vsys and device_group are a shared param.
        vsys_importable: Either this or `vsys` should be specified.  For:
            - Interfaces
            - VLANs
            - Virtual Wires
            - Virtual Routers
        rulebase: This is a policy of some sort.
        template: Panorama - The template name.
        template_stack: Panorama - The template stack name.
        with_classic_provider_spec(bool): Include the ip_address, username,
            password, api_key, and port params in the base spec, and make the
            "provider" param optional.
        with_state(bool): Include the standard 'state' param.
        with_enabled_state(bool): Include 'state', but also support "enabled"
            and "disabled" as valid states.
        argument_spec(dict): The argument spec to mixin with the
            generated spec based on the given parameters.
        required_one_of(list): List of lists to extend into required_one_of.
        min_pandevice_version(tuple): Minimum pandevice version allowed.
        min_panos_version(tuple): Minimum PAN-OS version allowed.
        error_on_firewall_shared(bool): Don't allow "shared" vsys.
        panorama_error(str): The error message if the device is Panorama.
        firewall_error(str): The error message if the device is a firewall.
        template_is_optional(bool): Set this to True if the config object could
            be local on Panorama and not just in a template or template stack.

    Returns:
        ConnectionHelper
    """
    helper = ConnectionHelper(
        min_pandevice_version, min_panos_version,
        error_on_firewall_shared, panorama_error, firewall_error,
        template_is_optional,
    )
    req = []
    spec = {
        'provider': {
            'required': True,
            'type': 'dict',
            'required_one_of': [['password', 'api_key'], ],
            'options': {
                'ip_address': {'required': True},
                'username': {'default': 'admin'},
                'password': {'no_log': True},
                'api_key': {'no_log': True},
                'port': {'default': 443, 'type': 'int'},
                'serial_number': {'no_log': True},
            },
        },
    }

    if with_classic_provider_spec:
        spec['provider']['required'] = False
        spec['provider']['options']['ip_address']['required'] = False
        del(spec['provider']['required_one_of'])
        spec.update({
            'ip_address': {'required': False},
            'username': {'default': 'admin'},
            'password': {'no_log': True},
            'api_key': {'no_log': True},
            'port': {'default': 443, 'type': 'int'},
        })
        req.extend([
            ['provider', 'ip_address'],
            ['provider', 'password', 'api_key'],
        ])

    if with_state:
        spec['state'] = {
            'default': 'present',
            'choices': ['present', 'absent'],
        }

    if with_enabled_state:
        spec['state'] = {
            'default': 'present',
            'choices': ['present', 'absent', 'enabled', 'disabled'],
        }

    if vsys_dg is not None:
        if isinstance(vsys_dg, bool):
            param = 'vsys_dg'
        else:
            param = vsys_dg
        spec[param] = {}
        helper.vsys_dg = param
    else:
        if vsys is not None:
            if isinstance(vsys, bool):
                param = 'vsys'
            else:
                param = vsys
            spec[param] = {'default': 'vsys1'}
            helper.vsys = param
        if device_group is not None:
            if isinstance(device_group, bool):
                param = 'device_group'
            else:
                param = device_group
            spec[param] = {'default': 'shared'}
            helper.device_group = param
        if vsys_importable is not None:
            if vsys is not None:
                raise KeyError('Define "vsys" or "vsys_importable", not both.')
            if isinstance(vsys_importable, bool):
                param = 'vsys'
            else:
                param = vsys_importable
            spec[param] = {}
            helper.vsys_importable = param
        if vsys_shared is not None:
            if vsys is not None:
                raise KeyError('Define "vsys" or "vsys_shared", not both.')
            elif vsys_importable is not None:
                raise KeyError('Define "vsys_importable" or "vsys_shared", not both.')
            if isinstance(vsys_shared, bool):
                param = 'vsys'
            else:
                param = vsys_shared
            spec[param] = {'default': 'shared'}
            helper.vsys_shared = param

    if rulebase is not None:
        if isinstance(rulebase, bool):
            param = 'rulebase'
        else:
            param = rulebase
        spec[param] = {
            'default': None,
            'choices': ['pre-rulebase', 'rulebase', 'post-rulebase'],
        }
        helper.rulebase = param

    if template is not None:
        if isinstance(template, bool):
            param = 'template'
        else:
            param = template
        spec[param] = {}
        helper.template = param

    if template_stack is not None:
        if isinstance(template_stack, bool):
            param = 'template_stack'
        else:
            param = template_stack
        spec[param] = {}
        helper.template_stack = param

    if argument_spec is not None:
        for k in argument_spec.keys():
            if k in spec:
                raise KeyError('{0}: key used by connection helper.'.format(k))
            spec[k] = argument_spec[k]

    if required_one_of is not None:
        req.extend(required_one_of)

    # Done.
    helper.argument_spec = spec
    helper.required_one_of = req
    return helper
