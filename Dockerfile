FROM python:3.8-slim-buster as base


# python builder for locust
FROM base as pybuilder
RUN apt-get -qq update \
    && apt-get install -y --no-install-recommends \
        file \
        g++ \
        libffi-dev
COPY requirements.txt .
RUN pip install --root="/install" -r requirements.txt


# golang builder for worker
FROM golang:1.14 as gobuilder
WORKDIR /build
ADD . /build
RUN go build -o worker worker.go


# we put some utilities in the runtime container
# so that we can shell in to troubleshoot when 
# neccessary
FROM base
RUN apt-get -qq update \
    && apt-get install -y --no-install-recommends \
        procps \
        net-tools \
        dnsutils \
        vim-tiny \
        curl \
        jq

COPY --from=pybuilder /install /
COPY --from=gobuilder /build/worker /
COPY entrypoint.sh locustfile.py prometheus_exporter.py  dummy_data.csv /

USER 1000

EXPOSE 8089
ENTRYPOINT ./entrypoint.sh

