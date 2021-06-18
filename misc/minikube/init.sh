#!/bin/bash

MINIKUBE_CONFIG="--driver=kvm2 --disk-size=20000mb --cpus=2 --memory=12288mb --kubernetes-version=1.19.11"
PROFILE=locust

# make sure the required binary exists in PATH before proceeding
check_bin()
{
    if which $1 > /dev/null; then 
        :
    else
        echo cannot find $1 in PATH
        exit 1
    fi
}

check_prereqs() 
{
    check_bin minikube
    check_bin kustomize
}

start_minikube()
{
    echo creating new minikube profile with parameters 
    echo
    echo "      $MINIKUBE_CONFIG "
    echo
    echo ctrl-c to abort in next 5 seconds
    sleep 5

    minikube start -p $PROFILE --wait=all $MINIKUBE_CONFIG

    sleep 2

    minikube profile $PROFILE
    
    if minikube status; then
        echo minikube is ready
    else
        echo minikube is not ready
        exit 2
    fi

}

install_prometheus()
{
    # install prometheus operator using kustomize
    #   https://github.com/prometheus-operator/prometheus-operator
    # see kustomization.yaml for details
    kustomize build operator | minikube kubectl -- apply -f - 
    # let CRDs initialize first, otherwise we'll get errors
    # when provisioning prometheus instance
    sleep 5
    if [ "$USER" = "guru_lin_gmail_com" ]; then
        overlay="gcpkube"
    else
        overlay="minikube"
    fi

    kustomize build appstack/envs/$overlay | minikube kubectl -- apply -f - 
}

check_prereqs
start_minikube
install_prometheus
