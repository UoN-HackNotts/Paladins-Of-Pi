import requests as rq
from flask import Flask, request, jsonify
from Story import story

app = Flask(__name__)

SYSTEM_PROMPT = """You're a medieval text adventure engine.
Write short vivid scenes under 50 words using the user input:
{user_input}
British English spelling
"""

TEMPLATE = """In <50 words respond to '{user_input}'"""

## GET REQUEST (FROM WEBSITE)
LLM_URL = "http://localhost:11434/api/generate" # ollama
LLM_TIMEOUT = 60

initial_prompt = True

@app.route("/generate", methods=["GET"])
def generate(): # handler for HTTP GET/generate
    """
    Takes in the input from the website using flask request (NOT requests)
    """
    global initial_prompt
    user_text = (request.args.get("q") or "").strip() # .strip() removes redundant chars, "" is a fallback if "q" not found
    try:
        story(user_text, True) # quarantining this code
    except Exception as e:
        print(f"YY's code is cooked because of {e}")
    """
    LLM output
    """
    payload = {"model": "phi3",
               "prompt": SYSTEM_PROMPT.format(user_input=user_text) if initial_prompt else TEMPLATE.format(user_input=user_text),
               "stream": False} # sends the text as a prompt (TEMPORARY)

    if initial_prompt: # disable flag after first use
        initial_prompt = False

    llm_resp = rq.post(LLM_URL, json=payload, timeout=LLM_TIMEOUT)
    llm_resp.raise_for_status()
    llm_json = llm_resp.json() # gets raw json file of llm's output

    ai_text = llm_json.get("response") or llm_json.get("generated") or llm_json.get("text") or "" # tries combinations to extracting json from inpt
    try:
        story(ai_text, False) # quarantining this code
    except Exception as e:
        print(f"YY's code is cooked because of {e}")

    return jsonify({
        "input": user_text,
        "ai_text": ai_text,
        

    }), 200 # flag for "okay"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
