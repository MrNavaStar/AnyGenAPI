import random
from lorem_text import lorem

email_domains = ["yahoo.ca", "yahoo.com", "aol.com", "verizon.net", "optonline.net", "comcast.net", "msn.com",
                 "live.com", "sbcglobal.net", "icloud.com", "att.net", "hotmail.com", "hotmail.ca", "me.com",
                 "gmail.com", "mac.com", "outlook.com", "telus.net"]


def person_names(amount: int, type: str) -> list:
    names = []
    if type == "first":
        with open("data/first_names") as fp:
            data = fp.readlines()
            for i in range(amount):
                names.append(data[random.randint(0, 147268)].replace("\n", ""))
            fp.close()

    if type == "last":
        with open("data/last_names") as fp:
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


def phone_number(area_code: str, format: str):
    number = ""
    if area_code is not None:
        number += area_code
    else:
        for i in range(3):
            number += str(random.randint(0, 9))

    for i in range(7):
        number += str(random.randint(0, 9))

    if format == "":
        return int(number)

    if format == "formatted":
        formatted = ""
        for i in range(len(number)):
            char = number[i]

            if i == 3 or i == 6:
                formatted += "-"
            formatted += char
        return formatted


def email(prefix: str):
    return prefix.replace(" ", ".").lower() + "@" + email_domains[random.randint(0, 17)]


def lorem_ipsum(amount: int, words: int) -> list:
    lorems = []
    for i in range(amount):
        lorems.append(lorem.words(words))
    return lorems
