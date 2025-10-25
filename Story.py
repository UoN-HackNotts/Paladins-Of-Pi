import json
def story(input, stat):

    if(stat):
        entry={"user": input}
    else:
        entry={"ai": input}
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    data.append(entry)

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)