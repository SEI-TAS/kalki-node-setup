#!/bin/sh
set -e

container=$1

echo -n "Waiting for postgres container $container..."

while ! docker logs $container 2>&1 | grep 'init process complete'; do
  echo -n .
  sleep 1
done

echo "Postrgres container finished initialization"

exec "${@:2}"
