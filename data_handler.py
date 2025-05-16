from embedding_module import Embedding
from pinecone_module import PineconeDBClient


def chunk_and_add_data(path_data, model_embedding, chunk_size):
    with open(path_data, "r", encoding="utf-8") as f:
        texts = f.read()

    # Chunk data in file .txt
    embedding_handler = Embedding(
        model_embedding=model_embedding,
        chunk_size=chunk_size
    )
    chunks = embedding_handler.chunk_text(texts)

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
