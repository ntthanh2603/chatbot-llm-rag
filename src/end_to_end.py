# from rag_module import RAG
from llm_service import LLMService
from dotenv import load_dotenv

load_dotenv()


def main():
    load_dotenv()

    model_variable = {
        "name": "qwen-2.5",
        "link": "Qwen/Qwen2.5-3B-Instruct"
    }
    model_embedding_variable = {
        "name": "phobert",
        "link": "vinai/phobert-base"
    }

    llm_service = LLMService(
        # You can specify a different model from the list if needed
        model_name=model_variable["link"],
        use_rag=True,
        model_embedding=model_embedding_variable["link"]
    )

    prompt = input()

    answer = llm_service.generate_text(prompt)

    print(answer)


if __name__ == "__main__":
    main()
