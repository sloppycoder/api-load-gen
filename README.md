## Load Generator

Use [Locust.io](http://locust.io) to generate continous calls to microservices in order to generate logs and trace entries.


### Quick Start
This project requires (Poetry Python package manager)[https://python-poetry.org/].
```
# install all needed dependencies
poetry install

# start up the venv
poetry shell

# start locust with web console enabled
./entry_point.sh 

# open browser to http://localhost:3000 to see the results

# to run it in minikube
skaffold dev
```

### To work with prometheus
```
poetry shell

# starts master, worker and locust_exporter
./entry_point.sh

```
Update your prometheus config to scrape at port 9464
```
# prometheus.yaml
scrape_configs:
  - job_name: 'locust'
    metrics_path: '/q/metrics'
    scheme: 'http'
    static_configs:
    - targets: ['localhost:8089']

```