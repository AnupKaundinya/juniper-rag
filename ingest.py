import chromadb
import fitz
import uuid
from sentence_transformers import SentenceTransformer
from config import CHROMA_PATH, COLLECTION_NAME, EMBED_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, DATASHEET_PATHS

print("Loading embedding model...")
embedder      = SentenceTransformer(EMBED_MODEL)
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection    = chroma_client.get_or_create_collection(COLLECTION_NAME)

def extract_pdf(path):
    doc  = fitz.open(path)
    text = " ".join(page.get_text() for page in doc)
    doc.close()
    return text

def chunk_text(text):
    words  = text.split()
    chunks = []
    start  = 0
    while start < len(words):
        chunk = " ".join(words[start : start + CHUNK_SIZE])
        if len(chunk.strip()) > 60:
            chunks.append(chunk)
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks

def store(chunks, source):
    print(f"  Embedding {len(chunks)} chunks...")
    embeddings = embedder.encode(chunks, show_progress_bar=True).tolist()
    ids        = [str(uuid.uuid4()) for _ in chunks]
    metadatas  = [{"source": source, "chunk_index": i} for i in range(len(chunks))]
    collection.upsert(ids=ids, embeddings=embeddings, documents=chunks, metadatas=metadatas)
    print(f"  Stored {len(chunks)} chunks from {source}")

if __name__ == "__main__":
    if not DATASHEET_PATHS:
        print("No PDFs found in ./datasheets/")
    else:
        for path in DATASHEET_PATHS:
            print(f"\nProcessing: {path}")
            text   = extract_pdf(path)
            chunks = chunk_text(text)
            store(chunks, source=path)
        print(f"\nDone! Total chunks in DB: {collection.count()}")