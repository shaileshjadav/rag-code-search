import os
from ollama import Client
from backend.config import ENCODER_NAME, OPENAI_API_KEY
from openai import OpenAI


MODEL = ENCODER_NAME  # local llm
print(OPENAI_API_KEY)
client = OpenAI(
  # host='http://127.0.0.1:11434',
  # headers={'x-some-header': 'some-value'}
  # base_url = 
  # api_key= OPENAI_API_KEY
)

def get_embedding(text: str, docstring: str):
    resp = client.embeddings.create(model=MODEL, input=text)
    return resp.data[0].embedding
