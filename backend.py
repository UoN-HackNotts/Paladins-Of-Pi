import requests
from flask import Flask, request, jsonify
from Story import story

app = Flask(__name__)

## GET REQUEST (FROM WEBSITE)
LLM_URL = "http://localhost:11434/api/generate" # ollama
LLM_TIMEOUT = 40

@app.route("/generate", methods=["GET"])
def generate(): # handler for HTTP GET/generate
    """
    Takes in the input from the website using flask request (NOT requests)
    """
    user_text = (request.args.get("q") or "").strip() # .strip() removes redundant chars, "" is a fallback if "q" not found

    story(user_text, True)

    """
    LLM output
    """
    payload = {"model": "phi3", "prompt": user_text, "stream": False} # sends the text as a prompt (TEMPORARY)
    llm_resp = requests.post(LLM_URL, json=payload, timeout=LLM_TIMEOUT)
    llm_resp.raise_for_status()
    llm_json = llm_resp.json() # gets raw json file of llm's output

    ai_text = llm_json.get("response") or llm_json.get("generated") or llm_json.get("text") or "" # tries combinations to extracting json from inpt
    story(ai_text, False)

    return jsonify({
        "input": user_text,
        "ai_text": ai_text,
        

    }), 200 # flag for "okay"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)