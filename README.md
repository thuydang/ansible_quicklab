Ansible scripts for creating VMs for quick lab using kvm. All resources are created in this 
directory.

= Scenario: 
The idea is to start a few VMs on a host (localhost) and automatically setup these VMs to form a virtual infrastructure
e.g., OpenStack.

= Steps:
1. Preparing virtual network using bridge, tun, tap

2. Provisioning VMs

3. Custom scripts for VMs installation

= Design decisions:
* Inventory files hold hosts group, each of which has a playbook, e.g., baremetal inventory, baremetal.yml

= Usage:

ansible-playbook -i inventory_file site.yml --limit tutorial_hosts
ansible-playbook -i inventory_file  tutorial.yml
----------
REF

  * https://www.azavea.com/blog/2014/10/09/creating-ansible-roles-from-scratch-part-1/
