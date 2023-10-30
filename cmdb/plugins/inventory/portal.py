import json
import os.path

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.module_utils.common.text.converters import to_native
from ansible.plugins.inventory import BaseInventoryPlugin

ANSIBLE_METADATA = {
    'metadata_version': '0.0.5',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r"""
name: bearer_token
plugin_type: inventory
version_added: "0.0.1"
authors:
  - UofU CHPC <helpdesk@chpc.utah.edu>
short_description: "A simple inventory plugin for a CMDB and bearer token."
description:
  - "A simple inventory plugin for a CMDB and bearer token."
  - Uses a YAML configuration file that ends with bearer_token.(yml|yaml)
requirements:
  - "Python >= 3.9"
  - "requests >= 2.31"
extends_documentation_fragment:
  - constructed
options:
  cmdb_api_bearer_token:
    description: Bearer token for the CMDB API.
    ini:
      - section: cmdb
        key: cmdb_api_bearer_token
    env:
      - name: CMDB_API_BEARER_TOKEN
    required: True
    type: str
  cmdb_api_url:
    description: "API URL for the CMDB."
    ini:
      - section: cmdb
        key: cmdb_api_url
    env:
      - name: CMDB_API_URL
    required: True
    type: str
"""

EXAMPLES = r"""
# Minimal example using environment vars
# Fetch all hosts returned by the CMDB
plugin: uofuchpc.cmdb.portal

# Minimal example using a cmdb_api_bearer_token and cmdb_api_url
# Fetch all hosts returned by the CMDB
plugin: uofuchpc.cmdb.portal
cmdb_api_bearer_token: "123456abcdefgH"
cmdb_api_url: "https://api.example.com/route/"
"""

try:
    # jsonschema is required for validating the CMDB API endpoint
    from jsonschema import validate

    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

try:
    # requests is required for connecting to the CMDB
    import requests

    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class InventoryModule(BaseInventoryPlugin):
    """A simple inventory plugin for a CMDB and bearer token."""

    NAME = 'bearer_token'

    def __init__(self):
        self._check_requirements()
        super(InventoryModule, self).__init__()

    @staticmethod
    def _check_requirements():
        """
        Check all requirements for this inventory are satisfied.
        """

        if not HAS_JSONSCHEMA:
            raise AnsibleParserError('Please install "jsonschema" Python module as this is required'
                                     ' for validating this dynamic inventory plugin.')

        if not HAS_REQUESTS:
            raise AnsibleParserError('Please install "requests" Python module as this is required'
                                     ' for this dynamic inventory plugin.')

    @staticmethod
    def _load_inventory_data(cmdb_api_url: str, cmdb_api_bearer_token: str):
        """
        Load the inventory from the CMDB
        :param cmdb_api_url: URL for the CMDB API endpoint
        :param cmdb_api_bearer_token: Bearer token
        :return: JSON
        """
        headers = {
            "Authorization": f"Bearer {cmdb_api_bearer_token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(cmdb_api_url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                return data
            else:
                raise AnsibleError(f"Failed to fetch JSON inventory data from CMDB: {cmdb_api_url}.")
        except Exception as e:
            raise AnsibleError(f"An error occurred, the original exception is: {to_native(e)}")

    def verify_file(self, path):
        """
        Verify the plugin configuration file
        :param path: path of the configuration YAML file
        :return: True if everything is correct, otherwise False
        """

        valid = False
        if super(InventoryModule, self).verify_file(path):
            if path.endswith((self.NAME + ".yaml", self.NAME + ".yml")):
                valid = True
        return valid

    def parse(self, inventory, loader, path, cache=False):
        """
        Parses the inventory file
        """

        super(InventoryModule, self).parse(inventory, loader, path, cache=cache)
        self._read_config_data(path)

        cmdb_api_bearer_token = self.get_option('cmdb_api_bearer_token')
        cmdb_api_url = self.get_option('cmdb_api_url')

        raw_data = self._load_inventory_data(cmdb_api_url, cmdb_api_bearer_token)
        self.display.vvv(to_native(raw_data))

        # Validate the data:
        schema_file = open(os.path.join(os.path.dirname(__file__),
                                        '..', 'plugin_utils', 'portal-cmdb-schema.json'))
        schema = json.load(schema_file)
        try:
            validate(instance=raw_data, schema=schema)
        except Exception as e:
            raise AnsibleError(f"An error occurred, the original exception is: {to_native(e)}")

        # Sort the data:
        sorted_data = sorted(raw_data['hosts'], key=lambda item: item['address'])

        # Add groups:
        host_groups = []
        for host in sorted_data:
            for key, val in host['attrs'].items():
                if key == 'tags' and isinstance(val, list):
                    host_groups = host_groups + val
        host_groups = list(set(host_groups))
        for group in host_groups:
            self.inventory.add_group(group)

        # Add hosts:
        for host in sorted_data:
            hostname = host['address']
            self.inventory.add_host(hostname, group='all')
            self.inventory.set_variable(hostname, 'ansible_host', hostname)

            for key, val in host['attrs'].items():
                if key == 'tags' and isinstance(val, list):
                    for tag in val:
                        self.inventory.add_host(hostname, group=tag)
                else:
                    self.inventory.set_variable(hostname, key, val)
