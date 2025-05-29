# from rag_module import RAG
from llm_service import LLMService
from model_env import (
    PATH_TEST_DATA,
    model_list, model_embedding_list
)
# from pinecone_module import PineconeDBClient
from dotenv import load_dotenv
import os
import sys
import json

load_dotenv()


def main(model_index=0, model_embedding_index=0):
    load_dotenv()

    model_variable = model_list[model_index]
    model_embedding_variable = model_embedding_list[model_embedding_index]

    llm_service = LLMService(
        # You can specify a different model from the list if needed
        model_name=model_variable["link"],
        use_rag=True,
        model_embedding=model_embedding_variable["link"]
    )

    # Load input JSON
    with open(PATH_TEST_DATA, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Process each question
    for i, item in enumerate(data):
        prompt = item["question"]
        print(f"\n--- Query {i + 1}: {prompt} ---")
        answer = llm_service.generate_text(prompt, max_length=128)
        print(f"rag_answer {i + 1}:", answer["rag_answer"])
        item["rag_prompt"] = answer["rag_prompt"]
        item["rag_answer"] = answer["rag_answer"]
        item["normal_answer"] = answer["normal_answer"]

    # Save to new JSON file
    os.makedirs(
        "./data/{}".format(model_embedding_variable["name"]),
        exist_ok=True
    )
    json_save_path = "data/{}/{}-result.json".format(
        model_embedding_variable["name"], model_variable["name"]
    )
    with open(json_save_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    os.makedirs("stdout", exist_ok=True)
    sys.stdout = open("stdout/main_out.txt", "w")
    sys.stderr = open("stdout/main_err.txt", "w")

    for i in range(1, len(model_list)-1):
        main(model_index=i, model_embedding_index=0)

    sys.stdout.close()
    sys.stderr.close()
