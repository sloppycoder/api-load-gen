import random
import re
import sys

from locust import TaskSet, between, events, task
from locust.contrib.fasthttp import FastHttpUser
from locust.main import main
from data_provider import dataset_for_user

import prometheus_exporter


@events.init.add_listener
def init_prometheus(**kwargs):
    prometheus_exporter.register(**kwargs)


class ApiCallTask(TaskSet):
    def __init__(self, *args, **kwargs):
        super(ApiCallTask, self).__init__(*args, **kwargs)

    @task
    def get_account_detail(self):
        data = self.user.next_call_params()
        url = f"/accounts/{ data['account_number'] }"
        self.client.get(url)


class ApiUser(FastHttpUser):
    tasks = [ApiCallTask]

    def __init__(self, *args, **kwargs):
        super(ApiUser, self).__init__(*args, **kwargs)
        self.dataset = dataset_for_user()

    wait_time = between(2, 5)

    def next_call_params(self):
        r = random.randrange(0, len(self.dataset))
        return self.dataset[r]


if __name__ == "__main__":
    sys.argv[0] = re.sub(r"(-script\.pyw|\.exe)?$", "", sys.argv[0])
    sys.exit(main())
