import json
def story(user_input, stat):
    """
    Logs text inputs into a dictionary in json
    """

    if(stat):
        entry={"user": user_input}
    else:
        entry={"ai": user_input}
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    data.append(entry)

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)