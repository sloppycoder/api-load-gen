import re
import sys

from locust import TaskSet, between, events, task

# from locust import HttpUser
from locust.contrib.fasthttp import FastHttpUser as HttpUser
from locust.main import main

import prometheus_exporter
from data_provider import next_call_params


@events.init.add_listener
def init_prometheus(**kwargs):
    prometheus_exporter.register(**kwargs)


class ApiCallTask(TaskSet):
    def __init__(self, *args, **kwargs):
        super(ApiCallTask, self).__init__(*args, **kwargs)

    @task
    def get_account_detail(self):
        name, url, headers, _ = next_call_params()
        self.client.get(url, name=name, headers=headers)


class ApiUser(HttpUser):
    tasks = [ApiCallTask]

    def __init__(self, *args, **kwargs):
        super(ApiUser, self).__init__(*args, **kwargs)
        self.dataset = []

    wait_time = between(5, 10)


if __name__ == "__main__":
    sys.argv[0] = re.sub(r"(-script\.pyw|\.exe)?$", "", sys.argv[0])
    sys.exit(main())
