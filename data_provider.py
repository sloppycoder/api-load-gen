import csv
import os
import os.path
import random
import sys
import uuid

_ALL_DATA_ = None
_USE_RANDOM_ = os.environ.get("USE_RANDOM", "False").lower() in ["true", "yes", "y"]
if _USE_RANDOM_:
    print("Use random account id")


def read_test_datafile():
    global _ALL_DATA_
    if _ALL_DATA_ is not None:
        return _ALL_DATA_

    data_file = os.environ.get("API_DATA_FILE", "dummy.csv")
    with open(data_file) as file:
        header = file.readline().strip()
        reader = csv.DictReader(file, header.split(","))
        _ALL_DATA_ = [row for row in reader]
        mem = int(sys.getsizeof(_ALL_DATA_) / (1024 * 1024))
        print(f"test data from {data_file} loaded, uses {mem}M of memory")

    if _ALL_DATA_ is not None:
        return _ALL_DATA_

    raise "Unable to read test data"


def next_call_params():
    """ randomly pick 1 record from the data set """
    global _USE_RANDOM_

    dataset = read_test_datafile()
    i = random.randrange(0, len(dataset), 1)
    params = dataset[i]
    group_id, account_num, asof, api_name = (
        params["GroupId"],
        params["AccountNumber"],
        params["Date"],
        "/accounts/<account>",
    )

    if _USE_RANDOM_:
        account_num = "random"
        asof = ""
        api_name = "/accounts/random"

    url = f"/accounts/{account_num}"
    url += f"/{asof}" if asof else ""
    headers = {"GroupId": group_id, "CorrelationId": str(uuid.uuid4())}

    return api_name, url, headers, {}


if __name__ == "__main__":
    for _ in range(10):
        print(next_call_params())
