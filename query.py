import anthropic
import chromadb
from sentence_transformers import SentenceTransformer
from config import (
    ANTHROPIC_API_KEY, CHROMA_PATH, COLLECTION_NAME,
    EMBED_MODEL, CLAUDE_MODEL, TOP_K
)

embedder      = SentenceTransformer(EMBED_MODEL)
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection    = chroma_client.get_or_create_collection(COLLECTION_NAME)
client        = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def query(question):
    # 1. Embed the question
    question_embedding = embedder.encode(question).tolist()

    # 2. Find the most relevant chunks
    results = collection.query(query_embeddings=[question_embedding], n_results=TOP_K)
    chunks  = results["documents"][0]
    sources = [m["source"] for m in results["metadatas"][0]]

    # Debugging 
    # print("\n--- Retrieved Chunks ---")
    # for i, chunk in enumerate(chunks):
        # print(f"\nChunk {i+1}:\n{chunk}")
        # print("-" * 50)

    # 3. Build the prompt
    context = "\n\n".join(chunks)
    prompt  = f"""You are a helpful assistant that answers questions about Juniper Networks switches.
Use only the information provided below to answer the question. If the answer isn't in the context, say so.

Context:
{context}

Question: {question}
"""

    # 4. Ask Claude
    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    answer = message.content[0].text

    return answer, sources

if __name__ == "__main__":
    q = input("Ask a question about Juniper switches: ")
    query(q)