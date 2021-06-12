#!/bin/bash

MINIKUBE_CONFIG="--driver=kvm2 --disk-size=20000mb --cpus=2 --memory=8192mb --kubernetes-version=1.19.11"
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
    if [ "$1" = "--create" ]; then

        echo creating new minikube profile with parameters 
        echo
        echo "      $MINIKUBE_CONFIG "
        echo
        echo ctrl-c to abort in next 5 seconds
        sleep 5

        minikube start -p $PROFILE --wait=all $MINIKUBE_CONFIG

    else 
        if minikube profile list | grep $PROFILE ; then
            
            minikube start -p $PROFILE --wait=all

        else 
            echo minikube profile $PROFILE does not exists
            exit 3
        fi
    fi

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
    kustomize build . | minikube kubectl -- apply -f - 
}

check_prereqs
start_minikube $1
install_prometheus
