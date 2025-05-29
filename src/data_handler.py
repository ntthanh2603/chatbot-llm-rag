from embedding_module import Embedding
from pinecone_module import PineconeDBClient
from dotenv import load_dotenv
import os
import sys

load_dotenv()


PATH_DATA = "./data/data_vnu_wikipedia.txt"
MODEL_EMBEDDING = os.getenv("MODEL_EMBEDDING")
CHUNK_SIZE = 256


def chunk_and_add_data(path_data, model_embedding, chunk_size):
    with open(path_data, "r", encoding="utf-8") as f:
        texts = f.read()

    # Chunk data in file .txt
    embedding_handler = Embedding(
        model_embedding=model_embedding,
        chunk_size=chunk_size
    )
    chunks = embedding_handler.chunk_text(texts)

    print(chunks)

    # Insert data to ChromaDB
    db = PineconeDBClient(
        model_embedding=model_embedding,
        chunk_size=chunk_size
    )

    try:
        db.index.delete(delete_all=True)  # 🧹 Wipe old data
    except Exception as e:
        print(e)
        print("All data has been wiped out before")

    # Sequentially insert chunks and wait for each to complete
    for i, chunk in enumerate(chunks):
        db.insert_with_text(chunk)
        print(f"Inserted chunk {i + 1}/{len(chunks)}")

    # print(texts_with_embeddings)


if __name__ == "__main__":
    os.makedirs("stdout", exist_ok=True)
    sys.stdout = open("stdout/data_handler_out.txt", "w")
    sys.stderr = open("stdout/data_handler_err.txt", "w")

    chunk_and_add_data(PATH_DATA, MODEL_EMBEDDING, CHUNK_SIZE)

    sys.stdout.close()
    sys.stderr.close()
