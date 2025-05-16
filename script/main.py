import argparse
import asyncio
from script.llm_service import LLMService
from script.chromadb_module import ChromaDBClient

async def main():
    # Load data to database 
    db = ChromaDBClient()
    db.upload_data()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--use-rag", action="store_true", help="Use RAG to enhance responses")
    parser.add_argument("--llm-api", action="store_true", help="Use LLM API instead of local model")
    parser.add_argument("--model", type=str, help="Specify a model to use")
    parser.add_argument("--gpu", action="store_true", help="Use GPU for model inference")
    parser.add_argument("--4bit", dest="use_4bit", action="store_true", help="Use 4-bit quantization")
    args = parser.parse_args()

    # Initialize the LLM service
    print("Init LLM service...")
    llm_service = LLMService(
        use_rag=args.use_rag, 
        use_llm_api=args.llm_api,
        model_name=args.model,
        use_gpu=args.gpu,
        use_4bit=args.use_4bit
    )

    print("\n===== Chat base =====")
    print("Enter 'exit' to exit")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break
            
        print("\nProcessing...")
        # Use await here to properly handle the async function
        response = await llm_service.generate_text(user_input)
        print(f"\nBot: {response}")

if __name__ == "__main__":
    asyncio.run(main())