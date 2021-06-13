# provides test data to locust User
# can be customized to provide data using different strategy:
# e.g.
#     each user gets same data
#     each user gets different data

import csv
import os
import os.path
import sys

all_data = None


def read_data_set():
    global all_data

    data_file = os.environ.get("API_DATA_FILE", "/data/data.csv")
    if not os.path.isfile(data_file):
        data_file = "dummy_data.csv"

    with open(data_file) as file:
        header = file.readline().strip()
        reader = csv.DictReader(file, header.split(","))
        all_data = [row for row in reader]
        mem = int(sys.getsizeof(all_data) / (1024 * 1024))
        print(f"test data from {data_file} loaded, uses {mem}M of memory")


def dataset_for_user():
    if all_data is None:
        read_data_set()
    return all_data


if __name__ == "__main__":
    dataset_for_user()
    for row in all_data[:20]:
        print(row)
