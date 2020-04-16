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
# - /etc/default/libvirt-bin or /etc/default/libvirtd: set libvirtd_opts to "--listen" , and uncomment.
install_qemu() {
    echo "Installing Qemu and Libvirt Daemon..."
    sudo apt-get -yqq install qemu-system libvirt-bin
    sudo usermod -a -G kvm $USER
    echo "Qemu and Libvirt Install Complete"
}

# Install packages
echo "Beginning packages setup..."
install_qemu
echo "Finished setting up packages"

# To enable nested VMs, if needed: http://www.server-world.info/en/note?os=Ubuntu_16.04&p=kvm&f=8
