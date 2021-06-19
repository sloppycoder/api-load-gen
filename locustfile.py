import re
import sys

from locust import User, events
from locust.main import main

import prometheus_exporter


# this is a dummy class. the actual user logic is in
# worker.go
class DummyUser(User):
    pass


@events.init.add_listener
def init_prometheus(**kwargs):
    prometheus_exporter.register(**kwargs)


if __name__ == "__main__":
    sys.argv[0] = re.sub(r"(-script\.pyw|\.exe)?$", "", sys.argv[0])
    sys.exit(main())
