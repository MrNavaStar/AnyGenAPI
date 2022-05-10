import random
from lorem_text import lorem


# params[0] = params from request
# params[1] = amount of elements to be generated
def people_names(params: list) -> list:
    names = []
    if "first" in params[0]:
        with open("data/first_names.csv") as fp:
            data = fp.readlines()
            for i in range(params[1]):
                names.append(data[random.randint(0, 147269)].split(",")[0])
    return names


def genders(amount: int) -> list:
    genders = []
    for i in range(amount):
        if random.randint(0, 1) == 1:
            genders.append("M")
        else:
            genders.append("F")
    return genders


def numbers(min: int, max: int, amount: int) -> list:
    ints = []
    for i in range(amount):
        ints.append(random.randint(min, max))
    return ints


def lorem_ipsum(params: list) -> list:
    lorems = []
    for i in range(params[1]):
        lorems.append(lorem.words(params[0]))
    return lorems
