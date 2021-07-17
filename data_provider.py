import csv
import os
import os.path
import random
import sys
import uuid

_ALL_DATA_ = None


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
    dataset = read_test_datafile()
    i = random.randrange(0, len(dataset), 1)
    params = dataset[i]
    group_id, account_num, asof = (
        params["GroupId"],
        params["AccountNumber"],
        params["Date"],
    )
    headers = {"GroupId": group_id, "CorrelationId": str(uuid.uuid4())}
    url = f"/accounts/v2/{account_num}"
    api_name = "/accounts/v2/<account>"
    if asof is not None:
        url += f"/{asof}"
        api_name += "/asOf"
    return api_name, url, headers, {}


if __name__ == "__main__":
    for _ in range(10):
        print(next_call_params())
