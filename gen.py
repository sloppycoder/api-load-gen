import numpy as np
import matplotlib.pyplot as plt


def plot(data, mu=0, sigma=2):
    count, bins, ignored = plt.hist(data, 30, density=True, stacked=True)
    plt.plot(
        bins,
        1
        / (sigma * np.sqrt(2 * np.pi))
        * np.exp(-((bins - mu) ** 2) / (2 * sigma ** 2)),
        linewidth=2,
        color="r",
    )
    plt.show()


def gen_random(size=100, mu=0, sigma=2):
    dataset = np.random.normal(mu, sigma, 1000)
    # dataset.sort()
    return dataset


np.random.seed(1234567890)
data = gen_random()
plot(data)
