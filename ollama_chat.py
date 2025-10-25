import requests
from flask import Flask, request, jsonify
from Story import story

app = Flask(__name__)

## GET REQUEST (FROM WEBSITE)
# user input source
FRONTEND_URL = "http://localhost:8501/generate" # might be 8501
LLM_URL = "http://localhost:11434/api/generate" # ollama

@app.route("/generate", methods=["GET"])
def generate(): # handler for HTTP GET/generate

    # for visualisation:
    # https://api.example.com/search?q=python&page=2

    """
    Takes in the input from the website using flask request (NOT requests)
    """
    user_text = (request.args.get("q") or "").strip() # .strip() removes redundant chars, "" is a fallback if "q" not found

    story(user_text, True)

    """
    ## LLM ONLY
    # exception handling (WIP)
    params = {"q": "python", # q=query, carries the search term/main text the client is asking the server about
            "page": 2} # pagination: tells server which page of results are desired

    try:
        resp = requests.get(LLM_URL, params=params)

        # check for errors, specifically the HTTP status code
        # if between 200-299, method does nothing
        # if 4xx (client) or 5xx (server) then an HTTPError is raised
        # why?: prevents the program from silently continuing when something goes wrong
        resp.raise_for_status()

        user_text = resp.text

    except requests.exceptions.HTTPError as err:
        pass
    """

    """
    LLM output
    """
    payload = {"model": "phi3", "prompt": user_text, "stream": False} # sends the text as a prompt (TEMPORARY)
    llm_resp = requests.post(LLM_URL, json=payload, timeout=15)
    llm_resp.raise_for_status()
    llm_json = llm_resp.json() # gets raw json file of llm's output

    ai_text = llm_json.get("response") or llm_json.get("generated") or llm_json.get("text") or "" # tries combinations to extracting json from inpt

    return jsonify({
        "input": user_text,
        "ai_text": ai_text,
        

    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)