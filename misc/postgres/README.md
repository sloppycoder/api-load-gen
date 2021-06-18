## Install Postgres using Helm chart

```

helm repo add bitnami https://charts.bitnami.com/bitnami
helm install pg1 bitnami/postgresql -f values.yaml 

# wait a while for everything to be configured
# check release status

helm status pg1

# helm should print something like this:


    pg1-postgresql.default.svc.cluster.local - Read/Write connection

To get the password for "postgres" run:

    export POSTGRES_PASSWORD=$(kubectl get secret --namespace default pg1-postgresql -o jsonpath="{.data.postgresql-password}" | base64 --decode)

To connect to your database run the following command:

    kubectl run pg1-postgresql-client --rm --tty -i --restart='Never' --namespace default --image docker.io/bitnami/postgresql:11.12.0-debian-10-r23 --env="PGPASSWORD=$POSTGRES_PASSWORD" --command -- psql --host pg1-postgresql -U postgres -d postgres -p 5432

To connect to your database from outside the cluster execute the following commands:

    kubectl port-forward --namespace default svc/pg1-postgresql 5432:5432 &
    PGPASSWORD="$POSTGRES_PASSWORD" psql --host 127.0.0.1 -U postgres -d postgres -p 5432


```

