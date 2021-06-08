## Load Generator

Use [Locust.io](http://locust.io) to generate continous calls to microservices in order to generate logs and trace entries.


### Quick Start
This project requires (Poetry Python package manager)[https://python-poetry.org/].
```
# install all needed dependencies
poetry install

# start up the venv
poetry shell

# start locust
locust 

# open browser to http://localhost:3000 to see the results

# to run it in minikube
skaffold dev
```

The ```prometheus_exporter.py``` has not been tested yet.
