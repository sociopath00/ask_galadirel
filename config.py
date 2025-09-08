import os
from dotenv import load_dotenv

load_dotenv(".env")

# Secrets
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

QDRANT_URL = os.environ["QDRANT_URL"]
QDRANT_API_KEY = os.environ["QDRANT_API_KEY"]

# Directories
DATA_DIR = "./data/*.pdf"

# Qdrant Params
COLLECTION_NAME = "middle_earth"

# Hyperparameters
CHUNK_SIZE = 800
CHUNK_OVERLAP = 200

