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
    d = data.decode("utf-8").replace(" ", "").replace("\n", "").replace("\t", "").replace("]", "];").casefold()
    args = argParser(d)

    print(data.decode("utf-8"))

    print(args)
    print(count(args))


def argParser(input: str) -> list:
    args = []
    start = 0
    brace_count = 0
    for i in range(len(input)):
        char = input[i]

        if char == "[":
            brace_count += 1
        if char == "]":
            brace_count -= 1

        if char == ";" and brace_count == 0:
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


def generateJson2(args: list, json: list):
    amountToGen = count(args)


def count(args: list):
    c = 0
    c1 = 0
    for arg in args:
        if arg[1] == "list":
            counts = count(arg[2])
            c += counts[0] * arg[3]
            c1 += counts[1] * arg[3]

        elif arg[1] == "people-names":
            c += 1
        elif arg[1] == "lorem-ipsum":
            c1 += 1

    return [c, c1]



if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)