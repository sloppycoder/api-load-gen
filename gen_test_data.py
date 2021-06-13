import random
import sys

accounts = ["12345657", "23343435435", "23432k432", "gigelwjr", "lkjlja"]
groups = ["acn", "scb", "ktb"]


def gen_test_csv(n, file_name):
    n_accounts = len(accounts)
    n_groups = len(groups)
    with open(file_name, "w") as file:
        file.write("group_id,account_number,balance_date,extra\n")
        for i in range(n):
            acc = accounts[random.randrange(0, n_accounts)]
            grp = groups[random.randrange(0, n_groups)]
            some_date = rand_date()
            file.write(f"{grp},{acc},{some_date},\n")


def rand_date():
    return "20200101"


if __name__ == "__main__":
    n, file_name = 1, "test_data.csv"
    try:
        n = int(sys.argv[1])
        file_name = sys.argv[2]
    except:
        pass

    gen_test_csv(n, file_name)
