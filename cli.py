import os
import json
import argparse
import requests
from google import genai
from google.genai import types

LSIF_FILE = "lsif.json"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/embeddings"

def embed_text(text):
    if not OPENROUTER_API_KEY:
        print("❌ Missing OPENROUTER_API_KEY env variable")
        return None

    client = genai.Client(api_key=OPENROUTER_API_KEY)

    try:
        response = client.models.embed_content(
            model='text-embedding-004',
            contents=text,
        )
        return response.embeddings[0].values
    except Exception as e:
        print("❌ Embedding request failed:", e)
        return None


def chunk_code(content, chunk_size=300, overlap=50):
    """
    Splits code into overlapping chunks for better semantic search.
    """
    chunks = []
    start = 0
    while start < len(content):
        end = min(len(content), start + chunk_size)
        chunks.append(content[start:end])
        start += chunk_size - overlap  # slide window
    return chunks

def index_repo(repo_path):
    repo_path = os.path.abspath(repo_path)  # ensure absolute path
    print(f"📂 Indexing repo at {repo_path}")

    symbols = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith((".py", ".js", ".ts", ".java", ".go", ".php", ".cpp", ".c")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    # 🔹 break file into chunks
                    chunks = chunk_code(content)

                    for i, chunk in enumerate(chunks):
                        embedding = embed_text(chunk)  # your Gemini embedding call
                        symbols.append({
                            "uri": file_path,
                            "symbol": f"{file}::chunk{i}",
                            "content": chunk[:200],  # preview just snippet
                            "embedding": embedding
                        })
                    print(f"✅ Indexed {file_path} into {len(chunks)} chunks")

                except Exception as e:
                    print(f"⚠️ Could not read {file_path}: {e}")

    with open(LSIF_FILE, "w") as f:
        json.dump({"symbols": symbols}, f, indent=2)

    print(f"🎉 Indexing complete! Stored {len(symbols)} code snippets in {LSIF_FILE}")

def search_repo(query):
    if not os.path.exists(LSIF_FILE):
        print("❌ No LSIF index found. Run `index` first.")
        return

    with open(LSIF_FILE, "r") as f:
        lsif = json.load(f)

    query_embedding = embed_text(query)
    if not query_embedding:
        return

    # simple cosine similarity
    def cosine(a, b):
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        return dot / (norm_a * norm_b + 1e-8)

    results = []
    for sym in lsif["symbols"]:
        if sym.get("embedding"):
            score = cosine(query_embedding, sym["embedding"])
            results.append((score, sym))

    results.sort(key=lambda x: x[0], reverse=True)

    print("🔎 Search results:")
    for score, sym in results[:5]:
        print(f"[{score:.3f}] {sym['uri']} → {sym['symbol']} (preview: {sym['content'][:50]}...)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mini LSIF + Embedding Search CLI")
    subparsers = parser.add_subparsers(dest="command")

    index_parser = subparsers.add_parser("index", help="Index a repo")
    index_parser.add_argument("--repo", required=True, help="Path to repo")

    search_parser = subparsers.add_parser("search", help="Search repo")
    search_parser.add_argument("--query", required=True, help="Search query")

    args = parser.parse_args()

    if args.command == "index":
        index_repo(args.repo)
    elif args.command == "search":
        search_repo(args.query)
