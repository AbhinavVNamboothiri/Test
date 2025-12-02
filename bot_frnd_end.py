from flask import Flask, request, jsonify
from flask_cors import CORS      # <-- ADD THIS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)  # <-- ENABLE CORS FOR ALL ROUTES

# Load env keys
api_key = os.environ.get("OPENAI_API_KEY")
base_url = os.environ.get("OPENAI_BASE_URL", "https://api.groq.com/openai/v1")

if not api_key:
    raise RuntimeError("Please set the OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=api_key, base_url=base_url)


def get_assistant_reply(conv):
    resp = client.responses.create(
        model="openai/gpt-oss-20b",
        input=conv,
        temperature=0.1,
        max_output_tokens=1000,
    )

    if hasattr(resp, "output_text") and resp.output_text:
        return resp.output_text

    try:
        out = resp.output
        if isinstance(out, list) and len(out) > 0:
            first = out[0]
            if isinstance(first, dict):
                return first.get("content") or first.get("text") or str(first)
        return str(out)
    except Exception:
        return ""


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "conversation" not in data:
        return jsonify({"error": "Missing 'conversation' field"}), 400

    conversation = data["conversation"]
    reply = get_assistant_reply(conversation)
    reply = (reply or "").strip()

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
