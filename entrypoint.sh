#!/bin/sh

set -e

locust --headless --host http://accounts:8080 --users "${USERS:-1}" 2>&1

