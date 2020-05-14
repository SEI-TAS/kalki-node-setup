#!/usr/bin/env bash
export http_proxy='';
curl -s -o /dev/null -w "Status: %{http_code}\n" -u Username:Password http://localhost:9010/test_server.sh
