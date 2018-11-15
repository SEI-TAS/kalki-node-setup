import subprocess
import shlex
from argparse import ArgumentParser

OF_COMMAND_BASE = "sudo ovs-ofctl -O OpenFlow13"
OF_COMMAND_SERVER = "tcp:{}:{}"
DEFAULT_SWITCH_PORT = 6653

DEFAULT_PRIORITY = "200"


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
        else:
            rule_string += "actions=drop"

        return rule_string + "\""


class RemoteVSwitch(object):
    """Represents a remove OVS switch. Communicates to it through OpenFlow using the ovs-ofctl local command line
    tool."""

    def __init__(self, server_ip, switch_port):
        self.server_ip = server_ip
        self.switch_port = switch_port

    def send_openflow_command(self, command, arguments=""):
        """Sends an OpenFlow command through ovs-ofctl to a remove ovsswitchd server."""
        try:
            server_info = OF_COMMAND_SERVER.format(self.server_ip, self.switch_port)
            full_command = OF_COMMAND_BASE + " " + command + " " + server_info + " " + arguments
            print("Executing command: " + full_command)
            output = subprocess.check_output(shlex.split(full_command))
            print("Output of command: " + output)
            return output
        except subprocess.CalledProcessError, e:
            print("Error executing command: " + str(e))

    def execute_show_command(self):
        """Sends the show command through OF to remote switch."""
        return self.send_openflow_command("show")

    def execute_dump_flows_command(self):
        """Send the dump-flows command through OF to remote switch."""
        return self.send_openflow_command("dump-flows")

    def add_rule(self, of_rule):
        """Adds a new rule/flow to the switch."""
        rule_string = of_rule.build_rule()
        print("Adding rule: " + rule_string)
        self.send_openflow_command("add-flow", rule_string)

    def remove_rule(self, of_rule):
        """Removes a rule/flow from the switch."""
        rule_string = of_rule.build_rule()
        print("Removing rule: " + rule_string)
        self.send_openflow_command("del-flow", rule_string)


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("-c", "--command", dest="command", required=True, help="Command: start or stop")
    parser.add_argument("-n", "--node", dest="datanodeip", required=True, help="IP of the data node")
    parser.add_argument("-d", "--deviceip", dest="deviceip", required=True, help="device IP")
    parser.add_argument("-i", "--inport", dest="inport", required=False, help="Input port on virtual switch")
    parser.add_argument("-o", "--outport", dest="outport", required=True, help="Output port on virtual switch")
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    print("Command: " + args.command)
    print("Data node to use: " + args.datanodeip)
    switch = RemoteVSwitch(args.datanodeip, DEFAULT_SWITCH_PORT)

    if args.command == "add_rule":
        print("Device IP: " + args.deviceip)
        print("Input port: " + str(args.inport))
        print("Output port: " + str(args.outport))

        rule = OpenFlowRule("ip", None, args.outport)
        rule.dest_ip = args.deviceip
        switch.add_rule(rule)
    else:
        switch.execute_show_command()
        switch.execute_dump_flows_command()


if __name__ == "__main__":
    main()
