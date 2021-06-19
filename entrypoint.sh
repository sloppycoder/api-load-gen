#!/bin/sh

set -e

NUM_OF_WORKER="${WORKERS:-1}"
HOST="${HOST:-http://accounts:8080}"

for i in $(seq 1 $NUM_OF_WORKER);
do
    ./worker --host $HOST $WORKER_PARAMS &
done

locust --master --host $HOST

# locust --headless --host $HOST --users "${USERS:-1}" 2>&1

