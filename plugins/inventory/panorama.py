#!/usr/bin/python

""" Dynamic inventory from Palo Alto Panorama """

import xml.etree.ElementTree as ET
import requests
import urllib3
from ansible.plugins.inventory import BaseInventoryPlugin

DOCUMENTATION = r"""
    name: panorama
    plugin_type: inventory
    short_description: Dynamic inventory from Palo Alto Panorama
    description: Get devices and groups from Palo Alto Panorama
    author:
        - Konstantin Kuminsky (@kk-at-redhat)
    options:
        plugin:
            description: Name of the plugin
            type: str
            required: true
        panorama_address:
            description: Panorama IP address or FQDN
            type: str
            required: false
            env:
              - name: PANORAMA_ADDRESS
        panorama_username:
            description: Panorama username
            type: str
            required: false
            env:
              - name: PANORAMA_USERNAME
        panorama_password:
            description: Panorama password
            type: str
            required: false
            env:
              - name: PANORAMA_PASSWORD
        additional_marker_key:
            description: Name of the variable name to be added to each host
            type: str
            required: false
        additional_marker_value:
            description: Value of the variable value to be added to each host
            type: str
            required: false
"""

EXAMPLES = r"""
plugin: "panorama"

additional_marker_key: "device"
additional_marker_value: "firewall"
"""

class InventoryModule(BaseInventoryPlugin):
    """ Ansible Inventory Module class"""
    NAME = "panorama"

    def verify_file(self, path):
        return path.endswith(("yml","yaml"))

    def _make_api_request(self, url):
        urllib3.disable_warnings()
        response = requests.get(url, verify=False, timeout=10)
        if response.status_code == 200:
            return response.text
        response.raise_for_status()
        return None

    def _get_api_key(self, panorama_address, panorama_username, panorama_password):
        endpoint = (
            f"https://{panorama_address}/api/?type=keygen&"
            f"user={panorama_username}"
            f"&password={panorama_password}"
            )
        api_response = self._make_api_request(endpoint)
        root = ET.fromstring(api_response)
        return root.find(".//key").text

    def _get_xml_data(self, panorama_address, query, panorama_api_key):
        endpoint = (
            f"https://{panorama_address}/api/?type=op&cmd="
            f"{query}&"
            f"key={panorama_api_key}"
            )
        xml_response = self._make_api_request(endpoint)
        root = ET.fromstring(xml_response)
        return root

    def _get_devices(self, panorama_address, panorama_api_key):
        devices_query = "<show><devices><all></all></devices></show>"
        devices_endpoint = self._get_xml_data(panorama_address, devices_query, panorama_api_key)
        devices = []
        for device in devices_endpoint.findall("./result/devices/entry"):
            device_model = getattr(device.find("model"), "text", "")
            device_version = getattr(device.find("sw-version"), "text", "")
            device_hostname = getattr(device.find("hostname"), "text", "")
            device_ipaddress = getattr(device.find("ip-address"), "text", "")
            if device_hostname and device_ipaddress:
                device_info = {"hostname": device_hostname,
                               "ip_address": device_ipaddress,
                               "model": device_model,
                               "version": device_version}
                devices.append(device_info)
        return devices

    def _get_device_groups(self, panorama_address, panorama_api_key):
        device_groups_query = "<show><devicegroups></devicegroups></show>"
        device_groups_endpoint = self._get_xml_data(panorama_address,
                                                    device_groups_query,
                                                    panorama_api_key)
        device_groups = []
        for device_group in device_groups_endpoint.findall("./result/devicegroups/entry"):
            if device_group.find("./devices"):
                for entry in device_group.findall("./devices/entry"):
                    device_hostname = getattr(entry.find("hostname"), "text", "")
                    if device_hostname:
                        devices_and_groups = {"hostname": device_hostname,
                                              "group": device_group.get("name")}
                        device_groups.append(devices_and_groups)
        return device_groups

    def _get_nested_groups(self, panorama_address, panorama_api_key):
        nested_groups_query = "<show><config><candidate></candidate></config></show>"
        nested_groups_endpoint = self._get_xml_data(panorama_address,
                                                    nested_groups_query,
                                                    panorama_api_key)
        nested_groups = []
        nested_groups_path = "./result/config/readonly/devices/entry/device-group/entry"
        for nested_group in nested_groups_endpoint.findall(nested_groups_path):
            parent_group = getattr(nested_group.find("parent-dg"), "text", "")
            if parent_group:
                parents_and_children = {"parent_group": parent_group,
                                        "child_group": nested_group.get("name")}
                nested_groups.append(parents_and_children)
        return nested_groups

    def parse(self, inventory, loader, path, cache=True):
        super().parse(inventory, loader, path, cache)

        self._read_config_data(path)
        additional_marker_key = self.get_option("additional_marker_key")
        additional_marker_value = self.get_option("additional_marker_value")
        panorama_address = self.get_option("panorama_address")
        panorama_username = self.get_option("panorama_username")
        panorama_password = self.get_option("panorama_password")

        panorama_api_key = self._get_api_key(panorama_address, panorama_username, panorama_password)

        for device in self._get_devices(panorama_address, panorama_api_key):
            self.inventory.add_host(device["hostname"])
            self.inventory.set_variable(device["hostname"], "ansible_host", device["ip_address"])
            self.inventory.set_variable(device["hostname"], "model", device["model"])
            self.inventory.set_variable(device["hostname"], "version", device["version"])
            if additional_marker_key and additional_marker_value:
                self.inventory.set_variable(device["hostname"],
                                            additional_marker_key,
                                            additional_marker_value)

        for device_group in self._get_device_groups(panorama_address, panorama_api_key):
            self.inventory.add_group(device_group["group"])
            self.inventory.add_host(device_group["hostname"], group=device_group["group"])

        for nested_group_pair in self._get_nested_groups(panorama_address, panorama_api_key):
            self.inventory.add_group(nested_group_pair["parent_group"])
            self.inventory.add_group(nested_group_pair["child_group"])
            self.inventory.add_child(nested_group_pair["parent_group"],
                                     nested_group_pair["child_group"])
