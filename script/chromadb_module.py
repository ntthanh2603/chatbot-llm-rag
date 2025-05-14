import chromadb
from chromadb.config import Settings
from script.embedding_module import Embedding
import uuid



class ChromaDBClient:
    def __init__(self,model_name="bkai-foundation-models/vietnamese-bi-encoder", chunk_size=256, host="localhost", port=8000, collection_name="vnu_chunks"):
        self.client = chromadb.HttpClient(
            host=host,
            port=port,
            settings=Settings(allow_reset=True)
        )
        self.embedding = Embedding(model_name=model_name, chunk_size=chunk_size)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def insert_with_text(self, text: str):
        try:
            embedding = self.embedding.embedding(text)
            self.collection.add(
                documents=[text],
                ids=[str(uuid.uuid4())],
                embeddings=[embedding],
                metadatas=[{"source": "script"}]
            )
        except Exception as e:
            print(e)

    def query(self, query_text: str, top_k: int = 3):
        try:
            embedding = self.embedding.embedding(query_text)
            result = self.collection.query(
                query_embeddings=[embedding],
                n_results=top_k,
                include=["documents", "distances", "metadatas"]
            )
            return result
        except Exception as e:
            print("Query error:", e)
            return None