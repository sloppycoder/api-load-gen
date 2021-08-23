import re
import sys

from locust import LoadTestShape, TaskSet, constant_pacing, events, task

# from locust import HttpUser
from locust.contrib.fasthttp import FastHttpUser as HttpUser
from locust.main import main

import prometheus_exporter
from data_provider import get_test_stages, next_call_params


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

    wait_time = constant_pacing(0.1)


class StagesShape(LoadTestShape):
    """
    A simply load test shape class that has different user and spawn_rate at
    different stages.
    Keyword arguments:
        stages -- A list of dicts, each representing a stage with the following keys:
            duration -- When this many seconds pass the test is advanced to the next stage
            users -- Total user count
            spawn_rate -- Number of users to start/stop per second
            stop -- A boolean that can stop that test at a specific stage
        stop_at_end -- Can be set to stop once all stages have run.

    e.g.

    stages = [
        {"duration": 60, "users": 10, "spawn_rate": 10},
        {"duration": 120, "users": 20, "spawn_rate": 10},
        {"duration": 180, "users": 100, "spawn_rate": 10},
        {"duration": 240, "users": 30, "spawn_rate": 10},
        {"duration": 300, "users": 10, "spawn_rate": 10},
        {"duration": 360, "users": 1, "spawn_rate": 1},
    ]

    """

    def tick(self):
        run_time = self.get_run_time()

        for stage in get_test_stages():
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                print(tick_data)
                return tick_data

        return None


if __name__ == "__main__":
    sys.argv[0] = re.sub(r"(-script\.pyw|\.exe)?$", "", sys.argv[0])
    sys.exit(main())
