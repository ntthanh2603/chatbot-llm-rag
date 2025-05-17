# from rag_module import RAG
from llm_service import LLMService
# from pinecone_module import PineconeDBClient
from dotenv import load_dotenv
import os
import sys
import json

load_dotenv()


MODEL_EMBEDDING = os.getenv("MODEL_EMBEDDING")
CHUNK_SIZE = 256
PATH_TEST_DATA = "./data/demo_wiki_questions.json"

model_list = [
    { 
        "name": "meta-llama-3.2",
        "link": "meta-llama/Llama-3.2-3B-Instruct"
    },
    {
        "name": "qwen-2.5",
        "link": "Qwen/Qwen2.5-3B-Instruct"
    },
    {
        "name": "gemma-3.4",
        "link": "google/gemma-3-4b-it"
    }
]


def main(model_index=0):
    load_dotenv()

    model_variable = model_list[model_index]

    llm_service = LLMService(
        # You can specify a different model from the list if needed
        model_name=model_variable["link"],
        use_rag=True,
        model_embedding=MODEL_EMBEDDING
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

    # Save to new JSON file
    json_save_path = "data/{}-result.json".format(model_variable["name"])
    with open(json_save_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    os.makedirs("stdout", exist_ok=True)
    sys.stdout = open("stdout/main_out.txt", "w")
    sys.stderr = open("stdout/main_err.txt", "w")

    main(model_index=1)

    sys.stdout.close()
    sys.stderr.close()
