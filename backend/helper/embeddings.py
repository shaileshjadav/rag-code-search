import os
from ollama import Client

MODEL = "nomic-embed-text"  # local llm

client = Client(
  host='http://127.0.0.1:11434',
  headers={'x-some-header': 'some-value'}
)

def get_embedding(text: str, docstring: str):
    resp = client.embed(model=MODEL, input=text)
    return resp['embeddings'][0]
