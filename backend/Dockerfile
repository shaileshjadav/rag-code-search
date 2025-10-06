FROM node:current as builder

# install lsif-tsc as dependency for generate lsif file
RUN npm install -g lsif-tsc

# Copy only tools package.json first (better for caching)
COPY tools/package*.json ./tools/

# Install deps inside tools
RUN cd tools && npm install

FROM python:3.10-slim

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY requirements.txt /code/

# Project initialization:
RUN pip install -r requirements.txt

# Install pre-trained models here
# Example:
RUN python -c 'from sentence_transformers import SentenceTransformer; SentenceTransformer("all-MiniLM-L6-v2");'
# TODO: Verify it
RUN python -c 'from transformers import RobertaTokenizer, RobertaModel, RobertaConfig; RobertaTokenizer.from_pretrained("microsoft/unixcoder-base") ; RobertaModel.from_pretrained("microsoft/unixcoder-base") ; RobertaConfig.from_pretrained("microsoft/unixcoder-base");'

# Creating folders, and files for a project:
COPY . /code

CMD uvicorn app:app --host 0.0.0.0 --port 8081