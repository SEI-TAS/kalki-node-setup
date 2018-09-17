import subprocess
import shlex

OF_COMMAND_BASE = "sudo ovs-ofctl -O OpenFlow13"
OF_COMMAND_SERVER = "tcp:{}:{}"
DEFAULT_SWITCH_PORT = 6653

IP_PORT_RULE = "ip, priority={}, in_port={}, nw_src={}, nw_dst={}, actions=output:{}"


class OpenFlowRule(object):
    """Represents an OF rule."""

    def __init__(self, type, in_port, out_port):
        self.type = type
        self.in_port = in_port
        self.out_port = out_port
        self.priority = None
        self.src_ip = None
        self.dest_ip = None

    def build_rule(self):
        """Creates a string with the flow rule from the information in this object."""
        rule_string = ""

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
            rule_string += "actions=drop, "


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

    def set_rule(self, of_rule):
        """Adds a new rule/flow to the switch."""
        rule_string = of_rule.build_rule()
        self.send_openflow_command("add-flow", rule_string)



def test():
    """Simple execution to test functionality."""
    server_ip = "192.168.58.102"
    switch = RemoteVSwitch(server_ip, DEFAULT_SWITCH_PORT)
    switch.execute_show_command()
    switch.execute_dump_flows_command()

    rule = OpenFlowRule("ip", "1", None)
    rule.dst_ip = "192.168.57.102"
    switch.set_rule(rule)


if __name__ == "__main__":
    test()
