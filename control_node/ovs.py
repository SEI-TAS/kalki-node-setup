import subprocess
import shlex
from argparse import ArgumentParser

OF_COMMAND_BASE = "sudo ovs-ofctl -O OpenFlow13"
OF_COMMAND_SERVER = "tcp:{}:{}"
DEFAULT_SWITCH_PORT = 6653

DEFAULT_PRIORITY = "200"

OVSDB_COMMAND_BASE = "sudo ovs-vsctl"
OVSDB_COMMAND_SERVER = "--db=tcp:{}:{}"
DEFAULT_OVSDB_PORT = 6654

class OpenFlowRule(object):
    """Represents an OF rule."""

    def __init__(self, type, in_port, out_port):
        self.type = type
        self.in_port = in_port
        self.out_port = out_port
        self.priority = DEFAULT_PRIORITY
        self.src_ip = None
        self.dest_ip = None

    def build_rule(self):
        """Creates a string with the flow rule from the information in this object."""
        rule_string = "\""

        if self.type is not None:
            rule_string += "{}, ".format(self.type)

        if self.priority is not None:
            rule_string += "priority={}, ".format(self.priority)

        if self.in_port is not None:
            rule_string += "in_port={}, ".format(self.in_port)

        if self.src_ip is not None:
            rule_string += "ip_src={}, ".format(self.src_ip)

        if self.dest_ip is not None:
            rule_string += "ip_dst={}, ".format(self.dest_ip)

        if self.out_port is not None:
            rule_string += "actions=output:{}, ".format(self.out_port)
        elif self.out_port == -1:
            rule_string += "actions=drop"

        return rule_string + "\""


class RemoteVSwitch(object):
    """Represents a remove OVS switch. Communicates to it through OpenFlow using the ovs-ofctl local command line
    tool."""

    def __init__(self, server_ip, switch_port):
        self.server_ip = server_ip
        self.switch_port = switch_port

    def _send_openflow_command(self, command, arguments=""):
        """Sends an OpenFlow command through ovs-ofctl to a remove ovsswitchd server."""
        try:
            server_info = OF_COMMAND_SERVER.format(self.server_ip, self.switch_port)
            full_command = OF_COMMAND_BASE + " " + command + " " + server_info + " " + arguments
            print("Executing command: " + full_command)
            output = subprocess.check_output(shlex.split(full_command))
            print("Output of command: " + output)
            return output.rstrip()
        except subprocess.CalledProcessError, e:
            print("Error executing command: " + str(e))

    def execute_show_command(self):
        """Sends the show command through OF to remote switch."""
        return self._send_openflow_command("show")

    def execute_dump_flows_command(self):
        """Send the dump-flows command through OF to remote switch."""
        return self._send_openflow_command("dump-flows")

    def add_rule(self, of_rule):
        """Adds a new rule/flow to the switch."""
        rule_string = of_rule.build_rule()
        print("Adding rule: " + rule_string)
        self._send_openflow_command("add-flow", rule_string)

    def remove_rule(self, of_rule):
        """Removes a rule/flow from the switch."""
        rule_string = of_rule.build_rule()
        print("Removing rule: " + rule_string)
        self._send_openflow_command("del-flows", rule_string)


class RemoteOVSDB(object):
    """Represents a remove OVS DB. Communicates to it through OpenFlow using the ovs-vsctl local command line
    tool."""

    def __init__(self, server_ip, db_port):
        self.server_ip = server_ip
        self.db_port = db_port

    def _send_db_command(self, command, arguments=""):
        """Sends an DB command through ovs-vsctl to a remove ovsdb server."""
        try:
            server_info = OVSDB_COMMAND_SERVER.format(self.server_ip, self.db_port)
            full_command = OVSDB_COMMAND_BASE + " " + server_info + " " + command + " " + arguments
            print("Executing DB command: " + full_command)
            output = subprocess.check_output(shlex.split(full_command))
            print("Output of command: " + output)
            return output.rstrip()
        except subprocess.CalledProcessError, e:
            print("Error executing command: " + str(e))

    def get_port_id(self, port_name):
        """Gets the id of a port given its id."""
        port_name_command = "get Interface {} ofport".format(port_name)
        return self._send_db_command(port_name_command)


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("-c", "--command", dest="command", required=True, help="Command: start or stop")
    parser.add_argument("-s", "--server", dest="datanodeip", required=True, help="IP of the data node server")
    parser.add_argument("-si", "--sourceip", dest="sourceip", required=False, help="Source IP")
    parser.add_argument("-di", "--destip", dest="destip", required=False, help="Destination IP")
    parser.add_argument("-i", "--inport", dest="inport", required=False, help="Input port name/number on virtual switch")
    parser.add_argument("-o", "--outport", dest="outport", required=False, help="Output port name/number on virtual switch")
    parser.add_argument("-p", "--priority", dest="priority", required=False, help="Priority")
    args = parser.parse_args()
    return args


def get_port_number(ovsdbip, port_name):
    if port_name is None:
        return None

    try:
        port_number = int(port_name)
        return port_number
    except ValueError:
        ovsdb = RemoteOVSDB(ovsdbip, DEFAULT_OVSDB_PORT)
        port_number = ovsdb.get_port_id(str(port_name))
        if port_number is None:
            print("Unable to obtain port number for {}; aborting.".format(port_name))
            exit(1)

        print("Port number for {} is {}".format(port_name, port_number))
        return port_number


def main():
    args = parse_arguments()
    print("Command: " + args.command)
    print("Data node to use: " + args.datanodeip)
    switch = RemoteVSwitch(args.datanodeip, DEFAULT_SWITCH_PORT)

    if args.command == "add_rule" or args.command == "del_rule":
        print("Source IP: " + args.sourceip)
        print("Destination IP: " + args.destip)
        print("Input port name: " + str(args.inport))
        print("Output port name: " + str(args.outport))
        print("Priority: " + args.priority)

        # First get port numbers if needed.
        in_port_number = get_port_number(args.datanodeip, args.inport)
        out_port_number = get_port_number(args.datanodeip, args.outport)

        # Set up rule with received IPs and OVS ports.
        rule = OpenFlowRule("ip", in_port_number, out_port_number)
        rule.src_ip = args.sourceip
        rule.dest_ip = args.destip
        if args.priority is not None:
            rule.priority = args.priority

        if args.command == "add_rule":
            switch.add_rule(rule)
        else:
            # Have to disable priority and output as that is not accepted when deleting flows.
            rule.priority = None
            rule.out_port = None
            switch.remove_rule(rule)
    else:
        switch.execute_show_command()
        switch.execute_dump_flows_command()


if __name__ == "__main__":
    main()
