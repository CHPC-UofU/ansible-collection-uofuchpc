from ansible.errors import AnsibleError, AnsibleParserError
from ansible.module_utils.common.text.converters import to_native
from ansible.plugins.inventory import BaseInventoryPlugin

# import requests

ANSIBLE_METADATA = {
    'metadata_version': '0.0.1',
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
plugin: uofuchpc.cmdb.bearer_token

# Minimal example using a cmdb_api_bearer_token and cmdb_api_url
# Fetch all hosts returned by the CMDB
plugin: uofuchpc.cmdb.bearer_token
cmdb_api_bearer_token: "123456abcdefgH"
cmdb_api_url: "https://portal.example.com/route/"
"""

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

        if not HAS_REQUESTS:
            raise AnsibleParserError('Please install "requests" Python module as this is required'
                                     ' for this dynamic inventory plugin.')

    @staticmethod
    def _fetch_inventory_data(cmdb_api_url: str, cmdb_api_bearer_token: str):
        """
        Fetch the inventory data
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

        super(InventoryModule, self).parse(inventory, loader, path, cache)
        self._read_config_data(path)

        cmdb_api_bearer_token = self.get_option('cmdb_api_bearer_token')
        cmdb_api_url = self.get_option('cmdb_api_url')

        raw_data = self._fetch_inventory_data(cmdb_api_url, cmdb_api_bearer_token)
        # _meta = raw_data.pop('_meta')
        for group_name, group_data in raw_data.items():
            for host_name in group_data['hosts']:
                self.inventory.add_host(host_name)
                # for var_key, var_val in _meta['hostvars'][host_name].items():
                #     self.inventory.set_variable(host_name, var_key, var_val)
