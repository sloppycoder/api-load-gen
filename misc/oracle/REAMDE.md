## Run Oralce inside kubernetes

```
# create a secret for image pull
# it's required for this image

kubectl create secret docker-registry regcred --docker-server=https://docker.io --docker-username=<username> --docker-password=<password> --docker-email=<email>

kubectl apply -f deployment.yaml

# wait a few minutes for the database to initialize
# then shell into the container

sqlplus / as sysdba

ALTER SESSION SET CONTAINER = ORCLPDB1;

-- disable the annoying password rules first
alter profile DEFAULT limit PASSWORD_REUSE_TIME unlimited;
alter profile DEFAULT limit PASSWORD_LIFE_TIME  unlimited;
alter profile DEFAULT limit FAILED_LOGIN_ATTEMPTS unlimited;
alter profile DEFAULT limit password_verify_function null;

create user qldsview identified by qldsview ;
grant create session, unlimited tablespace, resource to qldsview;

```
