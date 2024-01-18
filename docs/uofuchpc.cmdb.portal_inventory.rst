
uofuchpc.cmdb.portal
==============================

A simple inventory plugin for the CHPC web portal.

Testing the Plugin
----------------------------

Test the plugin by un-commenting the content in :code:`./ansible.cfg` and:

.. code-block:: console

   $ export CMDB_API_BEARER_TOKEN=<value>
   $ export CMDB_API_URL=<value>
   $ ansible-doc -t inventory uofuchpc.cmdb.portal
   ...
   $ ansible-inventory --list -i inventory.portal.yml
   ...

More Information
-------------------------

* `Write your own Red Hat Ansible Tower inventory plugin <https://developers.redhat.com/blog/2021/03/10/write-your-own-red-hat-ansible-tower-inventory-plugin>`_
* `How to Write an Inventory Import Script <https://uofu.app.box.com/file/1326767497658?s=8vc2x761npatscf0zfj6z0jc7xque5ev>`_
* `Creating custom dynamic inventories for Ansible <https://www.jeffgeerling.com/blog/creating-custom-dynamic-inventories-ansible>`_
* `Inventories <https://docs.ansible.com/ansible-tower/latest/html/userguide/inventories.html>`_
* `Inventory File Importing <https://docs.ansible.com/ansible-tower/3.8.6/html/administration/scm-inv-source.html#ag-inv-import>`_
* `Custom Credential Types <https://docs.ansible.com/ansible-tower/3.8.6/html/userguide/credential_types.html#ug-credential-types>`_
* `GitHub: amazon.aws/plugins/inventory/aws_ec2.py <https://github.com/ansible-collections/amazon.aws/blob/main/plugins/inventory/aws_ec2.py>`_
* `Inventory plugins <https://docs.ansible.com/ansible/latest/plugins/inventory.html>`_
* `How to write an Ansible plugin to create inventory files <https://www.redhat.com/sysadmin/ansible-plugin-inventory-files>`_
* `Ansible Dynamic Inventory Using Plugins <https://blog.networktocode.com/post/Ansible-Dynamic-Inventory-using-Plugins/>`_
* `Developing plugins <https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#developing-plugins>`_
* `Developing dynamic inventory <https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html>`_

