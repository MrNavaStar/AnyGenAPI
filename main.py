import random
import re
import fastapi
from fastapi import FastAPI
import datagen

app = FastAPI()


class SlowData:
    def __init__(self, args):
        amountToGen = count(args)
        self.first_names = datagen.people_names(amountToGen.first_names, "first")
        self.last_names = datagen.people_names(amountToGen.last_names, "last")


@app.get("/")
def index():
    return "Welcome to AnyGen"


@app.get("/generate")
async def generate(fastapi_req: fastapi.Request):
    data = await fastapi_req.body()
    args = argParser(data.decode("utf-8").replace(" ", "").replace("\n", "").replace("\t", "").replace("]", "];").casefold())
    print(args)
    return generateJson2(args, SlowData(args))


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


def generateJson2(args: list, slow_data: SlowData):
    json = {}
    for raw_arg in args:
        output_name = raw_arg[0]
        arg = raw_arg[1]
        params = None
        if len(raw_arg) == 3:
            params = raw_arg[2]

        match arg:
            case "list":
                json_array = []
                for i in range(raw_arg[3]):
                    json_array.append(generateJson2(raw_arg[2], slow_data))

                json[output_name] = json_array
                continue

            case "people-names":
                name = ""
                if "first" in params:
                    name += slow_data.first_names.pop()
                if "last" in params:
                    if len(name) != 0:
                        name += " "
                    name += slow_data.last_names.pop()

                json[output_name] = name
                continue

            case "gender":
                json[output_name] = datagen.gender()

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
        self.first_names = 0
        self.last_names = 0

        self.lorems = 0


def count(args: list) -> Counts:
    counts = Counts()
    for arg in args:
        if arg[1] == "list":
            countsFromList = count(arg[2])
            counts.first_names += countsFromList.first_names * arg[3]
            counts.last_names += countsFromList.last_names * arg[3]

        elif arg[1] == "people-names":
            if len(arg) == 2:
                arg.append(["first", "last"])

            if "first" in arg[2]:
                counts.first_names += 1
            if "last" in arg[2]:
                counts.last_names += 1

        elif arg[1] == "lorem-ipsum":
            counts.lorems += 1

    return counts
