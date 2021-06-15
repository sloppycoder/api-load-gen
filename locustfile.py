import random
import re
import sys
import uuid

from locust import TaskSet, between, events, task
from locust.contrib.fasthttp import FastHttpUser
from locust.main import main

import prometheus_exporter
from data_provider import dataset_for_user


@events.init.add_listener
def init_prometheus(**kwargs):
    prometheus_exporter.register(**kwargs)


class ApiCallTask(TaskSet):
    def __init__(self, *args, **kwargs):
        super(ApiCallTask, self).__init__(*args, **kwargs)

    @task
    def get_account_detail(self):
        data = self.user.next_call_params()
        # url = f"/accounts/{ data['account_number'] }"
        url = f"/accounts/v2/{ data['account_number'] }/2020-12-25"
        headers = {"GroupId": data["group_id"], "CorrelationId": str(uuid.uuid4())}
        self.client.get(url, headers)


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
