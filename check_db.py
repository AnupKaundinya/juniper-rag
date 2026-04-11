import chromadb
from config import CHROMA_PATH, COLLECTION_NAME

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection    = chroma_client.get_or_create_collection(COLLECTION_NAME)

results = collection.get(include=["metadatas"])
sources = sorted(set(m["source"] for m in results["metadatas"]))

print(f"Total chunks: {collection.count()}\n")
print("Ingested sources:")
for s in sources:
    print(f"  - {s}")