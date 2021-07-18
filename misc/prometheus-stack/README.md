## setup prometheus and grafana in minikube

The script and manifest files here are for setting up (Prometheus)[https://prometheus.io/] and (Grafana)[https://grafana.com/] in a (minikube)[] envioronment for collecting metrics during a locust run.

* (Prometheus Operator)[] is used to install Prometheus
* (Grafana )[https://grafana.com/]
* (Kustomize)[https://kustomize.io/] is used to apply manifest to minikue.

### Quick Start
```shell

# create a new minikube profile called locust
# if all goes well a new k8s cluster should be created
# with prometheus operator and instance running in namespace
# promeetheus.
# please make sure minikube and kustomize binaries are available
# in your path before running the following 

./init.sh

# check if prometheus is up
kubectl get prometheus -n prometheus

NAME         VERSION   REPLICAS   AGE
prometheus             1          3m

# check if prometheus UI is exposed
kubectl get svc prometheus -n prometheus

NAME         TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
prometheus   NodePort   10.101.241.60   <none>        9090:30900/TCP   93m

# check if prometheus UI is exposed
kubectl get svc prometheus -n prometheus

NAME         TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
prometheus   NodePort   10.101.241.60   <none>        9090:30900/TCP   93m

# open your browser and look around in Prometheus Web UI and Grafana
# need to setup datasource first time login to Grafana. the prometheus URL 
# is http://prometheus:9090
```

The proceed to run locust. See (project documents)[../README.md] for instructions. If all goes well, you should see timeseries with names like ```python_info``` in Prometheus UI. The data of Prometheus and Grafana are stored on persistent volumes and should remain after minikube restart.
