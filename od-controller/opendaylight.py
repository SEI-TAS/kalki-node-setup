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


def set_new_flow(switch_id, flow_id):
    """Sets a flow for the given switch."""

    flow_instructions = {}

    headers = {"Content-Type": "application/xml"}
    reply = od_restconf_request("post", "config", NODES_URL + FLOW_URL.format(switch_id, flow_id),
                                headers=headers, payload=flow_instructions)


def remove_flow():
    pass
