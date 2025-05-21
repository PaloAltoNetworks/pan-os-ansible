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

import re
import shlex
import sys
import time
from functools import reduce
import importlib

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection

_MIN_VERSION_ERROR = "{0} version ({1}) < minimum version ({2})"
HAS_PANDEVICE = True
try:
    import panos
    from panos.base import PanDevice
    from panos.device import Vsys
    from panos.errors import PanCommitNotNeeded, PanDeviceError, PanObjectMissing
    from panos.firewall import Firewall
    from panos.panorama import DeviceGroup, Template, TemplateStack
    from panos.policies import PostRulebase, PreRulebase, Rulebase
except ImportError:
    try:
        import pandevice as panos
        from pandevice.base import PanDevice
        from pandevice.device import Vsys
        from pandevice.errors import (
            PanCommitNotNeeded,
            PanDeviceError,
            PanObjectMissing,
        )
        from pandevice.firewall import Firewall
        from pandevice.panorama import DeviceGroup, Template, TemplateStack
        from pandevice.policies import PostRulebase, PreRulebase, Rulebase
    except ImportError:
        HAS_PANDEVICE = False


def _vstr(val):
    return "{0}.{1}.{2}".format(*val)


def eltostr(obj):
    if obj is None:
        return ""

    try:
        # Try pretty print first if pandevice supports it
        return obj.element_str(pretty_print=True)
    except TypeError:
        # Fall back to normal
        return obj.element_str()


def to_sdk_cls(pkg_name, cls_name):
    sdk_names = ("panos", "pandevice")

    for sdk_name in ("panos", "pandevice"):
        try:
            mod = importlib.import_module("{0}.{1}".format(sdk_name, pkg_name))
        except ModuleNotFoundError:
            continue
        else:
            try:
                return getattr(mod, cls_name)
            except AttributeError:
                raise Exception(
                    "{0}.{1}.{2} does not exist".format(sdk_name, pkg_name, cls_name)
                )

    raise Exception("Couldn't find any sdk package named {0}".format(pkg_name))


class ConnectionHelper(object):
    def __init__(
        self,
        min_pandevice_version,
        min_panos_version,
        min_panos_upgrade_assurance_version,
        error_on_firewall_shared,
        panorama_error,
        firewall_error,
        template_is_optional,
    ):
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
        self.min_panos_upgrade_assurance_version = min_panos_upgrade_assurance_version
        self.error_on_firewall_shared = error_on_firewall_shared
        self.panorama_error = panorama_error
        self.firewall_error = firewall_error
        self.template_is_optional = template_is_optional

        # Set by the helper's construction.
        self.sdk_cls = None
        self.parents = ()
        self.sdk_params = {}
        self.extra_params = {}
        self.default_values = {}
        self.preset_values = {}
        self.reference_operations = ()
        self.ansible_to_sdk_param_mapping = {}
        self.with_uuid = False
        self.with_commit = False
        self.with_target = False
        self.with_movement = False
        self.with_audit_comment = False
        self.with_import_support = False
        self.with_gathered_filter = False
        self.with_update_in_apply_state = False
        self.zone_mode = None
        self.default_zone_mode = None

        # References.
        self.with_set_vlan_reference = False
        self.with_set_vsys_reference = False
        self.with_set_zone_reference = False
        self.with_set_virtual_router_reference = False
        self.with_set_vlan_interface_reference = False

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
        try:
            importlib.import_module("pan.xapi")
        except ModuleNotFoundError:
            module.fail_json(
                msg='Missing required library "pan-python".',
                pypi="https://pypi.org/project/pan-python",
                syspath=sys.path,
            )
        if not HAS_PANDEVICE:
            module.fail_json(
                msg='Missing required library "pan-os-python".',
                pypi="https://pypi.org/project/pan-os-python",
                syspath=sys.path,
            )

        pdv = tuple(int(x) for x in panos.__version__.split("."))

        # Inform people that they should upgrade to pan-os-python instead of pandevice.
        if pdv < (1, 0, 0):
            lum = [
                'Python library "pandevice" is now "pan-os-python" and is now 1.0!',
                'Please "pip install pan-os-python" at your earliest convenience.',
            ]
            module.deprecate(
                " ".join(lum), version="4.0.0", collection_name="paloaltonetworks.panos"
            )

        # Verify pan-os-python (formerly pandevice) minimum version.
        if self.min_pandevice_version is not None:
            if pdv < self.min_pandevice_version:
                module.fail_json(
                    msg=_MIN_VERSION_ERROR.format(
                        "pan-os-python",
                        panos.__version__,
                        _vstr(self.min_pandevice_version),
                    ),
                    sdk_package_path=panos.__file__.rsplit("/", 1)[0],
                )

        if self.min_panos_upgrade_assurance_version is not None:
            try:
                import panos_upgrade_assurance
            except ImportError:
                module.fail_json(
                    msg='Missing required library "panos_upgrade_assurance".',
                    syspath=sys.path,
                )
            # This code assumes both panos_upgrade_assurance.version and self.min_panos_upgrade_assurance
            # are a tuple of 3 ints.  If panos_upgrade_assurance.version is a string, then you'll have
            # to turn it into a 3 element tuple of ints to do the comparison.
            pua_ver = tuple(
                int(x) for x in panos_upgrade_assurance.__version__.split(".")
            )
            if pua_ver < self.min_panos_upgrade_assurance_version:
                module.fail_json(
                    msg=_MIN_VERSION_ERROR.format(
                        "panos_upgrade_assurance",
                        _vstr(pua_ver),
                        _vstr(self.min_panos_upgrade_assurance_version),
                    )
                )

        pan_device_auth, serial_number = None, None
        if module.params["provider"] and module.params["provider"]["ip_address"]:
            pan_device_auth = (
                module.params["provider"]["ip_address"],
                module.params["provider"]["username"],
                module.params["provider"]["password"],
                module.params["provider"]["api_key"],
                module.params["provider"]["port"],
            )
            serial_number = module.params["provider"]["serial_number"]
        elif module.params.get("ip_address", None) is not None:
            pan_device_auth = (
                module.params["ip_address"],
                module.params["username"],
                module.params["password"],
                module.params["api_key"],
                module.params["port"],
            )
            msg = 'Classic provider params are deprecated; use "provider" instead'
            module.deprecate(
                msg, version="4.0.0", collection_name="paloaltonetworks.panos"
            )
        else:
            module.fail_json(msg="Provider params are required.")

        # Create the connection object.
        if not isinstance(timeout, int):
            raise ValueError("Timeout must be an int")
        elif timeout < 0:
            raise ValueError("Timeout must greater than or equal to 0")
        end_time = time.time() + timeout
        while True:
            try:
                self.device = PanDevice.create_from_device(*pan_device_auth)
            except PanDeviceError as e:
                if timeout == 0:
                    module.fail_json(msg="Failed connection: {0}".format(e))
                elif time.time() >= end_time:
                    module.fail_json(msg="Connection timeout: {0}".format(e))
            else:
                break

        # Verify PAN-OS minimum version.
        if self.min_panos_version is not None:
            if self.device._version_info < self.min_panos_version:
                module.fail_json(
                    msg=_MIN_VERSION_ERROR.format(
                        "PAN-OS",
                        _vstr(self.device._version_info),
                        _vstr(self.min_panos_version),
                    )
                )

        # Optional: Firewall via Panorama connectivity specified.
        if hasattr(self.device, "refresh_devices") and serial_number:
            fw = Firewall(serial=serial_number)
            self.device.add(fw)
            self.device = fw

        parent = self.device
        no_shared = 'Scope "shared" is not allowed'
        not_found = '{0} "{1}" is not present.'
        pano_mia_param = 'Param "{0}" is required for Panorama but not specified.'
        ts_error = "Specify either the template or the template stack{0}."
        if hasattr(self.device, "refresh_devices"):
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
                        module.fail_json(
                            msg=not_found.format(
                                "Template stack",
                                name,
                            )
                        )
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
                        module.fail_json(msg=ts_error.format(", not both"))
                    templates = Template.refreshall(parent, name_only=True)
                    for t in templates:
                        if t.name == name:
                            parent = t
                            break
                    else:
                        module.fail_json(
                            msg=not_found.format(
                                "Template",
                                name,
                            )
                        )
                elif self.template_is_optional:
                    pass
                elif tmpl_required:
                    module.fail_json(msg=ts_error.format(""))
                elif not added_template:
                    module.fail_json(msg=pano_mia_param.format(self.template))

            # Spec: vsys_dg or device_group.
            dg_name = self.vsys_dg or self.device_group
            if dg_name is not None:
                name = module.params[dg_name]
                if name not in (None, "shared"):
                    groups = DeviceGroup.refreshall(parent, name_only=True)
                    for dg in groups:
                        if dg.name == name:
                            parent = dg
                            break
                    else:
                        module.fail_json(
                            msg=not_found.format(
                                "Device group",
                                name,
                            )
                        )

            # Spec: vsys importable.
            vsys_name = self.vsys_importable or self.vsys or self.vsys_shared
            if dg_name is None and templated and vsys_name is not None:
                name = module.params[vsys_name]
                if name not in (None, "shared"):
                    vo = Vsys(name)
                    parent.add(vo)
                    parent = vo

            # Spec: rulebase.
            if self.rulebase is not None:
                if module.params[self.rulebase] in (None, "pre-rulebase"):
                    rb = PreRulebase()
                    parent.add(rb)
                    parent = rb
                elif module.params[self.rulebase] == "rulebase":
                    rb = Rulebase()
                    parent.add(rb)
                    parent = rb
                elif module.params[self.rulebase] == "post-rulebase":
                    rb = PostRulebase()
                    parent.add(rb)
                    parent = rb
                else:
                    module.fail_json(
                        msg=not_found.format("Rulebase", module.params[self.rulebase])
                    )
        else:
            # Firewall connection.
            # Error if firewalls are not supported.
            if self.firewall_error is not None:
                module.fail_json(msg=self.firewall_error)

            # Spec: vsys or vsys_dg or vsys_importable.
            vsys_name = (
                self.vsys_dg or self.vsys or self.vsys_importable or self.vsys_shared
            )
            if vsys_name is not None:
                parent.vsys = module.params[vsys_name]
                if parent.vsys == "shared" and self.error_on_firewall_shared:
                    module.fail_json(msg=no_shared)

            # Spec: rulebase.
            if self.rulebase is not None:
                rb = Rulebase()
                parent.add(rb)
                parent = rb

        # If the module has the commit option set, show a deprecation warning.
        if module.params.get("commit"):
            module.deprecate(
                "Please use the commit modules instead of the commit option",
                version="4.0.0",
                collection_name="paloaltonetworks.panos",
            )

        # Done.
        return parent

    def process(self, module):
        result = {}

        # Sanity test the input.
        if not module:
            raise Exception("module must be specified")

        # Optional: initial handling.
        self.initial_handling(module)

        # Global deprecation checks.
        if self.with_commit and module.params["commit"]:
            module.deprecate(
                'Param "commit" is deprecated; use the various commit modules',
                version="4.0.0",
                collection_name="paloaltonetworks.panos",
            )

        # Verify imports, build the initial object hierarchy.
        parent = self.get_pandevice_parent(module)

        # Build out the final object hierarchy.
        for p_info in self.parents:
            p = None
            parent_pkg, parent_class, parent_param_name = (
                p_info[0],
                p_info[1],
                p_info[2],
            )
            if parent_param_name is None:
                p = to_sdk_cls(parent_pkg, parent_class)()
            else:
                p = to_sdk_cls(parent_pkg, parent_class)(
                    module.params[parent_param_name]
                )
            parent.add(p)
            parent = p

        # Optional: customized parent handling.
        parent = self.parent_handling(parent, module)
        if parent is None:
            raise Exception("parent_handling() must return the parent")

        # Build the object from the spec.
        spec = {}
        for ansible_param in self.sdk_params.keys():
            sdk_param = self.ansible_to_sdk_param_mapping.get(
                ansible_param, ansible_param
            )
            spec[sdk_param] = module.params.get(ansible_param)
            if ansible_param in self.preset_values.keys():
                self.preset_values[sdk_param] = self.preset_values.pop(ansible_param)
            if ansible_param in self.default_values.keys():
                self.default_values[sdk_param] = self.default_values.pop(ansible_param)

        if self.with_uuid:
            spec["uuid"] = module.params["uuid"]
        if self.with_target:
            spec["target"] = module.params["target"]
            spec["negate_target"] = module.params["negate_target"]
        self.spec_handling(spec, module)

        # Attach the object to the parent.
        if self.sdk_cls is None:
            raise Exception("sdk_cls must be specified")
        elif not isinstance(self.sdk_cls, tuple) or len(self.sdk_cls) != 2:
            raise Exception("helper.sdk_cls must be tuple of len()=2")
        obj = to_sdk_cls(*self.sdk_cls)(**spec)
        parent.add(obj)

        # Apply the state.
        self.pre_state_handling(obj, result, module)
        self.apply_state(obj, result=result, module=module)
        self.post_state_handling(obj, result, module)

        # Optional: with_movement.
        if self.with_movement and module.params["state"] in (
            "present",
            "merged",
            "replaced",
        ):
            result["changed"] |= self.apply_position(
                obj, module.params["location"], module.params["existing_rule"], module
            )

        # Optional: with_audit_comment.
        if self.with_audit_comment and result["changed"] and not module.check_mode:
            comment = module.params["audit_comment"]
            if comment:
                obj.opstate.audit_comment.update(comment)

        # Optional: with_commit.
        if self.with_commit and result["changed"] and module.params["commit"]:
            self.commit(module)

        # Done.
        module.exit_json(**result)

    def initial_handling(self, module):
        """Override to implement module specific deprecations or param massaging."""
        pass

    def parent_handling(self, parent, module):
        """Override if special parent handling is required."""
        return parent

    def spec_handling(self, spec, module):
        """Override to do any custom spec handling before the object is built.

        Note that if the class of a module is dynamically being determined, this
        function is the last chance to set self.sdk_cls.
        """
        pass

    def object_handling(self, obj, module):
        """Override to provide custom functionality for newly created/replaced objects.

        This method is run for newly created objects with merged state or
        created/replaced objects with present state.

        By default it will handle default values for objects.
        It's advised to call `super().object_handling(obj, module)` if overriden
        in the modules.
        """
        for key, obj_value in obj.about().items():
            if obj_value is None:
                setattr(obj, key, self._get_default_value(obj, key))

    def pre_state_handling(self, obj, result, module):
        """Override to provide custom pre-state handling functionality."""
        pass

    def post_state_handling(self, obj, result, module):
        """Override to provide custom post-state handling functionality."""
        pass

    def apply_state(
        self,
        obj,
        listing=None,
        module=None,
        enabled_disabled_param=None,
        invert_enabled_disabled=False,
        result=None,
    ):
        """Generic state handling.

        Note:  If module.check_mode is True, then this function returns
        True if a change is needed, but doesn't actually make the change.

        Args:
            obj: The pandevice object to be applied.
            listing(list): List of objects currently configured.  If this param
                is `None`, then this function will try to do a targetted refresh
                of the object based on the type of the `obj` parameter.
            module: The Ansible module.
            enabled_disabled_param: If this is set, then this function also
                supports a state of "enabled" or "disabled", and the pandevice
                param has the specified name.
            invert_enabled_disabled (bool): Set this to True if the param
                specified in "enabled_disabled_param" is a disabled flag
                instead of an enabled flag.
            result(dict): Update this dict with the results of this function.

        Returns:
            dict: To pass in to module.exit_json().
        """
        ref_spec = {
            "refresh": True,
            "update": not module.check_mode,
            "return_type": "bool",
        }
        supported_states = [
            "present",
            "absent",
            "merged",
            "replaced",
            "deleted",
            "gathered",
        ]
        if result is None:
            result = {}
        result.setdefault("changed", False)

        if enabled_disabled_param is not None:
            supported_states.extend(["enabled", "disabled"])

        # Sanity checks.
        if module is None:
            raise Exception("No module passed in to apply_state()")
        elif result is not None and not isinstance(result, dict):
            raise Exception("result should be a dict")
        elif "state" not in module.params:
            module.fail_json(msg='No "state" present')
        elif module.params["state"] not in supported_states:
            module.fail_json(
                msg="Unsupported state: {0}".format(module.params["state"])
            )
        elif enabled_disabled_param is not None and not hasattr(
            obj, enabled_disabled_param
        ):
            module.fail_json(
                msg="enabled/disabled param {0} not present".format(
                    enabled_disabled_param
                )
            )
        elif (
            self.with_set_zone_reference
            and not hasattr(obj, "mode")
            and self.default_zone_mode is None
        ):
            raise Exception(
                "set_zone_ref error: obj doesn't have a mode and there is no default_zone_mode given"
            )

        if listing is None:
            if module.params.get("state", None) == "gathered" and module.params.get(
                "gathered_filter", None
            ):
                # Refresh everything as the user is doing a gathered_filter retrieval.
                try:
                    listing = obj.__class__.refreshall(obj.parent, add=False)
                except PanDeviceError as e:
                    module.fail_json(
                        msg="Failed gathered_filter refresh: {0}".format(e),
                    )
            else:
                # Do a targetted refresh if the listing is None.
                cls = obj.__class__
                if getattr(cls, "NAME", None) is not None:
                    x = cls(obj.uid)
                else:
                    x = cls()
                x.parent = obj.parent
                try:
                    x.refresh()
                except PanObjectMissing:
                    listing = []
                except PanDeviceError as e:
                    module.fail_json(
                        msg="Failed refresh: {0}".format(e),
                    )
                else:
                    listing = [
                        x,
                    ]
                    # Copy the uuid, if it's present and unspecified.
                    if hasattr(x, "uuid") and obj.uuid is None:
                        obj.uuid = x.uuid

        # Apply the state.
        if module.params["state"] in ("present", "replaced"):
            # Apply the config.
            for item in listing:
                if item.uid != obj.uid:
                    continue
                result["before"] = self.describe(item)
                result["diff"] = {
                    "before": eltostr(item),
                }
                obj_child_types = [x.__class__ for x in obj.children]
                other_children = []
                for x in reversed(item.children):
                    if x.__class__ in obj_child_types:
                        continue
                    other_children.append(x)
                    item.remove(x)
                # object_handling need to be before equal comparison for evaluating defaults
                self.object_handling(obj, module)
                if not item.equal(obj, compare_children=True):
                    result["changed"] = True
                    obj.extend(other_children)
                    if not module.check_mode:
                        if self.with_update_in_apply_state:
                            for key, obj_value in obj.about().items():
                                # NOTE checking defaults for with_update_in_apply_state doesnot have
                                # a use for now as template, stack and device group dont have
                                # defaults in the SDK
                                if getattr(item, key) != getattr(obj, key):
                                    try:
                                        obj.update(key)
                                    except PanDeviceError as e:
                                        module.fail_json(
                                            msg="Failed update {0}: {1}".format(key, e)
                                        )
                            result["after"] = self.describe(obj)
                            result["diff"]["after"] = eltostr(obj)
                        else:
                            result["after"] = self.describe(obj)
                            result["diff"]["after"] = eltostr(obj)
                            try:
                                obj.apply()
                            except PanDeviceError as e:
                                module.fail_json(msg="Failed apply: {0}".format(e))
                break
            else:
                self.object_handling(obj, module)
                result["changed"] = True
                result["before"] = None
                result["after"] = self.describe(obj)
                result["diff"] = {
                    "before": "",
                    "after": eltostr(obj),
                }
                if not module.check_mode:
                    try:
                        obj.create()
                    except PanDeviceError as e:
                        module.fail_json(msg="Failed create: {0}".format(e))

            # Apply references.
            if self.with_set_vsys_reference:
                try:
                    result["changed"] |= obj.set_vsys(
                        module.params[self.vsys_importable],
                        **ref_spec,
                    )
                except PanDeviceError as e:
                    module.fail_json(msg="Failed set_vsys: {0}".format(e))
            if self.with_set_vlan_interface_reference:
                try:
                    result["changed"] |= obj.set_vlan_interface(
                        module.params["vlan_name"],
                        **ref_spec,
                    )
                except PanDeviceError as e:
                    module.fail_json(msg="Failed set_zone: {0}".format(e))
            if self.with_set_zone_reference:
                the_mode = getattr(obj, "mode", self.default_zone_mode)
                try:
                    result["changed"] |= obj.set_zone(
                        module.params["zone_name"],
                        mode=the_mode,
                        **ref_spec,
                    )
                except PanDeviceError as e:
                    module.fail_json(msg="Failed set_zone: {0}".format(e))
            if self.with_set_vlan_reference:
                try:
                    result["changed"] |= obj.set_vlan(
                        module.params["vlan_name"],
                        **ref_spec,
                    )
                except PanDeviceError as e:
                    module.fail_json(msg="Failed set_zone: {0}".format(e))
            if self.with_set_virtual_router_reference:
                try:
                    result["changed"] |= obj.set_virtual_router(
                        module.params["vr_name"],
                        **ref_spec,
                    )
                except PanDeviceError as e:
                    module.fail_json(msg="Failed set_virtual_router: {0}".format(e))
        elif module.params["state"] in ("absent", "deleted"):
            # Remove references.
            if self.with_set_virtual_router_reference:
                try:
                    result["changed"] |= obj.set_virtual_router(None, **ref_spec)
                except PanDeviceError as e:
                    module.fail_json(msg="Failed set_virtual_router: {0}".format(e))
            if self.with_set_vlan_reference:
                try:
                    result["changed"] |= obj.set_vlan(None, **ref_spec)
                except PanDeviceError as e:
                    module.fail_json(msg="Failed set_vlan: {0}".format(e))
            if self.with_set_zone_reference:
                the_mode = getattr(obj, "mode", self.default_zone_mode)
                try:
                    result["changed"] |= obj.set_zone(None, mode=the_mode, **ref_spec)
                except PanDeviceError as e:
                    module.fail_json(msg="Failed set_zone: {0}".format(e))
            if self.with_set_vlan_interface_reference:
                try:
                    result["changed"] |= obj.set_vlan_interface(None, **ref_spec)
                except PanDeviceError as e:
                    module.fail_json(msg="Failed set_vlan_interface: {0}".format(e))
            if self.with_set_vsys_reference:
                try:
                    result["changed"] |= obj.set_vsys(None, **ref_spec)
                except PanDeviceError as e:
                    module.fail_json(msg="Failed set_vsys: {0}".format(e))

            # Remove the config.
            for item in listing:
                if item.uid != obj.uid:
                    continue
                result["changed"] = True
                result["before"] = self.describe(item)
                result["after"] = None
                result["diff"] = {
                    "before": eltostr(item),
                    "after": "",
                }
                if not module.check_mode:
                    try:
                        obj.delete()
                    except PanDeviceError as e:
                        module.fail_json(msg="Failed delete: {0}".format(e))
                break
            else:
                result["before"] = None
                result["diff"] = {"before": ""}
        elif module.params["state"] == "merged":
            for item in listing:
                if item.uid != obj.uid:
                    continue
                result["before"] = self.describe(item)
                result["diff"] = {"before": eltostr(item)}
                # Doing item.apply() is faster from an API perspective, but may have
                # undesired side-effects if the object is a vsys importable and the vsys
                # has not been specified, so we'll just do item.update() for all changed
                # params.
                updated_params = set([])
                for key, obj_value in obj.about().items():
                    item_value = getattr(item, key, None)
                    if obj_value:
                        if isinstance(obj_value, list) or isinstance(item_value, list):
                            if not item_value:
                                item_value = []
                            if isinstance(obj_value, str):
                                obj_value = [obj_value]
                            # if current config or obj to create is one of the preset values
                            # (dropdown options in UI) then replace it with the obj value
                            # since values like "any" can not be in place with other values.
                            if (
                                preset_values := self.preset_values.get(key, None)
                            ) and (
                                set(item_value).issubset(preset_values)
                                or set(obj_value).issubset(preset_values)
                            ):
                                updated_params.add(key)
                                setattr(item, key, obj_value)
                            else:
                                for elm in obj_value:
                                    if elm not in item_value:
                                        updated_params.add(key)
                                        item_value.append(elm)
                                        setattr(item, key, item_value)
                        elif item_value != obj_value:
                            updated_params.add(key)
                            setattr(item, key, obj_value)
                if updated_params:
                    result["changed"] = True
                    result["after"] = self.describe(item)
                    result["diff"]["after"] = eltostr(item)
                    if not module.check_mode:
                        for param in updated_params:
                            try:
                                item.update(param)
                            except PanDeviceError as e:
                                module.fail_json(
                                    msg="Failed update {0}: {1}".format(param, e)
                                )
                break
            else:  # create new record with merge
                self.object_handling(obj, module)
                result["before"] = None
                result["after"] = self.describe(obj)
                result["diff"] = {
                    "before": "",
                    "after": eltostr(obj),
                }
                result["changed"] = True
                if not module.check_mode:
                    try:
                        obj.create()
                    except PanDeviceError as e:
                        module.fail_json(msg="Failed create: {0}".format(e))

            # Apply references.
            if self.with_set_vsys_reference and module.params[self.vsys_importable]:
                try:
                    result["changed"] |= obj.set_vsys(
                        module.params[self.vsys_importable],
                        **ref_spec,
                    )
                except PanDeviceError as e:
                    module.fail_json(msg="Failed set_vsys: {0}".format(e))
            if self.with_set_vlan_interface_reference and module.params["vlan_name"]:
                try:
                    result["changed"] |= obj.set_vlan_interface(
                        module.params["vlan_name"],
                        **ref_spec,
                    )
                except PanDeviceError as e:
                    module.fail_json(msg="Failed set_zone: {0}".format(e))
            if self.with_set_zone_reference and module.params["zone_name"]:
                the_mode = getattr(obj, "mode", self.default_zone_mode)
                try:
                    result["changed"] |= obj.set_zone(
                        module.params["zone_name"],
                        mode=the_mode,
                        **ref_spec,
                    )
                except PanDeviceError as e:
                    module.fail_json(msg="Failed set_zone: {0}".format(e))
            if self.with_set_vlan_reference and module.params["vlan_name"]:
                try:
                    result["changed"] |= obj.set_vlan(
                        module.params["vlan_name"],
                        **ref_spec,
                    )
                except PanDeviceError as e:
                    module.fail_json(msg="Failed set_zone: {0}".format(e))
            if self.with_set_virtual_router_reference and module.params["vr_name"]:
                try:
                    result["changed"] |= obj.set_virtual_router(
                        module.params["vr_name"],
                        **ref_spec,
                    )
                except PanDeviceError as e:
                    module.fail_json(msg="Failed set_virtual_router: {0}".format(e))
        elif module.params["state"] == "gathered":
            if module.params.get("gathered_filter", None):
                result["gathered"] = []
                result["gathered_xml"] = []
                for item in listing:
                    if self.matches_gathered_filter(
                        item, module.params["gathered_filter"]
                    ):
                        result["gathered"].append(self.describe(item))
                        item_xml = ""
                        try:
                            item_xml = eltostr(item)
                        except Exception as e:
                            item_xml = "Failed to gather XML: {0}".format(e)
                        finally:
                            result["gathered_xml"].append(item_xml)
            else:
                for item in listing:
                    if item.uid != obj.uid:
                        continue
                    result["gathered"] = self.describe(item)
                    try:
                        result["gathered_xml"] = eltostr(item)
                    except Exception as e:
                        result["gathered_xml"] = "Failed to gather XML: {0}".format(e)
                    break
                else:
                    module.fail_json(msg="Object '{0}' not found".format(obj.uid))
        else:
            for item in listing:
                if item.uid != obj.uid:
                    continue

                result["before"] = self.describe(item)
                result["diff"] = {"before": eltostr(item)}
                val = getattr(item, enabled_disabled_param)
                if invert_enabled_disabled:
                    val = not val

                if module.params["state"] == "enabled" and not val:
                    result["changed"] = True
                elif module.params["state"] == "disabled" and val:
                    result["changed"] = True

                if result["changed"]:
                    setattr(item, enabled_disabled_param, not val)
                    result["after"] = self.describe(item)
                    result["diff"]["after"] = eltostr(item)
                    if not module.check_mode:
                        try:
                            item.update(enabled_disabled_param)
                        except PanDeviceError as e:
                            module.fail_json(msg="Failed toggle: {0}".format(e))
                break
            else:
                module.fail_json(msg="Cannot enable/disable non-existing obj")

        return result

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
        improper_combo |= location in ("before", "after") and existing_rule is None
        improper_combo |= location in ("top", "bottom") and existing_rule is not None
        if improper_combo:
            module.fail_json(
                msg='Improper combination of "location" / "existing_rule".'
            )
        elif location is None:
            return False

        # Retrieve the current rules.
        try:
            rules = obj.__class__.refreshall(obj.parent, name_only=True)
        except PanDeviceError as e:
            module.fail_json(msg="Failed move refresh: {0}".format(e))

        listing = [x.uid for x in rules]
        try:
            obj_index = listing.index(uid)
            rule = rules[obj_index]
        except ValueError:
            module.fail_json(msg="Object {0} isn't present for move".format(uid))

        if location == "top":
            if listing[0] != uid:
                changed = True
        elif location == "bottom":
            if listing[-1] != uid:
                changed = True
        else:
            try:
                ref_index = listing.index(existing_rule)
            except ValueError:
                msg = [
                    "Cannot do relative rule placement",
                    '"{0}" does not exist.'.format(existing_rule),
                ]
                module.fail_json(msg="{0}".format(msg))
            if location == "before":
                if obj_index + 1 != ref_index:
                    changed = True
            elif location == "after":
                if ref_index + 1 != obj_index:
                    changed = True

        # Perform the move (if not check mode).
        if changed and not module.check_mode:
            try:
                rule.move(location, existing_rule)
            except PanDeviceError as e:
                module.fail_json(msg="Failed move: {0}".format(e))

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
            module.fail_json(msg="Failed commit: {0}".format(e))

        if not hasattr(self.device, "commit_all"):
            return committed

        dg_name = self.vsys_dg or self.device_group
        if dg_name is not None:
            dg_name = module.params[dg_name]

        if dg_name in (None, "shared"):
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
            module.fail_json(msg="Failed commit-all: {0}".format(e))

        return committed

    def describe(self, element):
        """Changes a pandevice object or list of objects into a dict / list of dicts.

        Args:
            element: Either a single pandevice object or a list of pandevice objects

        Returns:
            A dict if "element" was a single pandevice object, or a list of dicts
            if "element" was a list of pandevice objects.
        """
        if isinstance(element, list):
            return [self._describe(x) for x in element]

        return self._describe(element)

    def _describe(self, elm):
        ans = elm.about()

        for module_name, sdk_name in self.ansible_to_sdk_param_mapping.items():
            if module_name == sdk_name:
                continue
            ans[module_name] = ans.pop(sdk_name)

        return ans

    def _get_default_value(self, obj, key):
        """Returns default value for an sdk param in Ansible module.

        Args:
            obj: The pandevice object to fetch defaults from SDK.
            key: sdk param name to get default value for.

        Returns:
            Default value of sdk param if defined in Ansible module default_values or
            fetch from SDK defaults as a fallback.

        """
        # TODO get default values from pan-os-python SDK
        # obj._params is not public attribute on SDK which provide default values
        # either make it public accessible or provide a method
        # NOTE create a temp object with defaults and use values from this temp object
        # to fetch defaults for None values and set it for the object to create
        obj_default = obj.__class__()
        if (default_value := self.default_values.get(key, None)) is None:
            # set default value from SDK if not found in module default_values
            default_value = getattr(obj_default, key, None)

        return default_value

    def _shlex_split(self, logic):
        """Split string using shlex.split without escape char

        Escape char '\' is removed from shlex class to correctly process regex.
        """
        lex = shlex.shlex(logic, posix=True)
        lex.whitespace_split = True
        lex.commenters = ""
        lex.escape = ""

        return list(lex)

    def matches_gathered_filter(self, item, logic):
        """Returns True if the item and its contents matches the logic given.

        Args:
            item: A pan-os-python instance.
            logic (str): The logic to apply to the item.

        Returns:
            bool: True if the item matches the logic.
        """
        err_msg = "Improperly formatted logic string"
        logic = logic.strip()
        item_config = self._describe(item)

        if not logic:
            raise Exception("no logic given")

        if logic == "*":
            return True

        evaler = []

        pdepth = 0
        logic_tokens = self._shlex_split(logic)
        token_iter = iter(logic_tokens)
        while True:
            end_parens = 0
            try:
                field = next(token_iter)
            except StopIteration:
                break

            while True:
                if field.startswith("not("):
                    evaler.append("not")
                    field = field[3:]

                if field.startswith("!("):
                    evaler.extend(["not", "("])
                    field = field[2:]
                    pdepth += 1
                elif field.startswith("("):
                    evaler.append("(")
                    field = field[1:]
                    pdepth += 1
                else:
                    break

            if not field:
                continue
            elif field in ("&&", "and"):
                evaler.append("and")
                continue
            elif field in ("||", "or"):
                evaler.append("or")
                continue
            elif field == "not":
                evaler.append("not")
                continue

            while field.endswith(")"):
                end_parens += 1
                pdepth -= 1
                if pdepth < 0:
                    raise Exception(err_msg)
                field = field[:-1]

            if field.lower() == "true":
                evaler.append("True")
                field = ""
            elif field.lower() == "false":
                evaler.append("False")
                field = ""

            if not field:
                evaler.extend(")" * end_parens)
                continue
            elif end_parens:
                raise Exception(err_msg)
            elif field not in item_config:
                raise Exception("No field named {0}".format(field))

            try:
                operator = next(token_iter)
            except StopIteration:
                raise Exception(err_msg)

            operator_list = operator.split(")")
            operator = operator_list[0]
            if operator == "is-none":
                evaler.append("{0}".format(item_config[field] is None))
            elif operator == "is-not-none":
                evaler.append("{0}".format(item_config[field] is not None))
            elif operator == "is-true":
                evaler.append("{0}".format(bool(item_config[field])))
            elif operator == "is-false":
                evaler.append("{0}".format(not bool(item_config[field])))

            if operator in ["is-none", "is-not-none", "is-true", "is-false"]:
                evaler.extend(")" * (len(operator_list) - 1))
                pdepth -= len(operator_list) - 1
                continue

            if len(operator_list) != 1:
                raise Exception(err_msg)

            try:
                value = next(token_iter)
            except StopIteration:
                raise Exception(err_msg)

            while value.endswith(")"):
                end_parens += 1
                pdepth -= 1
                if pdepth < 0:
                    raise Exception(err_msg)
                value = value[:-1]
                if not value:
                    raise Exception(err_msg)

            if operator == "==":
                evaler.append("{0}".format("{0}".format(item_config[field]) == value))
            elif operator == "!=":
                evaler.append("{0}".format("{0}".format(item_config[field]) != value))
            elif operator == "<":
                evaler.append(
                    "{0}".format(
                        False if value is None else item_config[field] < float(value)
                    )
                )
            elif operator == "<=":
                evaler.append(
                    "{0}".format(
                        False if value is None else item_config[field] <= float(value)
                    )
                )
            elif operator == ">":
                evaler.append(
                    "{0}".format(
                        False if value is None else item_config[field] > float(value)
                    )
                )
            elif operator == ">=":
                evaler.append(
                    "{0}".format(
                        False if value is None else item_config[field] >= float(value)
                    )
                )
            elif operator == "contains":
                evaler.append("{0}".format(value in (item_config[field] or [])))
            elif operator == "does-not-contain":
                evaler.append("{0}".format(value not in (item_config[field] or [])))
            elif operator == "starts-with":
                evaler.append(
                    "{0}".format((item_config[field] or "").startswith(value))
                )
            elif operator == "does-not-start-with":
                evaler.append(
                    "{0}".format(not (item_config[field] or "").startswith(value))
                )
            elif operator == "ends-with":
                evaler.append("{0}".format((item_config[field] or "").endswith(value)))
            elif operator == "does-not-end-with":
                evaler.append(
                    "{0}".format(not (item_config[field] or "").endswith(value))
                )
            elif operator == "matches-regex":
                evaler.append(
                    "{0}".format(
                        re.search(value, (item_config[field] or "")) is not None
                    )
                )
            elif operator == "does-not-match-regex":
                evaler.append(
                    "{0}".format(re.search(value, (item_config[field] or "")) is None)
                )
            elif operator == "contains-regex":
                prog = re.compile(value)
                evaler.append(
                    "{0}".format(
                        any(prog.search(x) for x in (item_config[field] or []))
                    )
                )
            elif operator == "does-not-contain-regex":
                prog = re.compile(value)
                evaler.append(
                    "{0}".format(
                        not any(prog.search(x) for x in (item_config[field] or []))
                    )
                )
            else:
                raise Exception("Unknown operator: {0}".format(operator))

            evaler.extend(")" * end_parens)

        if pdepth != 0:
            raise Exception("Parenthesis depth is inequal: {0}".format(pdepth))

        return bool(eval(" ".join(evaler)))


def get_connection(
    vsys=None,
    vsys_shared=None,
    device_group=None,
    vsys_dg=None,
    vsys_importable=None,
    rulebase=None,
    template=None,
    template_stack=None,
    with_classic_provider_spec=False,
    with_state=False,
    with_enabled_state=False,
    argument_spec=None,
    with_network_resource_module_state=False,
    with_network_resource_module_enabled_state=False,
    required_one_of=None,
    min_pandevice_version=None,
    min_panos_version=None,
    min_panos_upgrade_assurance_version=None,
    error_on_firewall_shared=False,
    panorama_error=None,
    firewall_error=None,
    template_is_optional=False,
    helper_cls=None,
    sdk_cls=None,
    parents=None,
    sdk_params=None,
    extra_params=None,
    default_values=None,
    preset_values=None,
    reference_operations=None,
    ansible_to_sdk_param_mapping=None,
    with_uuid=False,
    with_commit=False,
    with_target=False,
    with_movement=False,
    with_audit_comment=False,
    with_gathered_filter=False,
    with_update_in_apply_state=False,
    with_set_vlan_reference=False,
    with_set_vsys_reference=False,
    with_set_zone_reference=False,
    with_set_virtual_router_reference=False,
    with_set_vlan_interface_reference=False,
    virtual_router_reference_default="default",
    default_zone_mode=None,
):
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
        argument_spec(dict): The argument spec to mixin with the generated spec based
            on the given parameters.  This cannot be specified if sdk_params is specified.
        with_network_resource_module_state(bool): Include 'state',
            but also the network resource module
            states of "merged", "replaced", "deleted", and "gathered".
        with_network_resource_module_enabled_state(bool): Includes
            the `with_network_resource_module_state` values, but also
            support "enabled" and "disabled" as valid states.
        required_one_of(list): List of lists to extend into required_one_of.
        min_pandevice_version(tuple): Minimum pandevice version allowed.
        min_panos_version(tuple): Minimum PAN-OS version allowed.
        min_panos_upgrade_assurance_version(tuple): Minimum panos-upgrade-assurance package version.
        error_on_firewall_shared(bool): Don't allow "shared" vsys.
        panorama_error(str): The error message if the device is Panorama.
        firewall_error(str): The error message if the device is a firewall.
        template_is_optional(bool): Set this to True if the config object could
            be local on Panorama and not just in a template or template stack.
        helper_cls: The helper class to instantiate, when a module requires overridden
            functionality.
        sdk_cls(tuple): The SDK class that this module will manipulate, where the
            first element is the package name (e.g. - "objects") and the second element
            is the class name (e.g. - "AddressObject").
        parents(tuple): Tuple of length 3 or 4.  First element is a string of the
            SDK package name (e.g. - "network").  Second element is a string of the
            class in the package (e.g. - "VirtualRouter").  If the class is a singleton
            that does not have a NAME defined (such as panos.policies.Rulebase), then
            the 3rd param in the tuple should be `None`.  If the class is not a singleton,
            then the 3rd param should be a string which should be added into the final
            argument spec as a required param.  If a fourth element is present, then
            instead of the 3rd param being required, it will be optional and have a
            default value of the fourth element.
        sdk_params(dict): List of params that exist in the sdk_cls that should be present
            in the argument_spec of the module.
        extra_params(dict): List of params that should be present in the argument_spec,
            but aren't params in the specified sdk_cls object.
        reference_operations(tuple): Listing of reference operations to run before / after
            apply_state().
        ansible_to_sdk_param_mapping(dict): A dict where the key is the ansible param
            name and the value is the class' param name.  Used both for CRUD operations
            as well as for `state=gathered`.
        with_uuid(bool): Include UUID in the spec (for panos.policies objects).
        with_commit(bool): Include the commit boolean, which is deprecated.
        with_target(bool): Include target and negate_target in the spec (for
            panos.policies objects).
        with_movement(bool): This is a rule module, so move the rule into place.
        with_audit_comment(bool): This is a rule module, so perform audit comment
            operations.
        with_gathered_filter(bool): Include `gathered_filter` param for network resource modules.
        with_update_in_apply_state(bool): `apply_state()` should do `.update(param)` on
            changes instead of `obj.apply()`.
        with_set_vlan_reference(bool): Module should do `set_vlan()` in apply_state().
        with_set_vsys_reference(bool): Module should do `set_vsys()` in apply_state().
        with_set_zone_reference(bool): Module should do `set_zone()` in apply_state().
        with_set_virtual_router_reference(bool): Module should do `set_virtual_router()`
            in apply_state().
        with_set_vlan_interface_reference(bool): Module should do `set_vlan_interface()`
            in apply_state().
        virtual_router_reference_default(str): The default value for the virtual router
            reference.
        default_zone_mode(str): The default zone mode when with_set_zone_reference=True.

    Returns:
        ConnectionHelper
    """
    if helper_cls is None:
        helper_cls = ConnectionHelper

    helper = helper_cls(
        min_pandevice_version,
        min_panos_version,
        min_panos_upgrade_assurance_version,
        error_on_firewall_shared,
        panorama_error,
        firewall_error,
        template_is_optional,
    )
    req = []
    renames = {}
    spec = {
        "provider": {
            "required": True,
            "type": "dict",
            "required_one_of": [
                ["password", "api_key"],
            ],
            "options": {
                "ip_address": {"required": True},
                "username": {"default": "admin"},
                "password": {"no_log": True},
                "api_key": {"no_log": True},
                "port": {"default": 443, "type": "int"},
                "serial_number": {"no_log": True},
            },
        },
    }

    if with_classic_provider_spec:
        spec["provider"]["required"] = False
        spec["provider"]["options"]["ip_address"]["required"] = False
        del spec["provider"]["required_one_of"]
        spec.update(
            {
                "ip_address": {"required": False},
                "username": {"default": "admin"},
                "password": {"no_log": True},
                "api_key": {"no_log": True},
                "port": {"default": 443, "type": "int"},
            }
        )
        req.extend(
            [
                ["provider", "ip_address"],
                ["provider", "password", "api_key"],
            ]
        )

    if with_state:
        spec["state"] = {
            "default": "present",
            "choices": ["present", "absent"],
        }

    if with_enabled_state:
        spec["state"] = {
            "default": "present",
            "choices": ["present", "absent", "enabled", "disabled"],
        }

    if with_network_resource_module_state:
        spec["state"] = {
            "default": "present",
            "choices": [
                "present",
                "absent",
                "merged",
                "replaced",
                "deleted",
                "gathered",
            ],
        }

    if with_network_resource_module_enabled_state:
        spec["state"] = {
            "default": "present",
            "choices": [
                "present",
                "absent",
                "merged",
                "replaced",
                "deleted",
                "gathered",
                "enabled",
                "disabled",
            ],
        }

    if with_uuid:
        helper.with_uuid = True
        if "uuid" in spec:
            raise KeyError("uuid already in the spec")
        spec["uuid"] = {}

    if with_commit:
        helper.with_commit = True
        if "commit" in spec:
            raise KeyError("commit already in spec")
        spec["commit"] = {"type": "bool"}

    if with_target:
        helper.with_target = True
        if "target" in spec or "negate_target" in spec:
            raise KeyError("target and/or negate_target already in the spec")
        spec["target"] = {"type": "list", "elements": "str"}
        spec["negate_target"] = {"type": "bool"}

    if with_movement:
        helper.with_movement = True
        if "location" in spec or "existing_rule" in spec:
            raise KeyError("cannot add 'location' or 'existing_rule' for with_movement")
        spec["location"] = {
            "choices": ["top", "bottom", "before", "after"],
        }
        spec["existing_rule"] = {}

    if with_audit_comment:
        if "audit_comment" in spec:
            raise KeyError("audit_comment is already in the spec")
        helper.with_audit_comment = True
        spec["audit_comment"] = {}

    if vsys_dg is not None:
        if isinstance(vsys_dg, bool):
            param = "vsys_dg"
        else:
            param = vsys_dg
        spec[param] = {}
        helper.vsys_dg = param
    else:
        if vsys is not None:
            if isinstance(vsys, bool):
                param = "vsys"
            else:
                param = vsys
            spec[param] = {"default": "vsys1"}
            helper.vsys = param
        if device_group is not None:
            if isinstance(device_group, bool):
                param = "device_group"
            else:
                param = device_group
            spec[param] = {"default": "shared"}
            helper.device_group = param
        if vsys_importable is not None:
            if vsys is not None:
                raise KeyError('Define "vsys" or "vsys_importable", not both.')
            if isinstance(vsys_importable, bool):
                param = "vsys"
            else:
                param = vsys_importable
            spec[param] = {}
            helper.with_import_support = True
            helper.vsys_importable = param
        if vsys_shared is not None:
            if vsys is not None:
                raise KeyError('Define "vsys" or "vsys_shared", not both.')
            elif vsys_importable is not None:
                raise KeyError('Define "vsys_importable" or "vsys_shared", not both.')
            if isinstance(vsys_shared, bool):
                param = "vsys"
            else:
                param = vsys_shared
            spec[param] = {"default": "shared"}
            helper.vsys_shared = param

    if rulebase is not None:
        if isinstance(rulebase, bool):
            param = "rulebase"
        else:
            param = rulebase
        if param in spec:
            raise KeyError("rulebase param {0} already in spec".format(param))
        spec[param] = {
            "default": None,
            "choices": ["pre-rulebase", "rulebase", "post-rulebase"],
        }
        helper.rulebase = param

    if template is not None:
        if isinstance(template, bool):
            param = "template"
        else:
            param = template
        spec[param] = {}
        helper.template = param

    if template_stack is not None:
        if isinstance(template_stack, bool):
            param = "template_stack"
        else:
            param = template_stack
        spec[param] = {}
        helper.template_stack = param

    if parents is not None:
        if not isinstance(parents, tuple):
            raise Exception("parents should be a tuple")
        for num, x in enumerate(parents):
            if not isinstance(x, tuple):
                raise Exception("index {0}: is not a tuple".format(num))
            elif len(x) != 3 and len(x) != 4:
                raise Exception("index {0}: must be len-3 or len-4".format(num))
            elif len(x) == 4 and x[2] is None:
                raise Exception("index {0}: no name but has a default".format(num))
            parent_param_name = x[2]
            if parent_param_name is not None:
                if parent_param_name in spec:
                    raise KeyError(
                        "parent param {0}: already in spec".format(parent_param_name)
                    )
                ps = {}
                if len(x) == 3:
                    ps = {"required": True}
                else:
                    ps = {"default": x[3]}
                spec[parent_param_name] = ps
        helper.parents = parents

    if ansible_to_sdk_param_mapping is not None:
        if not isinstance(ansible_to_sdk_param_mapping, dict):
            raise Exception("ansible_to_sdk_param_mapping should be a dict")
        for ansible_param, sdk_param in ansible_to_sdk_param_mapping.items():
            if ansible_param in renames:
                raise KeyError(
                    "param mapping {0} already present".format(ansible_param)
                )
            renames[ansible_param] = sdk_param

    if argument_spec is not None and sdk_params is not None:
        raise Exception("either specify argument_spec or sdk_params, not both")

    if argument_spec is not None:
        for k in argument_spec.keys():
            if k in spec:
                raise KeyError("{0} is already present in argument_spec".format(k))
            spec[k] = argument_spec[k]

    if sdk_params is not None:
        if not isinstance(sdk_params, dict):
            raise Exception("sdk_params should be a dict")
        for k in sdk_params.keys():
            if k in spec:
                raise KeyError("sdk_param {0}: already in spec".format(k))
            try:
                sdk_name = sdk_params[k].pop("sdk_param")
            except KeyError:
                pass
            else:
                if k in renames and renames[k] != sdk_name:
                    raise Exception(
                        "param mapping {0} already present and different".format(k)
                    )
                renames[k] = sdk_name
            spec[k] = sdk_params[k]
        helper.sdk_params = sdk_params
        if preset_values is not None:
            helper.preset_values = preset_values
        if default_values is not None:
            helper.default_values = default_values

    if with_gathered_filter:
        if "gathered_filter" in spec:
            raise KeyError("cannot add 'gathered_filter' for with_gathered_filter")
        if sdk_params is None:
            raise Exception("with_gathered_filter requires sdk_params to be specified")
        helper.with_gathered_filter = True
        spec["gathered_filter"] = {}
        for k in sdk_params.keys():
            if spec[k].get("required", False):
                req.append(["gathered_filter", k])
                spec[k]["required"] = False

    if extra_params is not None:
        if not isinstance(extra_params, dict):
            raise Exception("extra_params should be a dict")
        for k in extra_params.keys():
            if k in spec:
                raise KeyError("extra param {0}: already in spec".format(k))
            spec[k] = extra_params[k]
        helper.extra_params = extra_params

    if with_set_zone_reference:
        if "zone_name" in spec:
            raise Exception("setref: spec already contains 'zone_name'")
        spec["zone_name"] = {}
        helper.with_set_zone_reference = True
        helper.default_zone_mode = default_zone_mode

    if with_set_vlan_reference:
        if "vlan_name" in spec:
            raise Exception("setref: spec already contains 'vlan_name'")
        spec["vlan_name"] = {}
        helper.with_set_vlan_reference = True

    if with_set_vsys_reference:
        if not helper.vsys_importable:
            raise Exception(
                "setref: with_set_vsys_reference requires vsys_importable=True"
            )
        helper.with_set_vsys_reference = True

    if with_set_virtual_router_reference:
        if "vr_name" in spec:
            raise Exception("setref: spec already contains 'vr_name'")
        spec["vr_name"] = {}
        if virtual_router_reference_default is not None:
            spec["vr_name"]["default"] = virtual_router_reference_default
        helper.with_set_virtual_router_reference = True

    if with_set_vlan_interface_reference:
        if "vlan_name" in spec:
            raise Exception("setref: spec already contains 'vlan_name'")
        spec["vlan_name"] = {}
        helper.with_set_vlan_interface_reference = True

    if required_one_of is not None:
        req.extend(required_one_of)

    # Done.
    helper.with_update_in_apply_state = with_update_in_apply_state
    helper.sdk_cls = sdk_cls
    helper.argument_spec = spec
    helper.required_one_of = req
    helper.ansible_to_sdk_param_mapping = renames
    return helper


class PanOSAnsibleModule(AnsibleModule):
    def __init__(
        self,
        argument_spec,
        api_endpoint=None,
        with_state=False,
        with_enabled_state=False,
        *args,
        **kwargs,
    ):
        spec = {}

        self.api_endpoint = api_endpoint

        if with_state:
            spec["state"] = {"default": "present", "choices": ["present", "absent"]}

        if with_enabled_state:
            spec["state"] = {
                "default": "present",
                "choices": ["present", "absent", "enabled", "disabled"],
            }

        argument_spec.update(spec)

        super().__init__(argument_spec, *args, **kwargs)

        self.connection = Connection(self._socket_path)


def cmd_xml(cmd):
    def _cmd_xml(args, obj):
        if not args:
            return
        arg = args.pop(0)
        if args:
            result = re.search(r'^"(.*)"$', args[0])
            if result:
                obj.append("<%s>" % arg)
                obj.append(result.group(1))
                obj.append("</%s>" % arg)
                args.pop(0)
                _cmd_xml(args, obj)
            else:
                obj.append("<%s>" % arg)
                _cmd_xml(args, obj)
                obj.append("</%s>" % arg)
        else:
            obj.append("<%s>" % arg)
            _cmd_xml(args, obj)
            obj.append("</%s>" % arg)

    args = cmd.split()
    obj = []
    _cmd_xml(args, obj)
    xml = "".join(obj)

    return xml


def get_nested_key(d, key_list):
    """
    Access a nested key within a dictionary safely.

    Example:

    For the dictionary d = {'one': {'two': {'three': 'four'}}},
    get_nested_key(d, ['one', 'two', 'three']) will return 'four'.

    :param d: Dictionary
    :param key_list: List of keys, in decending order.
    """

    return reduce(lambda val, key: val.get(key) if val else None, key_list, d)
