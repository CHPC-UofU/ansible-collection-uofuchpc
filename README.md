# Ansible Collection - uofuchpc.cmdb

A simple collection for a Content Management Database (CMDB).

## Resources

* [Write your own Red Hat Ansible Tower inventory plugin](https://developers.redhat.com/blog/2021/03/10/write-your-own-red-hat-ansible-tower-inventory-plugin#)
* [How to Write an Inventory Import Script](https://uofu.app.box.com/file/1326767497658?s=8vc2x761npatscf0zfj6z0jc7xque5ev)
* [Creating custom dynamic inventories for Ansible](https://www.jeffgeerling.com/blog/creating-custom-dynamic-inventories-ansible)
* [Inventories](https://docs.ansible.com/ansible-tower/latest/html/userguide/inventories.html)
* [Inventory File Importing](https://docs.ansible.com/ansible-tower/3.8.6/html/administration/scm-inv-source.html#ag-inv-import)
* [Custom Credential Types](https://docs.ansible.com/ansible-tower/3.8.6/html/userguide/credential_types.html#ug-credential-types)
* [GitHub: amazon.aws/plugins/inventory/aws_ec2.py](https://github.com/ansible-collections/amazon.aws/blob/main/plugins/inventory/aws_ec2.py)
* [Inventory plugins](https://docs.ansible.com/ansible/latest/plugins/inventory.html)
* [How to write an Ansible plugin to create inventory files](https://www.redhat.com/sysadmin/ansible-plugin-inventory-files)
* [Ansible Dynamic Inventory Using Plugins](https://blog.networktocode.com/post/Ansible-Dynamic-Inventory-using-Plugins/)
* [Developing plugins](https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#developing-plugins)
* [Developing dynamic inventory](https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html)

## Testing

Build and install the collection locally:

```console
$ mkdir ./build
$ ansible-galaxy collection build -f . --output-path build
...
$ ansible-galaxy collection install build/uofuchpc-cmdb-X.X.X.tar.gz --force
...
```

Test the collection by un-commenting the content in `./ansible.cfg` and:

```console
$ export CMDB_API_BEARER_TOKEN=<value>
$ export CMDB_API_URL=<value>
$ ansible-doc -t inventory uofuchpc.cmdb.portal
...
$ ansible-inventory --list -i demo.portal.yml
...
```
