
class Config:

    policy_file = ""
    opendaylight_ip = ""
    data_node_ip = ""

    def __init__(self, args):
        if hasattr(args, 'policy'):
            self.policy_file = args.policy
        if hasattr(args, 'odip'):
            self.opendaylight_ip = args.odip
        if hasattr(args, 'dnip'):
            self.data_node_ip = args.dnip

