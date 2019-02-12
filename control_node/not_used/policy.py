import json


# - Update-FSM_DAG
# -- recognize updates to "policy" and update accordingly
def load_policy(fd):
    with open(fd, 'r') as f:
        json_data = json.load(f)
    f.close()

    dev_policy = {}
    dev_policy['policy_description'] = json_data['description']
    dev_policy['nf_platform'] = json_data['nf_platform']
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


# Find next state number
def find_next_state(policy, device_number, current_state):
    max_states = int(policy[device_number]['num_states']) - 1
    if current_state == max_states:
        return current_state
    elif current_state < max_states:
        next_state = current_state + 1
        return next_state
