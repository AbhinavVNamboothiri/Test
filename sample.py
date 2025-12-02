from openai import OpenAI
import os

# Replace hard-coded API key with environment variables and add chat loop
api_key = os.environ.get("OPENAI_API_KEY")
base_url = os.environ.get("OPENAI_BASE_URL", "https://api.groq.com/openai/v1")
if not api_key:
    raise RuntimeError("Please set the OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=api_key, base_url=base_url)

# initial system instruction and conversation history
conversation = [
    {"role": "system", "content": "You are a helpful assistant. Keep answers concise."}
]

def get_assistant_reply(conv):
    resp = client.responses.create(
        model="openai/gpt-oss-20b",
        input=conv,
        temperature=0.1,
        max_output_tokens=1000,
    )
    # preferred accessor
    if hasattr(resp, "output_text") and resp.output_text:
        return resp.output_text
    # fallback: try to extract from resp.output
    try:
        out = resp.output
        if isinstance(out, list) and len(out) > 0:
            first = out[0]
            if isinstance(first, dict):
                # vary based on response shape
                return first.get("content") or first.get("text") or str(first)
        return str(out)
    except Exception:
        return ""

def main():
    print("Chatbot ready. Type your message and press Enter. Type 'exit' or 'quit' to stop.")
    try:
        while True:
            user_input = input("User: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit"):
                print("Exiting chatbot.")
                break
            conversation.append({"role": "user", "content": user_input})
            reply = get_assistant_reply(conversation)
            reply = (reply or "").strip()
            print("Assistant:", reply)
            conversation.append({"role": "assistant", "content": reply})
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")

if __name__ == "__main__":
    main()
