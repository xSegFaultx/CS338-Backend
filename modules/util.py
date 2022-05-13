import numpy as np


def get_decade(year):
    decade = int(int(year) / 10) * 10
    return str(decade) + "s"


def select_link(links):
    choice = np.random.choice(links)
    extension = choice.strip().split(".")[-1].lower()
    while extension != "jpg" and extension != "jpeg" and extension != "png":
        choice = np.random.choice(links)
        extension = choice.strip().split(".")[-1].lower()
    return choice, extension
