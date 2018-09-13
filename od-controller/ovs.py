import subprocess

OF_COMMAND_BASE = "sudo ovs-ofctl -O OpenFlow13"
OF_COMMAND_SERVER = "tcp:{}:{}"
OF_PORT = 6653


def send_openflow_command(command, server_ip):
    try:
        server_info = OF_COMMAND_SERVER.format(server_ip, OF_PORT)
        full_command = OF_COMMAND_BASE + " " + command + " " + server_info
        print("Executing command: " + full_command)
        output = subprocess.check_output(full_command)
        print("Output of command: " + output)
    except subprocess.CalledProcessError, e:
        print("Error executing command: " + str(e))


def execute_show_command(server_ip):
    send_openflow_command("show", server_ip)


def execute_dump_flows_command(server_ip):
    send_openflow_command("dump-flows", server_ip)


def test():
    server_ip = "192.168.58.102"
    execute_show_command(server_ip)
    execute_dump_flows_command(server_ip)

if __name__ == "__main__":
    test()
