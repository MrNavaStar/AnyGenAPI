import random
from lorem_text import lorem


def people_names(amount: int, type: str) -> list:
    names = []
    if type == "first":
        with open("data/first_names.csv") as fp:
            data = fp.readlines()
            for i in range(amount):
                names.append(data[random.randint(0, 147268)].replace("\n", ""))
            fp.close()

    if type == "last":
        with open("data/last_names.csv") as fp:
            data = fp.readlines()
            for i in range(amount):
                names.append(data[random.randint(0, 151670)].replace("\n", ""))
            fp.close()

    return names


def gender() -> str:
    if random.randint(0, 1) == 1:
        return "M"
    else:
        return "F"


def lorem_ipsum(amount: int, words: int) -> list:
    lorems = []
    for i in range(amount):
        lorems.append(lorem.words(words))
    return lorems
