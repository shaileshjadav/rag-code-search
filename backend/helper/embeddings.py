import os
from ollama import Client
from backend.config import ENCODER_NAME

MODEL = ENCODER_NAME  # local llm

client = Client(
  host='http://127.0.0.1:11434',
  headers={'x-some-header': 'some-value'}
)

def get_embedding(text: str, docstring: str):
    resp = client.embeddings(model=MODEL, prompt=text)
    return resp.embedding
