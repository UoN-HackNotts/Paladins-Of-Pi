import json
def story(user_input, stat):
    """
    Logs text inputs into a dictionary in json
    """

    entry={"user" if stat else "ai": user_input}
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    data.append(entry)

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)