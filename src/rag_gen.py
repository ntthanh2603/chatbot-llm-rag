from rag_module import RAG
# from llm_service import LLMService
# from pinecone_module import PineconeDBClient
from model_env import (
    CHUNK_SIZE, PATH_TEST_DATA,
    model_embedding_list
)
from dotenv import load_dotenv
import os
import sys
import json

load_dotenv()


def main(model_embedding_index=0):
    load_dotenv()

    model_embedding_variable = model_embedding_list[model_embedding_index]

    # Query in RAG
    rag = RAG(
        model_embedding=model_embedding_variable["link"],
        chunk_size=CHUNK_SIZE
    )
    result = rag.rag_query("Đại học Quốc gia Hà Nội có bao nhiêu cơ sở?")
    print('RAG query result', result)

    # Load input JSON
    with open(PATH_TEST_DATA, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Process each question
    for i, item in enumerate(data):
        prompt = item["question"]
        print(f"\n--- Query {i + 1}: {prompt} ---")
        rag_prompt = rag.rag_query(prompt)
        print(f"rag_answer {i + 1}:", rag_prompt)
        item["rag_prompt"] = rag_prompt

    # Save to new JSON file
    os.makedirs(
        "./data/{}".format(model_embedding_variable["name"]),
        exist_ok=True
    )
    json_save_path = "data/{}/rag-prompt-result.json".format(
        model_embedding_variable["name"]
    )
    with open(json_save_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    os.makedirs("stdout", exist_ok=True)
    sys.stdout = open("stdout/rag_gen_out.txt", "w")
    sys.stderr = open("stdout/rag_gen_err.txt", "w")

    for i in range(1, len(model_embedding_list)):
        main(model_embedding_index=i)

    sys.stdout.close()
    sys.stderr.close()
