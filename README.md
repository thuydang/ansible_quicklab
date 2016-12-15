Ansible scripts for creating VMs for quick lab using kvm. All resources are created in this 
directory.

= Scenario: 
The idea is to start a few VMs on a host (localhost) and automatically setup these VMs to form a virtual infrastructure
e.g., OpenStack.

= Steps:
1. Preparing virtual network using bridge, tun, tap

2. Provisioning VMs

3. Custom scripts for VMs installation

= Roles:
== kvm_host_setup: 
* Install packages on (this) host to support virtualization with kvm.

== kvm_network: 
* create bridges and tap/tun interfaces for the VMs with the extension of ansible-nmcli module (https://github.com/thuydang/ansible-nmcli.git; version: origin/ansible-nmcli-role).
* Configure iptables/firewall for routing traffic of bridges.
* The variables allows to see how the network is configured (default/main.yml):

== kvm_manage: 
* Start the vms
* The variables: 


= Design decisions:
* Inventory files hold hosts group, each of which has a playbook, e.g., baremetal inventory, baremetal.yml

= Usage:
== Install libraries and roles
ansible-galaxy install -r requirements.yml

== Start lab

# ansible-playbook -i inventory_file site.yml --limit tutorial_hosts
# ansible-playbook -i inventory_file  tutorial.yml
# ansible localhost -i inventory/vfoss_dev -m alternatives -a "link=/usr/bin/psql name=pgsql-psql path=/usr/pgsql-9.4/bin/psql" -s -vvvv

* Test run single Module:
    source ansible_src/ansible/hacking/env-setup

Create instance

    sudo ansible_src/ansible/hacking/test-module -m ansible_quicklabs/library_ext/ansible-kvm/library/kvm_cmd.py -a "action='instance-create' image_base='/mnt/nfv/kvm_openstack_lab/images/Fedora-Cloud-Base-24-1.2.x86_64.qcow2' image_format='qcow2' instance_name='/mnt/nfv/kvm_openstack_lab/instances/controller.qcow2' image_size=8G"

Boot instance

	  sudo ansible_src/ansible/hacking/test-module -m ansible_quicklabs/library_ext/ansible-kvm/library/kvm_cmd.py \
			  -a "action='boot' instance_name='/mnt/nfv/kvm_openstack_lab/instances/controller.qcow2' instance_cpus=1 instance_ram=1024 instance_vnc=:1 instance_cdrom=/mnt/nfv/kvm_openstack_lab/cloud-init/default/default-cidata.iso"


* Setup

Run all roles:

    ansible-playbook -i inventory/vi_nodes quicklab_kvm_openstack.yml -vvv

Run roles with tags:

    ansible-playbook -i inventory/vi_nodes quicklab_kvm_openstack.yml --tags dnsmasq -vvvv

* Shutdown: cleanup everything.

    ansible-playbook -i inventory/vi_nodes quicklab_kvm_openstack_shutdown.yml -vvv

= Work log
* can setup bridge & tun devs. Start kvm
----------
REF

  * https://www.azavea.com/blog/2014/10/09/creating-ansible-roles-from-scratch-part-1/
