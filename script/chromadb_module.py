import chromadb
from chromadb.config import Settings
from script.embedding_module import Embedding
import uuid



class ChromaDBClient:
    def __init__(self,model_embedding="bkai-foundation-models/vietnamese-bi-encoder", chunk_size=512, host="localhost", port=8000, collection_name="vnu_chunks"):
        self.client = chromadb.HttpClient(
            host=host,
            port=port,
            settings=Settings(allow_reset=True)
        )
        self.chunk_size = chunk_size
        self.model_embedding = model_embedding
        self.path_data = "./crawl/data_vnu_wikipedia.txt"
        self.embedding = Embedding(model_embedding=model_embedding, chunk_size=chunk_size)
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
    
    def upload_data(self):
        with open(self.path_data, "r", encoding="utf-8") as f:
            texts = f.read()

        # Chunk data in file .txt
        embedding_handler = Embedding(model_embedding=self.model_embedding, chunk_size=self.chunk_size)
        chunks = embedding_handler.split_file_by_chunk_size(texts)

        # Insert data to ChromaDB
        db = ChromaDBClient(model_embedding=self.model_embedding, chunk_size=self.chunk_size)
        [db.insert_with_text(chunk) for chunk in chunks]

        print("Save data to database successfully")
        return