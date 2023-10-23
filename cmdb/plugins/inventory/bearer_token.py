from ansible.errors import AnsibleError
from ansible.module_utils.common.text.converters import to_native
from ansible.plugins.inventory import BaseInventoryPlugin
import requests

ANSIBLE_METADATA = {
    'metadata_version': '0.0.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: bearer_token
plugin_type: inventory
short_description: "A simple inventory plugin for a CMDB and bearer token."
version_added: "0.0.1"
description:
  - "A simple inventory plugin for a CMDB and bearer token."
options:
  cmdb_api_url:
    description: "API URL for the CMDB."
    ini:
      - section: cmdb
        key: cmdb_api_url
    env:
      - name: CMDB_API_URL
    required: True
    type: string
  cmdb_api_bearer_token:
    description: Bearer token for the CMDB API.
    ini:
      - section: cmdb
        key: cmdb_api_bearer_token
    env:
      - name: CMDB_API_BEARER_TOKEN
    required: True
    type: string
author:
  - UofU CHPC
'''


class InventoryModule(BaseInventoryPlugin):
    """A simple inventory plugin for a CMDB and bearer token."""

    NAME = 'uofuchpc.cmdb.bearer_token'

    def verify_file(self, path):

        # Unused, always return True
        return True

    def _fetch_inventory_data(self):
        headers = {
            "Authorization": f"Bearer {self.get_option('cmdb_api_bearer_token')}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(self.get_option('cmdb_api_url'), headers=headers)

            if response.status_code == 200:
                data = response.json()
                return data
            else:
                raise AnsibleError(f"Failed to fetch JSON inventory data from CMDB: {self.get_option('cmdb_api_url')}.")
        except Exception as e:
            raise AnsibleError(f"An error occurred, the original exception is: {to_native(e)}")

    def parse(self, inventory, *args, **kwargs):

        # The following invocation supports Python 2 in case we are
        # still relying on it. Use the more convenient, pure Python 3 syntax
        # if you don't need it.
        super(InventoryModule, self).parse(inventory, *args, **kwargs)

        raw_data = self._fetch_inventory_data()
        # _meta = raw_data.pop('_meta')
        for group_name, group_data in raw_data.items():
            for host_name in group_data['hosts']:
                self.inventory.add_host(host_name)
                # for var_key, var_val in _meta['hostvars'][host_name].items():
                #     self.inventory.set_variable(host_name, var_key, var_val)
