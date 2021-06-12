#!/bin/bash

print_urls()
{
    HOST=$(minikube ip)
    PROMETHEUS_PORT=$(kubectl get svc prometheus -n prometheus -o jsonpath="{.spec.ports[?(@.port=="9090")].nodePort}")
    GRAFANA_PORT=$(kubectl get svc grafana -n prometheus -o jsonpath="{.spec.ports[?(@.port=="3000")].nodePort}")

    echo Prometheus:  http://$HOST:$PROMETHEUS_PORT
    echo Grafana:  http://$HOST:$GRAFANA_PORT
    echo 
    echo  Please use http://prometheus:9090 as Prometheus data source URL when adding data source.
}

print_urls

