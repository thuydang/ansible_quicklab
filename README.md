# Fast Provisioning OpenStack Virtualization Infrastructure with Ansibel Quicklab

Scenario: The idea is using ansible scripts to start a few VMs on a host (localhost) and automatically setup these VMs to form a virtualization infrastructure e.g., OpenStack. This is a portable setup showing the essence of virtualization, suiltable for exeriment and education purposes. Enjoy!

 
# Objectives:

Network Connectivity for OpenStack Infrastructure Nodes [1]

We want to create 3 VMs (guests) with KVM on a physical host. The VMs will be setup to become different nodes of an OpenStack infrastructure and will be connected as in the figure with 3 bridges. The bridges provide connectivity to Management Network, Internal Network and External Network. The network are also knows as NAT network in VirtualBox, etc.

For the purpose, we can use ansible scripts to configure the networks and make it ready to start the VMs. Step-by-step tutorial of the process is described following.

## Minimal hardware requirement:

 * Generated lab with 3 VMs uses 10Gb. More space should be available depending on OpenStack installatin and use.
 * Plenty of RAM, 5Gb may be enough for small OpenStack deployment.

# Quickstart:
Download ansible_quicklab scripts

Clone ansible quicklab from Gibhub:

```
https://github.com/thuydang/ansible_quicklab.git
```

## Install required ansible roles

The dependency modules are provided in requirements.yml. It contains customized modules for network and kvm commands. Install the modules with ansible-galaxy:

```
ansible-galaxy install -r requirements.yml
```

## Configure ansible variables to reflect the network architecture

Sample configurations of the network and nodes are in vars/quicklab_kvm_openstack_config.yml. We will update the file with our configurations. The parameter are self-explainatory.
### Quicklab directory

The directory contains everything related to our quicklab project, where kvm images, instances, etc are stored. Replace the path with your location.

quicklab_workspace: "/mnt/nfv/kvm_openstack_lab"

The full folder structure will be automatically generated under that location:

```
/mnt/nfv/kvm_openstack_lab
├── boot_vms.sh
├── cloud-init
│   └── default
│       └── default-cidata.iso
├── images
│   ├── cirros-0.3.4-x86_64-disk.img
│   └── Fedora-Cloud-Base-24-1.2.x86_64.qcow2
├── instances
│   ├── compute.qcow2
│   ├── controller.qcow2
│   ├── Fedora-x86_64-20-300G-20150309-sda-mininet.qcow2
│   └── network.qcow2
└── keys
```
 
### kvm_networks section

 

Configure bridge name, IP range:

- name: br_ql_mgmt
    interface: br_ql_mgmt # TODO not used, check consistency name vs interface.
    ## Firewall setting
    ip4: 10.10.10.1/24
    gw4:
    ## dnsmasq setting
    # DNS A record of the interface.
    #interface: br_ql_mgmt
    #name: 'mgmt_switch'
    # Optional DNS CNAME records of the interface.
    aliases: [ 'mgmt_router']
    # First IP address in the DHCP range (index).
    dhcp_range_start: '10'
    # Last IP address in the DHCP range (index).
    dhcp_range_end: '-10'
    # DHCP lease lifetime.
    dhcp_lease: '24h'
    # DHCPv6 options configured on this interface.
    ipv6_mode: 'ra-names,ra-stateless,slaac'

### kvm_guests section

Configure VM names, interfaces:
```
kvm_guests: # kvm quest vm
  - hostname: controller #insance_name?
    cpu: 1
    cpu_conf: "core2duo,+vmx -enable-kvm"
    ram: 2024M
    vnc: :0
    #image: cirros-0.3.4-x86_64-disk.img # base image in images_dir
    image: Fedora-Cloud-Base-24-1.2.x86_64.qcow2 # base image in images_dir
    image_format: qcow2
    image_size: 40G
    network_interfaces: #ref: https://github.com/mrlesmithjr/ansible-config-interfaces
      - name: eth0
        hwaddr: de:ad:be:80:7c:53
        bootproto: dhcp
        configure: true
        comment:
        method: manual
        address:
        netmask:
        netmask_cidr:
        gateway:
        network_name: br_ql_mgmt # Bridge iface to be connected
```
	
'image' holds the base image for our VM nodes. We use 'Fedora-Cloud-Base-24-1.2.x86_64.qcow2' whick can be download from Fedora project. Choose the image with qcow2 format. Alternative, you can also create your own base image with pre-installed packages. 

```
https://getfedora.org/atomic/download/
```

Note: automatic download of image is not yet implemented. Please download the exact image and place it in {{quicklab_workspace}}/images folder. You may have to create the images folder structure.

#### Generate MAC addresses for the interfaces from console:

```
$>MACADDR="52:54:00:$(dd if=/dev/urandom bs=512 count=1 2>/dev/null | md5sum | sed 's/^\(..\)\(..\)\(..\).*$/\1:\2:\3/')"; echo $MACADDR
```

## Create OpenStack lab

Hopfully we don't miss anything. Now we can get things ready by running ansible playbook:

```
$> sudo ansible-playbook -i inventory/vi_nodes quicklab_kvm_openstack.yml
```

ansible-playbook option -vvvv will ouput everything during the setup.
## Create cloud-init.iso

Incase a cloud image is used as base image for our VMs, we need to start the VMs with a cloud-init.iso, which can be configure to inject credential and ssh keys for the default user ('fedora' for fedora cloud image). You can create your own cloud init iso. There is a cloud-init.iso, which can be download from the project's github:

```
https://github.com/thuydang/ansible_quicklab/blob/vfoss_tutorial/default-cidata.iso
```

Place the file in {{quicklab_workspace}}/cloud-init/default/. See folder structure above.

The files used to generate cloud-init-iso are shown bellow:

```
cat /mnt/nfv/kvm_openstack_lab/cloud-init/default/meta-data
instance-id: default-instance
local-hostname: default-host

cat /mnt/nfv/kvm_openstack_lab/cloud-init/default/user-data
#cloud-config
password: password
chpasswd: { expire: False }
ssh_pwauth: True
#ssh_authorized_keys:
#   - ... ssh-rsa new public key here user@host ...
```

## Finally Start The VMs

A bash script is generated, which can be executed to start the VMs:

```
$>sudo ./boot_vms.sh
```

This is the command to start one of the vm:

```
#!/bin/sh
# Author thuydang.de@gmail.com
set -x
qemu-kvm -hda /mnt/nfv/kvm_openstack_lab/instances/controller.qcow2 \
        -cpu core2duo,+vmx -enable-kvm \
        -smp cpus=1 \
        -m 2024M -vnc :0 \
        -cdrom cloud-init/default/default-cidata.iso \
        -device e1000,netdev=br_ql_mgmt,mac=de:ad:be:80:7c:53 -netdev tap,id=br_ql_mgmt,ifname=controller-eth0,script=no,downscript=no \
        -device e1000,netdev=br_ql_int,mac=de:ad:be:80:7c:54 -netdev tap,id=br_ql_int,ifname=controller-eth1,script=no,downscript=no \
        -device e1000,netdev=br_ql_ext,mac=de:ad:be:80:7c:55 -netdev tap,id=br_ql_ext,ifname=controller-eth2,script=no,downscript=no \
    &
```

# Conclusion

We now ready to install OpenStack on the generated VMs!
I used puppet to setup the old OpenStack Juno on the same virtual infrastructure, which is avalable here:

```
https://github.com/thuydang/puppetlabs-openstack/tree/td_up_5.0.2
```

If you are not ready with ansible, I also created a bunch of Bash scripts to achieve the same objective. You may have to configure the network and vms by changing the script directly. The bash version of quicklab project is on github:

```
https://github.com/thuydang/kvm_scripts
```
Thanks for reading. Please fork, try, imporve and create pull requests!!

# Resources:

  * https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux_OpenStack_Platform/5/html/Cloud_Administrator_Guide/section_networking-arch.html


# Old 

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
