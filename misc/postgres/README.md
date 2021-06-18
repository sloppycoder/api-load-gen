## Install Postgres using CrunchyData operator

Follow this [Quick Start Guide](https://access.crunchydata.com/documentation/postgres-operator/4.7.0/quickstart/)

```
# install the operator
kubectl create namespace pgo
kubectl apply -f \ 
https://raw.githubusercontent.com/CrunchyData/postgres-operator/v4.7.0/installers/kubectl/postgres-operator.yml

# check operator installation
kubectl -n pgo get deployments
kubectl -n pgo get pods

# install the client, some manual steps involved
curl https://raw.githubusercontent.com/CrunchyData/postgres-operator/v4.7.0/installers/kubectl/client-setup.sh > client-setup.sh
chmod +x client-setup.sh
./client-setup.sh

# add the following to your .bash_profile or .zshrc
export PGOUSER="${HOME?}/.pgo/pgo/pgouser"
export PGO_CA_CERT="${HOME?}/.pgo/pgo/client.crt"
export PGO_CLIENT_CERT="${HOME?}/.pgo/pgo/client.crt"
export PGO_CLIENT_KEY="${HOME?}/.pgo/pgo/client.key"
export PGO_APISERVER_URL='https://127.0.0.1:8443'
export PGO_NAMESPACE=pgo


# the operator port is not directly accessible from outside cluster 
# for security reason, start proxy first
kubectl -n pgo port-forward svc/postgres-operator 8443:8443 &

# if this command prints out version the CLI can talk to operator successfully
pgo version

# create cluster
pgo create cluster hippo

# show user credential
pgo show user -n pgo hippo

# update your application database connection info


```

