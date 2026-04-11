import os
import glob

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

EMBED_MODEL  = "all-MiniLM-L6-v2"
CLAUDE_MODEL = "claude-sonnet-4-20250514"

CHROMA_PATH     = "./chroma_db"
COLLECTION_NAME = "juniper_switches"

CHUNK_SIZE    = 600
CHUNK_OVERLAP = 100

TOP_K = 10

DATASHEET_PATHS = glob.glob("./datasheets/**/*.pdf")