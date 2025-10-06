import os

from dotenv import load_dotenv

load_dotenv()

CODE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CODE_DIR)
DATA_DIR = os.path.join(CODE_DIR, "data")

QDRANT_URL = os.environ.get("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY",'test')

# QDRANT_FILE_COLLECTION_NAME="code-files"

# ENCODER_NAME = "deepseek-r1:1.5b"
# ENCODER_SIZE = 1536

ENCODER_NAME = "all-minilm:l6-v2"
# ENCODER_NAME = "qwen3:0.6b"
# ENCODER_NAME = "gemini-embedding-001"

ENCODER_SIZE = 384

# testing folder path for specific folder
TEST_FOLDER_PATH =  os.environ.get('TEST_REPO_PATH', './backend/twitter-fullstack')
SUPPORTED_LANGUAGES = [ '.js', '.ts', '.jsx', '.tsx']

# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY" , None)
# GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", None)
# ENCODER_NAME = "text-embedding-3-small"