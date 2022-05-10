import re
import fastapi
import uvicorn
from fastapi import FastAPI
import datagen

app = FastAPI()


@app.get("/")
def index():
    return "Welcome to AnyGen"


@app.get("/generate")
async def generate(fastapi_req: fastapi.Request):
    data = await fastapi_req.body()
    args = dataParser(data)


    print(data.decode("utf-8"))
    print(args)
    print(count("people-names", args))


# Parse the cleaned data into a "nice" list
def argParser(template: list) -> list:
    args = []
    for arg in template:
        data = re.split(":", arg, maxsplit=1)

        if "list" in data[1]:
            count_and_args = re.split("\\)", data[1].replace("list(", "", 1), maxsplit=1)
            new_template = list(filter(None, "".join(count_and_args[1].replace("[", "", 1).rsplit("]", 1)).split("#")))
            data.append(argParser(new_template))
            data.append(int(count_and_args[0]))
            data[1] = "list"

        else:
            params = re.split("\\(|,", data[1].replace(")", ""))
            data[1] = params.pop(0)
            if len(params) > 0:
                data.append(params)

        args.append(data)
    return args


# Convert raw data to a format that can be more easily parsed
def dataParser(data: bytes) -> list:
    data = list(data.decode("utf-8").replace(" ", "").replace("\n", "").replace("]", "];").casefold())

    out = []
    brace_count = 0
    j = 0
    for i in range(len(data)):
        char = data[i]
        if char == "[":
            brace_count += 1
        if char == "]":
            brace_count -= 1

        if char == ";" and brace_count > 0:
            data[i] = "#"
        if char == ";" and brace_count == 0:
            out.append("".join(data[j:i]))
            j = i + 1
    template = list(filter(None, out))
    print(template)
    return argParser(template)


def generateJson(args: list, json: list):
    for arg in args:
        output_name = arg[0]
        arg = arg[1]
        params = None
        if len(arg) == 3:
            params = arg[2]

        match arg:
            case "people-names":
                if params is None:
                    params = ["first", amount]

                names = datagen.people_names(params)
                for i in range(len(names)):
                    json[i] = json[i] | {output_name: names[i]}
                continue

            case "gender":
                genders = datagen.genders(amount)
                for i in range(len(genders)):
                    json[i] = json[i] | {output_name: genders[i]}
                continue

            case "lorem-ipsum":
                if params is None:
                    params = [5, amount]

                lorems = datagen.lorem_ipsum(params)
                for i in range(len(lorems)):
                    json[i] = json[i] | {output_name: lorems[i]}
                continue

        # Random ints in range
        try:
            ints = arg.split("-")
            int(ints[0])
            numbers = datagen.numbers(int(ints[0]), int(ints[1]), amount)
            for i in range(len(numbers)):
                json[i] = json[i] | {output_name: numbers[i]}
            continue
        except ValueError:
            pass


def count(arg_name: str, args: list):
    c = 0
    for arg in args:
        if arg[1] == arg_name:
            c += 1

        if arg[1] == "list":
            print(arg[2])
            print(arg[3])
            c += count(arg_name, arg[2]) * arg[3]
    return c


#def betterGenerateJson(args: list, json: list):


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)