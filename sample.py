
from openai import OpenAI
import os
client = OpenAI(
    api_key="api_key_value",
    base_url="https://api.groq.com/openai/v1",
)

response = client.responses.create(
    input="Who is the pm of india?",
    model="openai/gpt-oss-20b",
    temperature=0.1,
    max_output_tokens=1000,
)
print(response.output_text)
