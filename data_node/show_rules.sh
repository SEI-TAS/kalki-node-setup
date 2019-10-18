#!/bin/bash
watch -n 1 sudo ovs-ofctl -O OpenFlow13 dump-flows ovs-br
