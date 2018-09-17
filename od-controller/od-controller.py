
import argparse
import time

import config
import opendaylight as od
import policy
import umbox


def run(policy_file):
    curr_policy = policy.load_policy(policy_file)
    current_state = 0
    for i in range(0, curr_policy['n_devices']):
        pass
        od.set_new_flow(curr_policy[i]['states'][current_state], curr_policy[i]['flow'],
                        curr_policy['in_ip'], curr_policy['out_ip'])

    while True:
        for i in range(0, curr_policy['n_devices']):
            mbox_name = umbox.build_mbox_name(curr_policy[i]['states'][current_state], curr_policy[i]['flow'][current_state])

            # TODO: add way to check if a rule is found.
            next_step_is_needed = True
            if next_step_is_needed:
                next_state = policy.find_next_state(curr_policy, i, current_state)
                if next_state != current_state:
                    #od.remove_flow(curr_policy[i]['flow'], curr_policy[i]['states'][current_state], args.bridge)
                    current_state = next_state
                    #od.remove_flow(curr_policy[i]['states'][current_state],
                    #           curr_policy[i]['flow'], curr_policy['in_ip'],
                    #           curr_policy['out_ip'], args.bridge)
            else:
                time.sleep(100)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Kalki Controller v 0.1')
    parser.add_argument('--policy', '-P', required=False, type=str,
                        help='path to json policy file')
    parser.add_argument('--odip', '-O', required=False, type=str,
                        help='IP of OpenDaylight restconf API')
    parser.add_argument('--dnip', '-D', required=True, type=str,
                        help='IP of the Data Node')
    args = parser.parse_args()
    return args


def main():
    # Setup configuration
    print "Setting up config."
    curr_config = config.Config(parse_arguments())

    #run(curr_config.policy_file)

    # Test code.
    # print "Switch info: " + json.dumps(od.get_switch_info())
    device_id = "1"
    data_bridge_iface = "ovs-br"   # OpenVS bridge
    control_bridge_iface = "br-control"
    disk_image_path = "/home/kalki/images/test_image.qcow2"
    umbox.create_and_start_umbox(device_id, curr_config.data_node_ip, "test_umbox", disk_image_path,
                                 data_bridge_iface, control_bridge_iface)


if __name__ == '__main__':
    main()
