import random
import re
import sys

from locust import TaskSet, task
from locust.contrib.fasthttp import FastHttpUser
from locust.main import main

from prometheus_exporter import register_exporter

register_exporter()


class ApiCallTask(TaskSet):
    @task
    def get_account_detail(self):
        self.client.get(f"/accounts/{ self.get_test_id() }")

    def get_test_id(self):
        i = random.randrange(0, 10)
        return "11223344" if i > 2 else "gibberish"


class ApiUser(FastHttpUser):
    tasks = [ApiCallTask]

    def __init__(self, *args, **kwargs):
        super(ApiUser, self).__init__(*args, **kwargs)

    def wait_time(self):
        return 0


if __name__ == "__main__":
    sys.argv[0] = re.sub(r"(-script\.pyw|\.exe)?$", "", sys.argv[0])
    sys.exit(main())
