#!/bin/bash

update() {
    echo "Updating apt-get..."
    sudo apt-get -qq update
    echo "Update complete"
}

# Note that for the libvirt-bin daemon to actually listen to incoming connections, the following config changes are needed:
# - /etc/libvirt/libvirtd.conf: uncomment the line #listen_tcp = 1
# - /etc/libvirt/libvirtd.conf: uncomment the line #listen_tls = 0
# - /etc/libvirt/libvirtd.conf: uncomment the line and change to #auth_tcp = "none"
# - /etc/default/libvirt-bin: set libvirtd_opts to "--listen" , and uncomment.
install_qemu() {
    echo "Installing Qemu and Libvirt Daemon..."
    sudo apt-get -yqq install qemu-system-x86_64 libvirt-bin
    echo "Python Install Complete"
}

install_ovs() {
    echo "Installing OVS..."
    sudo apt-get -yqq install openvswitch-common openvswitch-switch openvswitch-dbg ethtool
    sudo systemctl start openvswitch-switch
    sudo systemctl enable openvswitch-switch
    echo "OVS Install Complete"
}

# Install packages
echo "Beginning packages setup..."
update
install_qemu
install_ovs
echo "Finished setting up packages"

# To enable nested VMs, if needed: http://www.server-world.info/en/note?os=Ubuntu_16.04&p=kvm&f=8
