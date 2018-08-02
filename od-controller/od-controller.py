#OD_IP = "192.168.58.3"
#DOCKER_IP = "192.168.58.4"


import argparse
import time
import json

import config
import opendaylight as od
import policy
import umbox


def run():
    args = parse_arguments()
    configuration = config.get_config(args)

    curr_policy = policy.load_policy(configuration.policy_file)
    current_state = 0
    for i in range(0, curr_policy['n_devices']):
        pass
        ##od.set_new_flow(curr_policy[i]['states'][current_state], curr_policy[i]['flow'],
        ##                curr_policy['in_ip'], curr_policy['out_ip'])

    while True:
        for i in range(0, curr_policy['n_devices']):
            #mbox_name = docker.build_mbox_name(curr_policy[i]['states'][current_state], curr_policy[i]['flow'][current_state])
            #if alert_handler.ping_snort_alert_found(mbox_name):
                next_state = policy.find_next_state(curr_policy, i, current_state)
                if next_state != current_state:
                    #stop_flow(curr_policy[i]['flow'], curr_policy[i]['states'][current_state], args.bridge)
                    current_state = next_state
                    #setup_flow(curr_policy[i]['states'][current_state],
                    #           curr_policy[i]['flow'], curr_policy['in_ip'],
                    #           curr_policy['out_ip'], args.bridge)
            #else:
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

    # print "Switch info: " + json.dumps(od.get_switch_info())
    device_id = "device1"
    umbox.create_and_start_umbox(device_id, curr_config.data_node_ip, "test_umbox", "disk.qcow2", "vboxnet0", "vboxnet1")


if __name__ == '__main__':
    main()
