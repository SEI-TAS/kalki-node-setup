import requests
import json
import config

OD_RESTCONF_PORT = "8181"

# Assuming default auth.
USER = "admin"
PASS = "admin"

NODES_URL = "/opendaylight-inventory:nodes"
FLOW_URL = "/node/{}/table/0/flow/{}"

FLOW_PREFIX = "flow-node-inventory"

# Used to identify a bridge that is not connected to any port, since it is the bridge itself.
BRIDGE_PORT_PLACEHOLDER = 4294967294


def od_restconf_request(method, request_type, request_url, headers={}, payload={}):
    """A generic restconf request to OD."""

    url = "http://" + config.get_config().opendaylight_ip + ":" + OD_RESTCONF_PORT + "/restconf/" + request_type + request_url
    print url
    headers["Accept"] = "application/json"

    if method == "get":
        reply = requests.get(url, headers=headers, auth=(USER, PASS))
    else:
        reply = requests.post(url, payload, headers=headers, auth=(USER, PASS))

    print reply
    print reply.content
    return json.loads(reply.content)


def get_switch_info():
    """Obtains the current switch id from OD."""

    switch_id = ""
    connections = []

    reply = od_restconf_request("get", "operational", NODES_URL)
    print reply

    if len(reply["nodes"]["node"]) > 0:
        json_node = reply["nodes"]["node"][0]

        # Get id.
        if "openflow" in json_node["id"]:
            switch_id = json_node["id"]

        # Get local port and bridge name info.
        for connector in json_node["node-connector"]:
            connection_info = {}

            connection_info["interface"] = connector[FLOW_PREFIX + ":name"]

            connection_info["type"] = "port"
            connection_info["port"] = connector[FLOW_PREFIX + ":port-number"]
            if connection_info["port"] == BRIDGE_PORT_PLACEHOLDER:
                connection_info["port"] = None
                connection_info["type"] = "bridge"

            if "address-tracker:addresses" in connector:
                connection_info["ip"] = connector["address-tracker:addresses"][0]["ip"]
            else:
                connection_info["ip"] = None
            connections.append(connection_info)

    return {"id": switch_id, "connections": connections}


def set_new_flow(switch_id, flow_id, from_port, to_port):
    """Sets a flow for the given switch."""

    defaultPriority = 500
    #flow_instructions.update({"ingressPort": from_port})

    match_data = {}

    action = {}
    action["order"] = 0
    action["output-action"] = {"output-node-connector": to_port, "max-length": 65535}
    instruction_data = {}
    instruction_data["order"] = "0"
    instruction_data["apply-actions"] = {"action": [action]}

    flow_data = {}
    flow_data["strict"] = False
    flow_data["instructions"] = {"instruction": [instruction_data]}
    flow_data["match"] = match_data
    flow_data["table_id"] = 0
    flow_data["id"] = flow_id
    flow_data["cookie_mask"] = 255
    flow_data["installHw"] = False
    flow_data["hard-timeout"] = 12
    flow_data["cookie"] = 4
    flow_data["idle-timeout"] = 34
    flow_data["flow-name"] = ""
    flow_data["priority"] = defaultPriority
    flow_data["barrier"] = False

    flow = {"flow": [flow_data]}

    headers = {"Content-Type": "application/json"}
    reply = od_restconf_request("post", "config", NODES_URL + FLOW_URL.format(switch_id, flow_id),
                                headers=headers, payload=json.dumps(flow))
    return reply


def remove_flow():
    pass
