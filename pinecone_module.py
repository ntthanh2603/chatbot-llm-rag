import pinecone
import os
import uuid
from embedding_module import Embedding
from dotenv import load_dotenv

load_dotenv()


class PineconeDBClient:
    def __init__(
        self, model_embedding, chunk_size=256,
        index_name="vnu_chunks"
    ):
        self.embedding = Embedding(
            model_embedding=model_embedding,
            chunk_size=chunk_size
        )

        # Init Pinecone
        pinecone.init(
            api_key=os.getenv("PINECONE_API_KEY"),
            environment=os.getenv("PINECONE_ENV")  # e.g., 'gcp-starter'
        )

        self.index_name = index_name
        if self.index_name not in pinecone.list_indexes():
            pinecone.create_index(
                name=self.index_name,
                dimension=self.embedding.embedding_dim
            )

        self.index = pinecone.Index(self.index_name)

    def insert_with_text(self, text: str):
        try:
            vector = self.embedding.embedding(text)
            item_id = str(uuid.uuid4())
            self.index.upsert([
                (item_id, vector, {"text": text, "source": "script"})
            ])
        except Exception as e:
            print("Insert error:", e)

    def query(self, query_text: str, top_k: int = 3):
        try:
            vector = self.embedding.embedding(query_text)
            result = self.index.query(
                vector=vector,
                top_k=top_k,
                include_metadata=True
            )
            return {
                "documents": [match["metadata"]["text"] for match in result["matches"]],
                "distances": [match["score"] for match in result["matches"]],
                "metadatas": [match["metadata"] for match in result["matches"]],
            }
        except Exception as e:
            print("Query error:", e)
            return None
