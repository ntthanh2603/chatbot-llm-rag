from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model
embedding_model = SentenceTransformer("vinai/phobert-base")

# Sample document corpus
documents = [
    "Transformers are neural networks designed for sequence data.",
    "LLaMA is a language model developed by Meta AI.",
    "RAG stands for Retrieval-Augmented Generation.",
    "Sentence embeddings are useful for semantic similarity.",
    "Hugging Face provides many NLP models and tools."
]

# Encode the document corpus
doc_embeddings = embedding_model.encode(documents, convert_to_tensor=False)
dimension = doc_embeddings[0].shape[0]

# Build FAISS index
index = faiss.IndexFlatL2(dimension)
index.add(np.array(doc_embeddings))

def rag_retrieve_and_concat(query: str, top_k: int = 2) -> str:
    # Embed the query
    query_embedding = embedding_model.encode([query])

    # Search for top-k relevant documents
    distances, indices = index.search(query_embedding, top_k)
    retrieved_docs = [documents[i] for i in indices[0]]

    # Construct context + query string
    context = "\n".join(retrieved_docs)
    full_input = f"Context:\n{context}\n\nQuestion: {query}"

    return full_input


if __name__ == "__main__":
    prompt = "Tell a funny story!"
    output = rag_retrieve_and_concat(prompt)
    print(output)