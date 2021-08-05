## Load Generator

[![Build a container image and publish to GitHub package](https://github.com/sloppycoder/api-load-gen/actions/workflows/build.yaml/badge.svg)](https://github.com/sloppycoder/api-load-gen/actions/workflows/build.yaml)


Use [Locust.io](http://locust.io) to generate continous calls to microservices for performance testing.
The load generation uses [Boomer](https://github.com/myzhan/boomer) for ability to generate large amount of requests with load CPU oerhead.



### Quick Start
This project requires (Poetry Python package manager)[https://python-poetry.org/].
```
# install all needed dependencies
poetry install

# start up the venv
poetry shell

# start locust with web console enabled
./entry_point.sh

# open browser to http://localhost:8089 to see the results

# to run it in minikube
skaffold dev
```

### To work with prometheus in Minikube
See [this README](misc/minikube/README.md) for instruction to run locust, Prometheus and Grafana in Minkube.

### Test Data
This script reads test data from CSV file at run time. The name of the csv file is /data/data.csv and can be overriden by API_DATA_FILE environment variable. When running inside K8S environment, to use new data for testing, just copy the data file into the persistent volume, e.g. ''' kubectl cp data.csv api-load-gen-7cc7899d78-vkxcs:/data/. ''' and then kill the pod. A new pod will be started which will use new data file for testing.
