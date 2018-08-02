
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

import os
import re

from vmutils import VirtualMachineException


################################################################################################################
# Represents an XML description of a VM.
################################################################################################################
class VirtualMachineDescriptor(object):

    # The namespace and nodes used for QEMU parameters.
    qemuXmlNs = "http://libvirt.org/schemas/domain/qemu/1.0"
    qemuCmdLineNodeName = "{%s}commandline" % qemuXmlNs
    qemuArgNodeName = "{%s}arg" % qemuXmlNs

    ################################################################################################################
    # Constructor.
    ################################################################################################################
    def __init__(self, xmlDescriptorString):
        # Load the XML root element from the XML descriptor string.
        self.xmlRoot = ElementTree.fromstring(xmlDescriptorString)

    ################################################################################################################
    #
    ################################################################################################################
    @staticmethod
    def does_name_fit(xml_string, new_name):
        # Any new data must not be bigger than the previous one, or it won't fit in the raw header.
        new_name_will_fit = False
        original_name = VirtualMachineDescriptor.get_raw_name(xml_string)
        if original_name:
            new_name_will_fit = len(new_name) <= len(original_name)

        return new_name_will_fit

    ################################################################################################################
    # Gets the name from a raw xml descriptor string.
    ################################################################################################################
    @staticmethod
    def get_raw_name(xml_string):
        name = None
        matches = re.search(r"<name>([\w\-]+)</name>", xml_string)
        if matches:
            name = matches.group(1)
        return name

    ################################################################################################################
    # Updates the name and id of an xml by simply replacing the text, without parsing, to ensure the result will
    # have exactly the same length as before.
    ################################################################################################################
    @staticmethod
    def update_raw_name_and_id(saved_xml_string, uuid, name):
        updated_xml = re.sub(r"<uuid>[\w\-]+</uuid>", "<uuid>%s</uuid>" % uuid, saved_xml_string)
        updated_xml = re.sub(r"<name>[\w\-]+</name>", "<name>%s</name>" % name, updated_xml)
        return updated_xml

    ################################################################################################################
    # Returns an XML string with the contents of this VMDescriptor
    ################################################################################################################
    def get_as_string(self):
        xmlString = ElementTree.tostring(self.xmlRoot)
        return xmlString
    
    ################################################################################################################
    # Returns the port the VNC server is listening on, if any.
    ################################################################################################################
    def get_vnc_port(self):
        vnc_node = self.xmlRoot.find("devices/graphics[@type='vnc']")
        if vnc_node is not None:
            vnc_port = vnc_node.get("port")
            return vnc_port
        else:
            raise VirtualMachineException("VNC not set up for this VM.")

    ################################################################################################################
    # Sets the realtek network driver instead of the default virtio one. Needed for Windows-based VMs that do
    # not have the virtio driver installed (which does come installed in Linux distributions).
    ################################################################################################################
    def set_realtek_network_driver(self):
        # Get the devices node
        devices = self.xmlRoot.find('devices')

        # We assume the VM has exactly 1 network interface.
        network_card = devices.find("interface")
        model = network_card.find("model")
        model.set("type", "rtl8139")

    ################################################################################################################
    # Will enable bridged mode in the XML.
    ################################################################################################################
    def enable_bridged_mode(self, interface, ovs=False):
        # Get the devices node
        devices = self.xmlRoot.find('devices')

        # Find the network card, change its type to bridge.
        # We assume the VM has exactly 1 network interface.
        network_card = devices.find("interface")
        network_card.set("type", "bridge")

        # Update or add the source element, needed for bridged mode.
        network_card_source = network_card.find("source")
        if network_card_source is not None:
            network_card_source.set("bridge", interface)
        else:
            network_card.append(ElementTree.fromstring('<source bridge="%s"/>' % interface))

        # Attribute for OpenVSwitch.
        if ovs:
            network_card_vp = network_card.find("virtualport")
            if network_card_vp is not None:
                network_card_vp.set("type", "openvswitch")
            else:
                network_card.append(ElementTree.fromstring('<virtualport type="openvswitch"/>'))

    ################################################################################################################
    # Adds a new network card in bridged mode with the MAC and bridge that are indicagted.
    ################################################################################################################
    def add_bridge_interface(self, bridge, mac, target=None, ovs=False):
        target_string = ""
        if target is not None:
            target_string = '<target dev="{}"/>'.format(target)

        # Attribute for OpenVSwitch.
        ovs_string = ""
        if ovs:
            ovs_string = '<virtualport type="openvswitch"/>'

        # Add a new bridge interface.
        devices = self.xmlRoot.find('devices')
        devices.append(ElementTree.fromstring('<interface type="bridge"><model type="virtio"/><source bridge="{}"/><mac address="{}" />{}{}</interface>'.format(bridge, mac, target_string, ovs_string)))

    ################################################################################################################
    # Will enable the non-bridged mode in the XML.
    ################################################################################################################
    def enable_non_bridged_mode(self, adapter):
        # Get the devices node
        devices = self.xmlRoot.find('devices')

        # Find the network card, change its type to ethernet.
        # We assume the VM has exactly 1 network interface.
        network_card = devices.find("interface")
        network_card.set("type", "user")
        network_card.set("name", adapter)

        network_card_source = network_card.find("source")
        if network_card_source is not None:
            network_card.remove(network_card_source)

    ################################################################################################################
    # Sets the mac address to the given value.
    # We assume the VM has exactly 1 network interface.
    ################################################################################################################
    def set_mac_address(self, mac_address):
        # Get the network card.
        network_card = self.xmlRoot.find('devices/interface')

        # Update or add the mac element.
        mac_element = network_card.find("mac")
        if mac_element is not None:
            mac_element.set("address", mac_address)
        else:
            network_card.append(ElementTree.fromstring('<mac address="%s"/>' % mac_address))

    ################################################################################################################
    # Ensures that VNC is enabled and accessible remotely.
    ################################################################################################################
    def enable_remote_vnc(self):
        self.enable_vnc("0.0.0.0")

    ################################################################################################################
    # Ensures that VNC is enabled and accessible locally only.
    ################################################################################################################
    def enable_local_vnc(self):
        self.enable_vnc("127.0.0.1")

    ################################################################################################################
    # Ensures VNC is enabled.
    ################################################################################################################
    def enable_vnc(self, listening_address):
        vnc_graphics = self.xmlRoot.find("devices/graphics[@type='vnc']")
        if vnc_graphics is None:
            devices_node = self.xmlRoot.find("devices")
            devices_node.append(ElementTree.fromstring('<graphics type="vnc" port="-1" autoport="yes" keymap="en-us" listen="' + listening_address + '"/>'))
        else:
            vnc_graphics.set("listen", listening_address)
            vnc_address = self.xmlRoot.find("devices/graphics/listen[@type='address']")
            if vnc_address is not None:
                vnc_address.set("address", listening_address)

    ################################################################################################################
    # Disables VNC access.
    ################################################################################################################
    def disable_vnc(self):
        vnc_node = self.xmlRoot.find("devices/graphics[@type='vnc']")
        if vnc_node is not None:
            print 'Disabling VNC access.'
            devices_node = self.xmlRoot.find("devices")
            devices_node.remove(vnc_node)

    ################################################################################################################
    # Removes the security label.
    ################################################################################################################
    def remove_sec_label(self):
        sec_label = self.xmlRoot.find('seclabel')
        if sec_label is not None:
            print 'Removing security label.'
            self.xmlRoot.remove(sec_label)

    ################################################################################################################
    # Sets the path to the main disk image.
    ################################################################################################################
    def set_disk_image(self, newDiskImagePath, newDiskType):
        # Find the first disk in the description.
        diskElements = self.xmlRoot.findall('devices/disk')
        mainDiskImageNode = None
        mainDiskDriverNode = None
        for diskElement in diskElements:
            diskType = diskElement.attrib['device']
            if diskType == 'disk':
                mainDiskImageNode = diskElement.find('source')
                mainDiskDriverNode = diskElement.find('driver')
                break

        # Check if we found a disk.
        if mainDiskImageNode == None or mainDiskDriverNode == None:
            raise VirtualMachineException("No disk found in XML descriptor.")

        # Set the path to the new disk image.
        mainDiskImageNode.set("file", os.path.abspath(newDiskImagePath))
        mainDiskDriverNode.set("type", newDiskType)

    ################################################################################################################
    # Sets the VM name.
    ################################################################################################################
    def set_name(self, newName):
        nameElement = self.xmlRoot.find('name')
        if nameElement is None:
            raise VirtualMachineException("No name node found in XML descriptor.")
        nameElement.text = newName

    ################################################################################################################
    # Sets the VM id.
    ################################################################################################################
    def set_uuid(self, newUUID):
        uuidElement = self.xmlRoot.find('uuid')
        if uuidElement is None:
            raise VirtualMachineException("No UUID node found in XML descriptor.")
        uuidElement.text = newUUID

    ################################################################################################################
    # Gets the VM id.
    ################################################################################################################
    def get_uuid(self):
        uuidElement = self.xmlRoot.find('uuid')
        if uuidElement is None:
            raise VirtualMachineException("No UUID node found in XML descriptor.")
        return str(uuidElement.text)

    ################################################################################################################
    # Sets port redirection commands for qemu.
    ################################################################################################################
    def set_port_redirection(self, portMappings):
        # Get the node with qemu-related arguments.
        qemuElement = self.xmlRoot.find(self.qemuCmdLineNodeName)

        # If the node was not there, add it.
        if qemuElement == None:
            qemuElement = Element(self.qemuCmdLineNodeName)
            self.xmlRoot.append(qemuElement)

        # Values for redirect arguments.
        portRedirectionCommand = '-redir'

        # First we will remove all redirections that contain either the host or guest port.
        qemuArgumentElements = qemuElement.findall(self.qemuArgNodeName)
        lastRedirElement = None
        for qemuArgument in qemuArgumentElements:
            # Get the actual value to check.
            qemuArgumentValue = qemuArgument.get('value')

            # Store "redir" commands since, if we have to remove a redirection, we also have to remove this previous node.
            if(portRedirectionCommand in qemuArgumentValue):
                lastRedirElement = qemuArgument
                continue

            # We will assume that only redirections will have the :%d::%d format. If we find any argument
            # with this format and the host or guest ports redirected, we will remove it, along with
            # the previous redir command argument.
            #if(':%d::' % int(hostPort) in qemuArgumentValue) or ('::%d' % int(guestPort) in qemuArgumentValue):

            # We will assume that only redirection arguments have "tcp:" in them, and we will remove them all.
            if('tcp:' in qemuArgumentValue):
                qemuElement.remove(lastRedirElement)
                qemuElement.remove(qemuArgument)

            if('-usb' in qemuArgumentValue):
                qemuElement.remove(qemuArgument)

        # Now we setup the redirection for all the port mappings that were provided.
        for hostPort, guestPort in portMappings.iteritems():
            #break
            portRedirectionValue = 'tcp:%d::%d' % (int(hostPort), int(guestPort))
            qemuElement.append(Element(self.qemuArgNodeName, {'value':portRedirectionCommand}))
            qemuElement.append(Element(self.qemuArgNodeName, {'value':portRedirectionValue}))
            #break

