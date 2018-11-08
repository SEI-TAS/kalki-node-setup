
import uuid
import os.path
import random
import re

import psycopg2

import vm.vmutils as vmutils
import vm.vm_descriptor as vm_descriptor
import vm.diskimage

DB_NAME = "kalkidb"
DB_USER = "kalkiuser"
DB_PASS = "kalkipass"

XML_VM_TEMPLATE = "vm/vm_template.xml"

# Base names for the TUN/TAP virtual interfaces on the data node that handle the VM interfaces.
UMBOX_DATA_TUN = "vnudata"
UMBOX_CONTROL_TUN = "vnucont"

# Names of the virtual bridges in the data node that will be connected to the VM.
OVS_VIRTUAL_SWITCH = "ovs-br"
CONTROL_PLANE_BRIDGE = "br-control"

# Path to stored VM umbox images in data node.
DATA_NODE_IMAGES_PATH = "/home/kalki/images/"


def build_mbox_name(state_name, state_actions):
    mbox_name = state_name
    if len(state_actions) >= 2:
        for i in range(0, len(state_actions)):
            regex = re.compile('[^a-zA-Z]')
            mbox_name = regex.sub('', state_name) + regex.sub('', state_actions[i]) + str(i)
    return mbox_name


def create_and_start_umbox(device_id, data_node_ip, instance_name, image_name, data_bridge=OVS_VIRTUAL_SWITCH,
                           control_bridge=CONTROL_PLANE_BRIDGE):

    # First create a linked qcow2 file so that we don't modify the template, and we don't have to copy the complete image.
    full_template_path = os.path.join(DATA_NODE_IMAGES_PATH, image_name)
    template_image = vm.diskimage.DiskImage(full_template_path)
    full_instance_path = os.path.join(DATA_NODE_IMAGES_PATH, "instances", instance_name)
    instance_image = template_image.create_linked_qcow2_image(full_instance_path)

    umbox = VmUmbox(instance_name, instance_image.filepath, data_bridge, control_bridge)
    umbox.start(data_node_ip)

    # Store umbox info in the DB.
    store_umbox_info(umbox.control_mac_address, instance_name, device_id)


def store_umbox_info(umbox_id, umbox_name, device_id):
    # Store VM Info (at least control MAC) in DB
    conn = psycopg2.connect("dbname=" + DB_NAME + " user=" + DB_USER+ " password=" + DB_PASS)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO umbox_instance (umbox_external_id, device_id) VALUES (%s, %s)",
                   (umbox_id, device_id))
    conn.commit()
    cursor.close()
    conn.close()

    print "Stored umbox info in DB."


class VmUmbox(object):
    """Class that stores information about a VM that is working as a umbox."""

    def __init__(self, umbox_name, image_path, data_bridge, control_bridge):
        """Default constructor."""

        unique_id = uuid.uuid4()
        self.id = str(unique_id)
        self.numeric_id = unique_id.int
        self.name = umbox_name
        self.image_path = image_path
        self.data_bridge = data_bridge
        self.control_bridge = control_bridge
        self.data_mac_address = self.generate_random_mac()
        self.control_mac_address = self.generate_random_mac()

    def get_updated_descriptor(self, xml_descriptor_string):
        """Updates an XML containing the description of the VM with the current info of this VM."""

        # Get the descriptor and inflate it to something we can work with.
        xml_descriptor = vm_descriptor.VirtualMachineDescriptor(xml_descriptor_string)

        xml_descriptor.set_uuid(self.id)
        xml_descriptor.set_name(self.name)
        xml_descriptor.set_disk_image(self.image_path, 'qcow2')

        data_iface_name = UMBOX_DATA_TUN + str(self.numeric_id)
        print 'Adding OVS connected network interface, using tap: ' + data_iface_name
        xml_descriptor.add_bridge_interface(self.data_bridge, self.data_mac_address, target=data_iface_name, ovs=True)

        control_iface_name = UMBOX_CONTROL_TUN + str(self.numeric_id)
        print 'Adding control plane network interface, using tap: ' + control_iface_name
        xml_descriptor.add_bridge_interface(self.control_bridge, self.control_mac_address, target=control_iface_name)

        # Remove seclabel item, which tends to generate issues when the VM is executed.
        xml_descriptor.remove_sec_label()

        updated_xml_descriptor_string = xml_descriptor.get_as_string()
        return updated_xml_descriptor_string

    def start(self, hypervisor_host_ip):
        """Creates a new VM using the XML template plus the information set up for this umbox."""
        # Explicitly connect to hypervisor to ensure we are getting to remote libvirtd.
        vmutils.VirtualMachine.get_hypervisor_instance(is_system_level=True, host_name=hypervisor_host_ip, transport='tcp')

        # Set up VM information from template and umbox data.
        template_xml_file = os.path.abspath(XML_VM_TEMPLATE)
        with open(template_xml_file, 'r') as xml_file:
            template_xml = xml_file.read().replace('\n', '')
        updated_xml = self.get_updated_descriptor(template_xml)
        print updated_xml

        # Check if the VM is already running.
        vm = vmutils.VirtualMachine()
        try:
            # If it is, connect and destroy it, before starting a new one.
            vm.connect_to_virtual_machine_by_name(self.name)
            print "VM with same name was already running; destroying it."
            vm.destroy()
            print "VM destroyed."
        except vmutils.VirtualMachineException, ex:
            print "VM was not running."
            vm = vmutils.VirtualMachine()

        # Then create and start the VM itself.
        print "Starting new VM."
        vm.create_and_start_vm(updated_xml)
        print "New VM started."

    def generate_random_mac(self):
        """Generate a random mac. We are using te 00163e prefix used by Xensource."""
        mac = [
            0x00, 0x16, 0x3e,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff)
        ]
        return ':'.join(map(lambda x: "%02x" % x, mac))


def test():
    # Test code.
    data_node_ip = "192.168.58.102"
    device_id = "1"
    image_file = "umbox-sniffer.qcow2"
    instance_name = "umbox-sniffer-1"
    create_and_start_umbox(device_id, data_node_ip, instance_name, image_file)


if __name__ == '__main__':
    test()
