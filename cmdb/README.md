# Ansible Collection - uofuchpc.cmdb

A simple collection for a CMDB.

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

````console
$ ansible-galaxy collection build -f ./cmdb/ --output-path build
...
$ ansible-galaxy collection install build/uofuchpc-cmdb-0.0.2.tar.gz --force
...
$ ansible-doc -t inventory uofuchpc.cmdb.bearer_token
...
$ ansible-inventory --list -i demo.bearer_token.yml
...
````