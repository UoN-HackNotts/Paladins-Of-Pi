import requests

## GET REQUEST
# user input source
FRONTEND_URL = "http://localhost:11434/api/generate"

params = {"q": "python", # q=query, carries the search term/main text the client is asking the server about
          "page": 2} # pagination: tells server which page of results are desired


# for visualisation:
# https://api.example.com/search?q=python&page=2


resp = requests.get(FRONTEND_URL, params=params)

# check for errors, specifically the HTTP status code
# if between 200-299, method does nothing
# if 4xx (client) or 5xx (server) then an HTTPError is raised
# why?: prevents the program from silently continuing when something goes wrong
resp.raise_for_status()

user_text = resp.text

## POST JSON REQUEST
obj = {"Original text:", user_text, "processed from client"} # actual text being returned back to the url

post_resp = requests.post(FRONTEND_URL, json=obj)
post_resp.raise_for_status() # check for errors

print("POST response:", post_resp.text)