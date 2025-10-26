import requests as rq
import logging
from flask import Flask, request, jsonify
from Story import story

app = Flask(__name__)

# create logger to make errors visible in Flask console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("paladins_backend")

SYSTEM_PROMPT = """You're a medieval text adventure engine.
Write short vivid scenes under 50 words using the user input: {user_input}
British English spelling
"""

TEMPLATE = """In <50 words respond medievally (don't break character) to '{user_input}'"""

## GET REQUEST (FROM WEBSITE)
LLM_URL = "http://localhost:11434/api/generate" # ollama
LLM_TIMEOUT = 60

initial_prompt = True

def last_n_nonempty_lines(text, n):
    if not text:
        return ""
    lines = [ln.rstrip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        # fallback: return the last ~30 words as a short single-line preview
        words = text.split()
        return " ".join(words[-30:]) if words else ""
    return "\n".join(lines[-n:])

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

    try:
        llm_resp = rq.post(LLM_URL, json=payload, timeout=LLM_TIMEOUT)
    except rq.exceptions.ConnectTimeout as e:
        logger.exception("LLM connection timed out")
        return jsonify({"error":"LLM connection timed out", "detail": str(e)}), 504
    except rq.exceptions.ConnectionError as e:
        logger.exception("LLM connection error")
        return jsonify({"error":"LLM connection error", "detail": str(e)}), 502
    except rq.exceptions.RequestException as e:
        logger.exception("LLM request failed")
        return jsonify({"error":"LLM request failed", "detail": str(e)}), 502
    
    try:
        llm_resp.raise_for_status()
    except rq.exceptions.HTTPError as e:
        raw = llm_resp.text[:400] if hasattr(llm_resp, "text") else "<no body>" # raw llm file
        logger.error("LLM returned HTTP %s: %s", llm_resp.status_code, raw)
        return jsonify({
            "error": "LLM HTTP error",
            "status_code": llm_resp.status_code,
            "llm_raw_snippet": raw
        }), 502
    
    try:
        llm_json = llm_resp.json() # gets raw json file of llm's output
    except ValueError:
        raw = llm_resp.text if hasattr(llm_resp, "text") else ""
        logger.error("LLM returned non-JSON response: %s", raw[:400])
        return jsonify({"error": "LLM returned non-JSON", "raw_snippet": raw[:400]}), 502

    full_ai_text = llm_json.get("response") or llm_json.get("generated") or llm_json.get("text") or "" # tries combinations to extracting json from inpt

    ai_text = last_n_nonempty_lines(full_ai_text, 3)

    try:
        story(ai_text, False) # quarantining this code
    except Exception as e:
        logger.exception(f"YY's code is cooked because of %s", e)

    return jsonify({
        "input": user_text,
        "ai_text": ai_text,
        "full_ai_text": full_ai_text,
        "status": llm_resp.status_code
    }), 200 # flag for "okay"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
