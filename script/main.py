from script.embedding_module import Embedding
from script.chromadb_module import ChromaDBClient
from script.rag_module import RAG
from script.llm_service import LLMService
from dotenv import load_dotenv
import os
import argparse

load_dotenv()


PATH_DATA = "./crawl/data_vnu_wikipedia.txt"
MODEL_EMBEDDING = os.getenv("MODEL_EMBEDDING")
CHUNK_SIZE = 512



def main():
    load_dotenv()

    # with open(PATH_DATA, "r", encoding="utf-8") as f:
    #     texts = f.read()

    # # Chunk data in file .txt
    # embedding_handler = Embedding(model_embedding=MODEL_EMBEDDING, chunk_size=CHUNK_SIZE)
    # chunks = embedding_handler.split_file_by_chunk_size(texts)

    # # Insert data to ChromaDB
    # db = ChromaDBClient(model_embedding=MODEL_EMBEDDING, chunk_size=CHUNK_SIZE)
    # texts_with_embeddings = [db.insert_with_text(chunk) for chunk in chunks]


    # Query to ChromaDB
    # result = db.query("Đại học Quốc gia Hà Nội")
    # print('result', result)

    # Query in RAG
    # rag = RAG(model_embedding=MODEL_EMBEDDING, chunk_size=CHUNK_SIZE)
    # result = rag.rag_query("Đại học Quốc gia Hà Nội")
    # print('result', result)

    # llm_service = LLMService(
    #     # You can specify a different model from the list if needed
    #     # model_name='meta-llama/Llama-3.1-8B-Instruct',
    #     use_rag=True,
    #     model_embedding=MODEL_EMBEDDING
    # )

    # prompt1 = "Đại học Quốc gia Hà Nội có bao nhiêu cơ sở?"
    # print(f"\n--- Query 1: {prompt1} ---")
    # output1 = llm_service.generate_text(prompt1)
    # print("output1", output1)
    
    # # Example 2: Vietnamese query with RAG
    # prompt2 = "Đại học Quốc Gia Hà Nội có những trường thpt nào?"
    # print(f"\n--- Query 2: {prompt2} ---")
    # output2 = llm_service.generate_text(prompt2)
    # print("output2", output2)
    
    # # Example 3: Direct query without RAG
    # prompt3 = "Ai là Đại tướng đầu tiên của Quân đội Nhân dân Việt Nam?"
    # print(f"\n--- Query 3 (without RAG): {prompt3} ---")
    # output3 = llm_service.generate_text(prompt3, use_rag=False)
    # print("output3", output3)

    # Tạo parser cho đối số dòng lệnh
    parser = argparse.ArgumentParser(description='Chatbot LLM-RAG')
    
    # Thêm các tùy chọn dòng lệnh
    parser.add_argument('--model', type=str, default=None,
                        help='Tên mô hình để sử dụng (mặc định: TinyLlama-1.1B-Chat-v1.0)')
    parser.add_argument('--no-rag', action='store_false', dest='use_rag',
                        help='Tắt hệ thống RAG (mặc định: Bật)')
    parser.add_argument('--gpu', action='store_true', dest='use_gpu',
                        help='Sử dụng GPU nếu có (mặc định: Chỉ sử dụng CPU)')
    parser.add_argument('--4bit', action='store_true', dest='use_4bit',
                        help='Sử dụng lượng tử hóa 4-bit nếu trên GPU (mặc định: Tắt)')
    
    # Parse đối số
    args = parser.parse_args()
    
    # Danh sách các mô hình có sẵn để hiển thị
    available_models = [
        'mistralai/Mistral-7B-Instruct-v0.3',
        'Qwen/Qwen2.5-7B-Instruct',
        'meta-llama/Llama-3.1-8B-Instruct',
        'google/gemma-3-4b-it',
        'TinyLlama/TinyLlama-1.1B-Chat-v1.0',
    ]
    
    # Hiển thị các mô hình có sẵn
    print("Các mô hình có sẵn:")
    for i, model in enumerate(available_models):
        print(f"{i+1}. {model}")
    
    # Khởi tạo dịch vụ LLM
    print("\nKhởi tạo LLM service...")
    llm_service = LLMService(
        use_rag=args.use_rag,
        model_name=args.model,
        use_gpu=args.use_gpu,
        use_4bit=args.use_4bit
    )
    
    # Chế độ chat đơn giản
    print("\n===== Chế độ Chat =====")
    print("Nhập 'exit' để thoát")
    
    while True:
        user_input = input("\nBạn: ")
        if user_input.lower() == 'exit':
            break
        
        print("\nĐang xử lý...")
        response = llm_service.generate_text(user_input)
        print(f"\nBot: {response}")


if __name__ == "__main__":
    # Load data
    # db = ChromaDBClient()
    # db.upload_data()

    main()
