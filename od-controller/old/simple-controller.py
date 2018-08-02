# Goal: Create simple controller for v0 demo (1 device tunnelling traffic
# through a single snort container, change policy based upon output from
# snort container)
#
# Initial example: Ping (detect then block, but allow tcp)
# 

## Argument Call example: python simple-controller.py -P exp/policy1.json -B br0

import argparse
import ipaddress
import json
import subprocess
import shlex
import itertools
import os
import time
import re
import os.path

## Future Updates
# - Update-FSM_DAG
# -- recognize updates to "policy" and update accordingly
# - Verify


# Get-FSM_DAG
def load_policy(fd):
    with open(fd, 'r') as f:
        json_data = json.load(f)
    f.close

    dev_policy = {}
    dev_policy['policy_description'] = json_data['description']
    dev_policy['nf_platform'] = json_data['nf_platform']
    in_ip = ipaddress.ip_address(json_data['in_ip'])
    out_ip = ipaddress.ip_address(json_data['out_ip'])
    dev_policy['in_ip'] = json_data['in_ip']
    dev_policy['out_ip'] = json_data['out_ip']
    dev_policy['n_devices'] = json_data['n_devices']
    FSM_defs = json_data['FSM_defs']
    DAG_defs = json_data['DAG_defs']
    policy = json_data['policy']

    i = 0
    for device in policy:
        dev_policy[i] = {}
        dev_policy[i]['SM'] = policy[device]['state_machine']
        dev_policy[i]['num_states'] = FSM_defs[dev_policy[i]['SM']]['n']
        dev_policy[i]['states'] = []
        for j in range(0, int(dev_policy[i]['num_states'])):
            dev_policy[i]['states'].append(FSM_defs[dev_policy[i]['SM']][str(j)])
        dev_policy[i]['DAG'] = policy[device]['DAG']
        dev_policy[i]['flow'] = {}
        for k in dev_policy[i]['states']:
            dev_policy[i]['flow'][k] = DAG_defs[dev_policy[i]['DAG']][k].split()
        i += 1

    return dev_policy

#Name mboxes
def find_name(state, name, number):
    regex = re.compile('[^a-zA-Z]')
    new_name=regex.sub('',state)+regex.sub('',name)+str(number)
    return new_name

#Start-up NF Container
def start_nf_container(init_mbox, name):
    cmd = ('/usr/bin/sudo /usr/bin/docker run -itd --rm ' +
           '--network=none --name {} {}')
    cmd = cmd.format(name, init_mbox)
    subprocess.check_call(shlex.split(cmd))


def add_nf_flow(bridge, name, interfaces):
    for interface in interfaces:
        cmd = '/usr/bin/sudo /usr/bin/ovs-docker add-port {} {} {}'
        cmd = cmd.format(bridge, interface, name)
        subprocess.check_call(shlex.split(cmd))
    
def find_of_port(bridge, name, interface):
    cmd = '/usr/bin/sudo '
    cmd += '/usr/bin/ovs-vsctl --data=bare --no-heading --columns=name find \
    interface external_ids:container_id={} external_ids:container_iface={}'
    cmd = cmd.format(name, interface)
    ovs_port = subprocess.check_output(shlex.split(cmd))
    ovs_port = ovs_port.strip()

    cmd = '/usr/bin/sudo /usr/bin/ovs-ofctl show {} | grep {} '
    cmd = cmd.format(bridge, ovs_port)
    cmd += "| awk -F '(' '{ print $1 }'"
    of_port = subprocess.check_output(cmd, shell=True)
    of_port = of_port.strip()

    return of_port


def pairwise(iterable):
    's -> (s0, s1), (s2, s3), (S4, s5), ...'
    a = iter(iterable)
    return itertools.izip(a,a)


def install_route(bridge, flow, name, in_ip, out_ip):
    interfaces = ('eth0', 'eth1')
    of_ports = []
    if(len(flow[name])<2):
        of_ports += [find_of_port(bridge, name, interface) for interface in interfaces]
    else:
        for i in range(0,len(flow[name])):
            mbox_name=find_name(name, flow[name][i],str(i))
            of_ports += [find_of_port(bridge, mbox_name, interface) for interface in interfaces]
    of_ports = [1] + of_ports + [2]

    # From device to mbox to outside
    for in_port, out_port in pairwise(of_ports):
        cmd = '/usr/bin/sudo /usr/bin/ovs-ofctl add-flow {} '.format(bridge)
        cmd+='"priority=100 ip in_port={} nw_src={}"'.format(in_port, in_ip)
        cmd+='" nw_dst={} actions=output:{}"'.format(out_ip, out_port)
        subprocess.check_call(shlex.split(cmd))

    # From outside to mbox to device
    for in_port, out_port in pairwise(reversed(of_ports)):
        cmd = '/usr/bin/sudo /usr/bin/ovs-ofctl add-flow {} '.format(bridge)
        cmd+='"priority=100 ip in_port={} nw_src={}"'.format(in_port, out_ip)
        cmd+='" nw_dst={} actions=output:{}"'.format(in_ip, out_port)
        subprocess.check_call(shlex.split(cmd))

    # All other traffic bypass mbox
    cmd = ('/usr/bin/sudo /usr/bin/ovs-ofctl add-flow {} ' +
           '"priority=0 in_port=1 actions=output:2"').format(bridge)
    subprocess.check_call(shlex.split(cmd))
    cmd = ('/usr/bin/sudo /usr/bin/ovs-ofctl add-flow {} ' +
           '"priority=0 in_port=2 actions=output:1"').format(bridge)
    subprocess.check_call(shlex.split(cmd))


# Setup-flow
# -- input is output of Get-FSM_DAG (or the variable that it creates).
def setup_flow(name, flow, in_ip, out_ip, bridge):
    interfaces = ('eth0', 'eth1')
    if(len(flow[name]))<2:
        init_mbox = flow[name]
        start_nf_container(init_mbox, name)
        add_nf_flow(bridge, name, interfaces)
        install_route(bridge, flow, name, in_ip, out_ip)
    else:
        for i in range(0,len(flow[name])):
            mbox_name=find_name(name, flow[name][i],str(i))
            start_nf_container(flow[name][i], mbox_name)
            add_nf_flow(bridge, mbox_name, interfaces)
        install_route(bridge, flow, name, in_ip, out_ip)

# Turn off flow
def stop_flow(flow, name, bridge):
    interfaces=('eth0', 'eth1')
    if len(flow[name])<2:
        cmd='/usr/bin/sudo /usr/bin/ovs-docker del-ports {} {}'
        cmd=cmd.format(bridge, name)
        subprocess.check_call(shlex.split(cmd))
        cmd='/usr/bin/sudo /usr/bin/docker kill {}'.format(name)
        
    else:
        for i in range(0,len(flow[name])):
            mbox_name=find_name(name, flow[name][i],str(i))
            cmd='/usr/bin/sudo /usr/bin/ovs-docker del-ports {} {}'
            cmd=cmd.format(bridge, mbox_name)
            subprocess.check_call(shlex.split(cmd))
            cmd='/usr/bin/sudo /usr/bin/docker kill {}'.format(mbox_name)
            subprocess.check_call(shlex.split(cmd))
        
    cmd='/usr/bin/sudo /usr/bin/ovs-ofctl del-flows {}'.format(bridge)
    subprocess.check_call(shlex.split(cmd))

    cmd='/usr/bin/sudo /bin/rm -f -- /tmp/alert'
    subprocess.check_call(shlex.split(cmd))
        
# Alert monitor
def alert_monitor(flow, name):
    if len(flow[name])<2:
        mbox_name = name
    else:
        for i in range(0, len(flow[name])):
            if re.search("snort", flow[name][i]):
                mbox_name=find_name(name, flow[name][i],str(i))

    cmd='/usr/bin/sudo /usr/bin/docker cp {}:/var/log/snort/alert /tmp/'
    cmd=cmd.format(mbox_name)
    subprocess.call(shlex.split(cmd))

    if os.path.isfile('/tmp/alert'):
        f = open('/tmp/alert', 'r')
        output=f.read()
        f.close()
    else:
        output=""
        
    if output == "":
        return False
    elif re.search("ICMP", output):
        cmd='/usr/bin/sudo /bin/rm -f -- /tmp/alert'
        subprocess.call(shlex.split(cmd))
        return True


# Find next mbox state number
def find_next_state(policy, device_number, current_state):
    max_states=int(policy[device_number]['num_states'])-1
    if current_state==max_states:
        return current_state
    elif current_state<max_states:
        next_state = current_state+1
        return next_state
        
def main():
    parser = argparse.ArgumentParser(description='Run PSI demo, json policy')
    parser.add_argument('--policy', '-P', required=True, type=str,
                        help='path to json policy file')
    parser.add_argument('--bridge', '-B', required=True, type=str,
                        help='bridge name')
    args = parser.parse_args()

    policy = {}
    policy = load_policy(args.policy)
    current_state = 0
    for i in range(0, policy['n_devices']):
        setup_flow(policy[i]['states'][current_state], policy[i]['flow'],
                   policy['in_ip'], policy['out_ip'], args.bridge)

    next_state = 0
    var = 1
    while var == 1:
        for i in range(0, policy['n_devices']):
            if alert_monitor(policy[i]['flow'], policy[i]['states'][current_state]):
                next_state = find_next_state(policy, i, current_state)
                if next_state != current_state:
                    stop_flow(policy[i]['flow'], policy[i]['states'][current_state], args.bridge)
                    current_state = next_state
                    setup_flow(policy[i]['states'][current_state],
                           policy[i]['flow'], policy['in_ip'],
                           policy['out_ip'], args.bridge)
            else:
                time.sleep(1)


if __name__== '__main__':
    main()
