import random
import re
import fastapi
from fastapi import FastAPI
import datagen

app = FastAPI()


class SlowData:
    def __init__(self, args):
        amountToGen = count(args)
        self.err = None

        if amountToGen.err is not None:
            self.err = {"error": amountToGen.err}
            return

        self.first_names = datagen.person_names(amountToGen.first_names, "first")
        self.last_names = datagen.person_names(amountToGen.last_names, "last")


@app.get("/")
def index():
    return "Welcome to AnyGen"


@app.get("/generate")
async def generate(fastapi_req: fastapi.Request):
    data = await fastapi_req.body()
    args = argParser(
        data.decode("utf-8").replace(" ", "").replace("\n", "").replace("\t", "").replace("]", "];").replace("()", "").casefold())

    slow_data = SlowData(args)
    if slow_data.err is not None:
        return slow_data.err

    return generateJson(args, slow_data)


def argParser(input: str) -> list:
    args = []
    start = 0
    brace_count = 0
    for i in range(len(input)):
        char = input[i]

        if char == "[":
            brace_count += 1
        elif char == "]":
            brace_count -= 1

        elif char == ";" and brace_count == 0:
            arg = "".join(input[start:i])
            data = re.split(":", arg, maxsplit=1)

            if "list" in data[1]:
                count_and_args = re.split("\\)", data[1].replace("list(", "", 1), maxsplit=1)
                data.append(argParser(count_and_args[1][1:-1]))
                data.append(int(count_and_args[0]))
                data[1] = "list"

            else:
                params = re.split("[(,]", data[1].replace(")", ""))
                data[1] = params.pop(0)
                if len(params) > 0:
                    data.append(params)

            args.append(list(data))
            start = i + 1

    return args


def generateJson(args: list, slow_data: SlowData):
    json = {}
    names = []
    for raw_arg in args:
        output_name = raw_arg[0]
        arg = raw_arg[1]
        params = []
        if len(raw_arg) == 3:
            params = raw_arg[2]

        match arg:
            case "list":
                json_array = []
                for i in range(raw_arg[3]):
                    json_array.append(generateJson(raw_arg[2], slow_data))

                json[output_name] = json_array
                continue

            case "person_name":
                name = ""
                if "first" in params:
                    name += slow_data.first_names.pop()
                if "last" in params:
                    if len(name) != 0:
                        name += " "
                    name += slow_data.last_names.pop()

                json[output_name] = name
                names.append(name)
                continue

            case "gender":
                json[output_name] = datagen.gender()
                continue

            case "phone_number":
                format = ""
                if "formatted" in params:
                    format = "formatted"

                area_code = None
                for param in params:
                    try:
                        ac = str(int(param))
                        if len(ac) == 3:
                            area_code = ac
                    except ValueError:
                        pass

                json[output_name] = datagen.phone_number(area_code, format)
                continue

            case "email":
                for param in params:
                    if param in json:
                        json[output_name] = datagen.email(str(json[param]))
                        continue

        # Random ints in range
        try:
            ints = arg.split("-")
            int(ints[0])
            json[output_name] = random.randint(int(ints[0]), int(ints[1]))
            continue
        except ValueError:
            pass

    return json


class Counts:
    def __init__(self):
        self.err = None
        self.first_names = 0
        self.last_names = 0
        self.genders = 0
        self.rand_ints = 0
        self.phone_numbers = 0
        self.lorems = 0

    def check(self):
        if self.first_names > 1000 or self.last_names > 1000:
            self.err = "You are trying to generate too many person names! (Max 1000)"
        if self.genders > 10000:
            self.err = "You are tying to generate too many genders! (Max 10000)"
        if self.rand_ints > 10000:
            self.err = "You are trying to generate too many random integers! (Max 10000)"
        if self.phone_numbers > 10000:
            self.err = "You are trying to generate too many phone numbers! (Max 10000)"


def count(args: list):
    counts = Counts()
    for arg in args:
        if arg[1] == "list":
            countsFromList = count(arg[2])
            counts.first_names += countsFromList.first_names * arg[3]
            counts.last_names += countsFromList.last_names * arg[3]
            counts.genders += countsFromList.genders * arg[3]
            counts.phone_numbers += countsFromList.phone_numbers * arg[3]
            counts.rand_ints += countsFromList.rand_ints * arg[3]

        elif arg[1] == "person_name":
            if len(arg) > 2 and len(arg[2]) > 2:
                counts.err = "Too many args in person_name! (max 2, found " + str(len(arg[2])) + ")"
                return counts

            if len(arg) == 2:
                arg.append(["first", "last"])

            if "first" in arg[2]:
                counts.first_names += 1
            if "last" in arg[2]:
                counts.last_names += 1

        elif arg[1] == "gender":
            if len(arg) > 2:
                counts.err = "Too many args in gender! (max 0, found " + str(len(arg[2])) + ")"
                return counts

            counts.genders += 1
            print("test")

        elif arg[1] == "phone_number":
            if len(arg) > 2 and len(arg[2]) > 2:
                counts.err = "Too many args in phone_number! (max 2, found " + str(len(arg[2])) + ")"
                return counts

            counts.phone_numbers += 1

        elif arg[1] == "lorem-ipsum":
            counts.lorems += 1

        try:
            ints = arg[1].split("-")
            int(ints[0])
            counts.rand_ints += 1
            continue
        except ValueError:
            pass

        counts.check()
        if counts.err is not None:
            return counts

    return counts
