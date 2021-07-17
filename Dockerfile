FROM python:3.8-slim-buster as base

FROM base as builder
RUN apt-get -qq update \
    && apt-get install -y --no-install-recommends \
        file \
        g++ \
        libffi-dev

COPY requirements.txt .
RUN pip install --root="/install" -r requirements.txt

FROM base
RUN apt-get -qq update \
    && apt-get install -y --no-install-recommends \
        procps \
        net-tools \
        dnsutils \
        vim-tiny \
        curl \
        jq

COPY --from=builder /install /
COPY entrypoint.sh *.py dummy.csv /

EXPOSE 8089

ENTRYPOINT ./entrypoint.sh

