
# Node.js builder for LSIF generation
FROM node:current as builder

# install lsif-tsc as dependency for generate lsif file
RUN npm install -g lsif-tsc

# Copy only tools package.json first (better for caching)
COPY tools/package*.json ./tools/

# Install deps inside tools
RUN cd tools && npm install


# syntax=docker/dockerfile:1.4
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Context is backend/, so requirements.txt is at root of context
COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Example:
RUN python -c 'from sentence_transformers import SentenceTransformer; SentenceTransformer("all-MiniLM-L6-v2");'
# TODO: Verify it
RUN python -c 'from transformers import RobertaTokenizer, RobertaModel, RobertaConfig; RobertaTokenizer.from_pretrained("microsoft/unixcoder-base") ; RobertaModel.from_pretrained("microsoft/unixcoder-base") ; RobertaConfig.from_pretrained("microsoft/unixcoder-base");'
  

# Copy the backend folder content only
COPY . /app/backend

# Ensure Python sees repo root equivalent
ENV PYTHONPATH=/app
EXPOSE 8081

CMD ["python", "-m", "uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8081"]


