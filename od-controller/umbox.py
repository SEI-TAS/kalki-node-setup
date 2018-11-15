
import uuid
import os
import os.path
import random
import re
from argparse import ArgumentParser

import psycopg2

import vm.vmutils as vmutils
import vm.vm_descriptor as vm_descriptor
import vm.diskimage

# DB Info.
DB_NAME = "kalkidb"
DB_USER = "kalkiuser"
DB_PASS = "kalkipass"
PG_DB_STRING = "dbname=" + DB_NAME + " user=" + DB_USER + " password=" + DB_PASS

XML_VM_TEMPLATE = "vm/vm_template.xml"

# Base names for the TUN/TAP virtual interfaces on the data node that handle the VM interfaces.
UMBOX_DATA_TUN = "vnudata"
UMBOX_CONTROL_TUN = "vnucont"

# Names of the virtual bridges in the data node that will be connected to the VM.
OVS_VIRTUAL_SWITCH = "ovs-br"
CONTROL_PLANE_BRIDGE = "br-control"

# Path to stored VM umbox images in data node.
DATA_NODE_IMAGES_PATH = "/home/kalki/images/"
INSTANCES_FOLDER = "instances"

NUM_SEPARATOR = "-"


def build_mbox_name(state_name, state_actions):
    mbox_name = state_name
    if len(state_actions) >= 2:
        for i in range(0, len(state_actions)):
            regex = re.compile('[^a-zA-Z]')
            mbox_name = regex.sub('', state_name) + regex.sub('', state_actions[i]) + str(i)
    return mbox_name


def create_and_start_umbox(data_node_ip, device_id, image_name,
                           data_bridge=OVS_VIRTUAL_SWITCH,
                           control_bridge=CONTROL_PLANE_BRIDGE):
    umbox = VmUmbox(None, image_name, device_id, data_bridge, control_bridge)
    #umbox.create_linked_image()
    umbox.start(data_node_ip)
    umbox.store_info()

    return umbox


def stop_umbox(data_node_ip, instance_name):
    """Stops a running instance of an umbox."""
    umbox = VmUmbox(instance_name)
    umbox.stop(data_node_ip)

    # TODO: mark instance as stopped in DB, or delete it.


class VmUmbox(object):
    """Class that stores information about a VM that is working as a umbox."""

    def __init__(self, umbox_name, image_name=None, device_id=None, data_bridge=None, control_bridge=None):
        """Default constructor."""
        self.name = umbox_name
        self.image_name = image_name
        self.device_id = device_id
        self.data_bridge = data_bridge
        self.control_bridge = control_bridge

        self.image_id = None
        self.image_path = None
        if self.name is None:
            # For new VMs, generate random uuids, ids, and macs.
            unique_id = uuid.uuid4()
            self.id = str(unique_id)
            self.numeric_id = random.randint(1, 999)
            self.data_mac_address = self.generate_random_mac()
            self.control_mac_address = self.generate_random_mac()

            if self.image_name is not None:
                self.load_image_info()
                self.name = self.image_name + NUM_SEPARATOR + str(self.numeric_id)
        else:
            self.id = None
            self.numeric_id = self.name[self.name.rfind(NUM_SEPARATOR) + 1:]
            self.data_mac_address = None
            self.control_mac_address = None

        self.instance_disk_path = os.path.join(DATA_NODE_IMAGES_PATH, INSTANCES_FOLDER, self.name)

        print("VM name: " + self.name)

    def store_info(self):
        """Store VM Info (at least control MAC) in DB"""
        conn = psycopg2.connect(PG_DB_STRING)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO umbox_instance (alerter_id, umbox_image_id, container_id, device_id) VALUES (%s, %s, %s, %s)",
                       (self.control_mac_address, self.image_id, self.name, self.device_id))
        conn.commit()
        cursor.close()
        conn.close()

        print "Stored umbox info in DB."

    def load_image_info(self):
        conn = psycopg2.connect(PG_DB_STRING)
        cursor = conn.cursor()
        cursor.execute("SELECT path, id FROM umbox_image WHERE name=%s", (self.image_name,))
        image_info = cursor.fetchone()
        self.image_path = image_info[0]
        self.image_id = image_info[1]
        cursor.close()
        conn.close()

    def create_linked_image(self):
        """Create a linked qcow2 file so that we don't modify the template, and we don't have to copy the complete image."""
        # TODO: find way to do this remotely.
        template_image = vm.diskimage.DiskImage(self.image_path)
        template_image.create_linked_qcow2_image(self.instance_disk_path)

    def get_updated_descriptor(self, xml_descriptor_string):
        """Updates an XML containing the description of the VM with the current info of this VM."""

        # Get the descriptor and inflate it to something we can work with.
        xml_descriptor = vm_descriptor.VirtualMachineDescriptor(xml_descriptor_string)

        xml_descriptor.set_uuid(self.id)
        xml_descriptor.set_name(self.name)

        # TODO: change this back to instance_disk_path when we are able to create it.
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

    def _connect_to_remote_hypervisor(self, hypervisor_host_ip):
        """Explicitly connect to hypervisor to ensure we are getting to remote libvirtd."""
        vmutils.VirtualMachine.get_hypervisor_instance(is_system_level=True, host_name=hypervisor_host_ip, transport='tcp')

    def start(self, hypervisor_host_ip):
        """Creates a new VM using the XML template plus the information set up for this umbox."""
        self._connect_to_remote_hypervisor(hypervisor_host_ip)

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

    def pause(self, hypervisor_host_ip):
        self._connect_to_remote_hypervisor(hypervisor_host_ip)
        vm = vmutils.VirtualMachine()
        try:
            vm.connect_to_virtual_machine_by_name(self.name)
            vm.pause()
        except:
            print("VM not found.")

    def unpause(self, hypervisor_host_ip):
        self._connect_to_remote_hypervisor(hypervisor_host_ip)
        vm = vmutils.VirtualMachine()
        try:
            vm.connect_to_virtual_machine_by_name(self.name)
            vm.unpause()
        except:
            print("VM not found.")

    def stop(self, hypervisor_host_ip):
        self._connect_to_remote_hypervisor(hypervisor_host_ip)
        vm = vmutils.VirtualMachine()
        try:
            vm.connect_to_virtual_machine_by_name(self.name)
            vm.destroy()

            #TODO: destroy instance image file.
        except:
            print("VM not found.")


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("-c", "--command", dest="command", required=True, help="Command: start or stop")
    parser.add_argument("-n", "--node", dest="datanodeip", required=True, help="IP of the data node")
    parser.add_argument("-d", "--deviceid", dest="deviceid", required=False, help="device id")
    parser.add_argument("-i", "--image", dest="imagename", required=False, help="name of the umbox image")
    parser.add_argument("-u", "--umbox", dest="umboxname", required=False, help="name of the umbox instance")
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    print("Command: " + args.command)
    print("Data node to use: " + args.datanodeip)
    if args.command == "start":
        print("Device ID: " + args.deviceid)
        print("Image name: " + args.imagename)

        create_and_start_umbox(args.datanodeip, args.deviceid, args.imagename)
    else:
        print("Instance: " + args.umboxname)

        stop_umbox(args.datanodeip, args.umboxname)


if __name__ == '__main__':
    main()
