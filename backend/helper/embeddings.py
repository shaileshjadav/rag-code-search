import os
from ollama import Client
from backend.config import ENCODER_NAME, ENCODER_SIZE
from openai import OpenAI
import numpy as np


def normalize_l2(x):
    x = np.array(x)
    if x.ndim == 1:
        norm = np.linalg.norm(x)
        if norm == 0:
            return x
        return x / norm
    else:
        norm = np.linalg.norm(x, 2, axis=1, keepdims=True)
        return np.where(norm == 0, x, x / norm)


MODEL = ENCODER_NAME  # local llm

client = OpenAI(
  # host='http://127.0.0.1:11434',
  # headers={'x-some-header': 'some-value'}
  base_url = "http://localhost:11434/v1",
  api_key='ollama', # required, but unused
  # api_key= GEMINI_API_KEY,
  # base_url='https://generativelanguage.googleapis.com/v1beta/openai/',
)

def get_embedding(text: str, docstring: str):
    resp = client.embeddings.create(model=MODEL, input=text)
    # return resp.data[0].embedding
    return normalize_l2(resp.data[0].embedding[:ENCODER_SIZE])
