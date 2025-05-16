from rag_module import RAG
from llm_service import LLMService
from pinecone_module import PineconeDBClient
from dotenv import load_dotenv
# from data_handler import chunk_and_add_data
import os
import sys

load_dotenv()


PATH_DATA = "./data/data_vnu_wikipedia.txt"
MODEL_EMBEDDING = os.getenv("MODEL_EMBEDDING")
CHUNK_SIZE = 256


def main():
    load_dotenv()

    # chunk_and_add_data(PATH_DATA, MODEL_EMBEDDING, CHUNK_SIZE)

    db = PineconeDBClient(
        model_embedding=MODEL_EMBEDDING,
        chunk_size=CHUNK_SIZE
    )

    # Query to ChromaDB
    result = db.query("Đại học Quốc gia Hà Nội")
    print('DB query result:\n', result)

    # Query in RAG
    rag = RAG(model_embedding=MODEL_EMBEDDING, chunk_size=CHUNK_SIZE)
    result = rag.rag_query("Đại học Quốc gia Hà Nội")
    print('RAG query result', result)

    return

    llm_service = LLMService(
        # You can specify a different model from the list if needed
        model_name='meta-llama/Llama-3.1-8B-Instruct',
        use_rag=True,
        model_embedding=MODEL_EMBEDDING
    )

    prompt1 = "Đại học Quốc gia Hà Nội có bao nhiêu cơ sở?"
    print(f"\n--- Query 1: {prompt1} ---")
    output1 = llm_service.generate_text(prompt1)
    print("output1", output1)

    # Example 2: Vietnamese query with RAG
    prompt2 = "Đại học Quốc Gia Hà Nội có những trường thpt nào?"
    print(f"\n--- Query 2: {prompt2} ---")
    output2 = llm_service.generate_text(prompt2)
    print("output2", output2)

    # Example 3: Direct query without RAG
    prompt3 = "Ai là Đại tướng đầu tiên của Quân đội Nhân dân Việt Nam?"
    print(f"\n--- Query 3 (without RAG): {prompt3} ---")
    output3 = llm_service.generate_text(prompt3, use_rag=False)
    print("output3", output3)


if __name__ == "__main__":
    sys.stdout = open("out.txt", "w")
    sys.stderr = open("err.txt", "w")

    main()

    sys.stdout.close()
    sys.stderr.close()
