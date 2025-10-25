import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

template = """You are a tone engine.
Input: {input_text}
Instruction: Rewrite the input to be written in Shakespearean.
"""

input_text = ""
prompt = template.format(input_text=input_text)

params = {"q": "python", # q=query, carries the search term/main text the client is asking the server about
          "page": 2} # pagination: tells server which page of results are desired


# for visualisation:
# https://api.example.com/search?q=python&page=2


resp = requests.get(OLLAMA_URL, params=params)

# check for errors, specifically the HTTP status code
# if between 200-299, method does nothing
# if 4xx (client) or 5xx (server) then an HTTPError is raised
# why?: prevents the program from silently continuing when something goes wrong
resp.raise_for_status()

data = resp.json()
print(data)