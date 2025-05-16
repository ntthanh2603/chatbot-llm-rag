import os
import uuid
from dotenv import load_dotenv
from embedding_module import Embedding
from pinecone import Pinecone, ServerlessSpec

load_dotenv()


class PineconeDBClient:
    def __init__(
        self,
        model_embedding,
        chunk_size=256,
        index_name="vnu-chunks"
    ):
        self.embedding = Embedding(
            model_embedding=model_embedding,
            chunk_size=chunk_size
        )
        self.index_name = index_name
        self.embedding_dim = self.embedding.embedding_dim

        # Init Pinecone v3 client
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API"))

        # Create index if it doesn't exist
        if self.index_name not in [
            index.name for index in self.pc.list_indexes()
        ]:
            self.pc.create_index(
                name=self.index_name,
                dimension=self.embedding_dim,
                metric="cosine",  # or "dotproduct"
                spec=ServerlessSpec(
                    cloud="aws",  # or "gcp"
                    region=os.getenv("PINECONE_REGION", "us-east-1")
                )
            )

        self.index = self.pc.Index(self.index_name)

    def insert_with_text(self, text: str):
        try:
            vector = self.embedding.embedding(text)
            item_id = str(uuid.uuid4())
            self.index.upsert(vectors=[
                {
                    "id": item_id,
                    "values": vector,
                    "metadata": {
                        "text": text,
                        "source": "script"
                    }
                }
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
                "documents": [
                    match["metadata"]["text"] for match in result["matches"]
                ],
                "distances": [match["score"] for match in result["matches"]],
                "metadatas": [
                    match["metadata"] for match in result["matches"]
                ],
            }
        except Exception as e:
            print("Query error:", e)
            return None
