# Ansible Collection - uofuchpc.cmdb

> **_IMPORTANT:_** This repository has been deprecated in favor of its GitLab counterpart.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A simple Ansible Collection for a Content Management Database (CMDB).

## Supported Versions of Ansible

This collection has been tested against following Ansible versions: `>=2.15`.

## Included content
<!--start collection content-->
### Dynamic Inventories
Name | Description
--- | ---
[uofuchpc.cmdb.portal](https://github.com/CHPC-UofU/uofuchpc.cmdb/tree/main/docs/uofuchpc.cmdb.portal_inventory.rst)|A simple inventory plugin for the CHPC web portal.
<!--end collection content-->

## Installing this Collection

You can locally build and install the `uofuchpc.cmdb` collection with the Ansible Galaxy CLI:

```console
$ mkdir ./build
$ ansible-galaxy collection build -f . --output-path build
...
$ ansible-galaxy collection install build/uofuchpc-cmdb-X.X.X.tar.gz --force
...
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
collections:
  - name: https://github.com/CHPC-UofU/uofuchpc.cmdb/releases/download/v<release>/uofuchpc-cmdb-<release>.tar.gz
    type: url
```

## Using this Collection

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.
