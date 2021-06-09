#!/bin/sh

set -e
trap ctrl_c INT

# kill exporter when ctrl-c the master
# useful when running in terminal
ctrl_c() {
    killall locust_exporter
}

./bin/locust_exporter &

NUM_OF_WORKER="${WORKERS:-1}"
HOST="${HOST:-http://accounts:8080}"
for i in $(seq 1 $NUM_OF_WORKER); 
do 
    locust --host $HOST --worker &
done

locust --master --host $HOST 

# locust --headless --host $HOST --users "${USERS:-1}" 2>&1

