from script.embedding_module import Embedding
from script.chromadb_module import ChromaDBClient
from script.rag_module import RAG
from dotenv import load_dotenv
import os

load_dotenv()


PATH_DATA = "./crawl/data_vnu_wikipedia.txt"
MODEL_EMBEDDING = os.getenv("MODEL_EMBEDDING")
CHUNK_SIZE = 256

if __name__ == "__main__":
    with open(PATH_DATA, "r", encoding="utf-8") as f:
        texts = f.read()

    embedding_handler = Embedding(model_name=MODEL_EMBEDDING, chunk_size=CHUNK_SIZE)
    chunks = embedding_handler.chunk_text(texts)

    db = ChromaDBClient(model_name=MODEL_EMBEDDING, chunk_size=CHUNK_SIZE)

    texts_with_embeddings = [db.insert_with_text(chunk) for chunk in chunks]


    # Truy vấn thử voe
    # result = db.query("Đại học Quốc gia Hà Nội")
    # print('result', result)

    rag = RAG(model_name=MODEL_EMBEDDING, chunk_size=CHUNK_SIZE)

    result = rag.rag_query("Đại học Quốc gia Hà Nội")
    print('result', result)
