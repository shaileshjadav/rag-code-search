import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from starlette.staticfiles import StaticFiles

from backend.config import ROOT_DIR
from backend.helper.get_file import FileGet
from backend.search.searcher import CombinedSearcher


app = FastAPI()

searcher = CombinedSearcher()
get_file = FileGet()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],            # List of allowed origins
    allow_credentials=True,           # Allow cookies/auth headers
    allow_methods=["*"],              # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],              # Allow all headers
)

@app.get("/api/search")
async def search(query: str):
    return {
        "result": searcher.search(query, limit=5)
    }

@app.get("/api/file")
async def file(path: str):
    return {
        "result": get_file.get(path)
    }


app.mount("/", StaticFiles(directory=os.path.join(ROOT_DIR, 'frontend', 'dist'), html=True))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081)
