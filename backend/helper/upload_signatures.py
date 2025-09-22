import json
from pathlib import Path

import tqdm
from qdrant_client import QdrantClient, models
from qdrant_client.models import Distance, VectorParams

from backend.config import DATA_DIR, QDRANT_URL, QDRANT_API_KEY, ENCODER_NAME, \
    ENCODER_SIZE
from backend.helper.textify import textify

from backend.helper.embeddings import get_embedding

file_name = Path(DATA_DIR) / "signatures.json"

# function to get collection name for upload_code 
def get_collection_name(repo_name):
    return repo_name+"_signatures"


def iter_batch(iterable, batch_size=64):
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def load_records():
    with open(file_name, "r") as fp:
        data = json.load(fp)
        for row in data:
            yield row


def encode(sentence_transformer_name=ENCODER_NAME):
    for batch in iter_batch(load_records()):
        texts = [textify(row) for row in batch]
        embeddings = [get_embedding(text, "") for text in texts]
        yield from embeddings


def upload_signatures(repo_name):
    # collection name is equals to repo_name for multiple projects supports
    collection_name = get_collection_name(repo_name)

    client = QdrantClient(
        QDRANT_URL,
        api_key=QDRANT_API_KEY,
        prefer_grpc=False,
    )

    print(f"Recreating the collection {collection_name}")
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=ENCODER_SIZE,
            distance=Distance.COSINE,
            on_disk=True,
        ),
        quantization_config=models.ScalarQuantization(
            scalar=models.ScalarQuantizationConfig(
                type=models.ScalarType.INT8,
                always_ram=True,
                quantile=0.99,
            )
        )
    )

    client.upload_collection(
        collection_name=collection_name,
        vectors=encode(),
        payload=tqdm.tqdm(load_records()),
    )


if __name__ == '__main__':
    upload_signatures()
