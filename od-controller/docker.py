import requests
import json
import re

import config

DOCKER_PORT = "2376"


def build_mbox_name(state_name, state_actions):
    mbox_name = state_name
    if len(state_actions) >= 2:
        for i in range(0, len(state_actions)):
            regex = re.compile('[^a-zA-Z]')
            mbox_name = regex.sub('', state_name) + regex.sub('', state_actions[i]) + str(i)
    return mbox_name


def docker_request(method, request_url, headers={}, payload={}):
    """A generic API request to Docker."""

    url = "http://" + config.get_config().data_node_ip + ":" + DOCKER_PORT + "/containers/" + request_url
    print url
    headers["Content-Type"] = "application/json"

    if method == "post":
        reply = requests.post(url, payload, headers=headers)
    elif method == "delete":
        reply = requests.delete(url, headers=headers)

    print reply
    print reply.content
    return reply.content


def create_and_start_umbox(image_name, container_name):
    # Remove in case it was there.
    docker_request("post", container_name + "/stop")

    config = {"Image": image_name, "AutoRemove": True}

    reply = json.loads(docker_request("post", "create?name=" + container_name, payload=json.dumps(config)))
    container_id = reply['Id']
    print container_id

    docker_request("post", container_name + "/start")

    return container_id


def get_file_from_container(container_name, file_path):
    tar_file = docker_request("get", "{}/archive?path=".format(container_name, file_path))

    # TODO: Untar file.
    file_contents = ""

    # Return file contents.
    return file_contents
