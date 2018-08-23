
import uuid
import os.path
import random
import time

import psycopg2

import vm.vmutils as vmutils
import vm.vm_descriptor as vm_descriptor

XML_VM_TEMPLATE = "vm/vm_template.xml"

UMBOX_DATA_INTERFACE = "eth0"
UMBOX_CONTROL_INTERFACE = "eth1"


def create_and_start_umbox(device_id, data_node_ip, instance_name, image_name, data_bridge, control_bridge):

    # First generate an updated XML from the template to use when creating the VM.
    umbox = VmUmbox(instance_name, image_name, data_bridge, control_bridge)
    template_xml_file = os.path.abspath(XML_VM_TEMPLATE)
    with open(template_xml_file, 'r') as xml_file:
        template_xml = xml_file.read().replace('\n', '')
    updated_xml = umbox.get_updated_descriptor(template_xml)
    print updated_xml

    # Explicitly connect to hypervisor to ensure we are getting to remote libvirtd.
    vmutils.VirtualMachine.get_hypervisor_instance(is_system_level=True, host_name=data_node_ip, transport='tcp')

    # Then create and start the VM itself.
    vm = vmutils.VirtualMachine()
    vm.create_and_start_vm(updated_xml)

    # Store umbox info in the DB.
    store_umbox_info(umbox.control_mac_address, instance_name, device_id)


def store_umbox_info(umbox_id, umbox_name, device_id):
    # Store VM Info (at least control MAC) in DB
    start_time_in_ms = int(round(time.time() * 1000))
    conn = psycopg2.connect("dbname=alerts user=alert_user password=alert_user_pwd")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO umbox_instance (umbox_external_id, device_id, started_at) VALUES (%s, %s, %s)",
                   (umbox_id, device_id, start_time_in_ms))
    conn.commit()
    cursor.close()
    conn.close()

    print "Stored umbox info in DB."


class VmUmbox(object):
    """Class that stores information about a VM that is working as a umbox."""

    def __init__(self, umbox_name, image_name, data_bridge, control_bridge):
        """Default constructor."""

        self.id = str(uuid.uuid4())
        self.name = umbox_name
        self.image_name = image_name
        self.data_bridge = data_bridge
        self.control_bridge = control_bridge
        self.data_mac_address = generate_random_mac()
        self.control_mac_address = generate_random_mac()

    def get_updated_descriptor(self, xml_descriptor_string):
        """Updates an XML containing the description of the VM with the current info of this VM."""

        # Get the descriptor and inflate it to something we can work with.
        xml_descriptor = vm_descriptor.VirtualMachineDescriptor(xml_descriptor_string)

        xml_descriptor.set_uuid(self.id)
        xml_descriptor.set_name(self.name)
        xml_descriptor.set_disk_image(self.image_name, 'qcow2')

        print 'Adding OVS connected network interface'
        xml_descriptor.add_bridge_interface(self.data_bridge, self.data_mac_address, target=UMBOX_DATA_INTERFACE, ovs=True)

        print 'Adding control plane network interface'
        xml_descriptor.add_bridge_interface(self.control_bridge, self.control_mac_address, target=UMBOX_CONTROL_INTERFACE)

        # Remove seclabel item, which tends to generate issues when the VM is executed.
        xml_descriptor.remove_sec_label()

        updated_xml_descriptor_string = xml_descriptor.get_as_string()
        return updated_xml_descriptor_string


def generate_random_mac():
    """Generate a random mac. We are using te 00163e prefix used by Xensource."""
    mac = [
        0x00, 0x16, 0x3e,
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff)
    ]
    return ':'.join(map(lambda x: "%02x" % x, mac))
