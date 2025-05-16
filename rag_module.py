from pinecone_module import PineconeDBClient


class RAG:
    def __init__(
        self,
        model_embedding="bkai-foundation-models/vietnamese-bi-encoder",
        chunk_size=256
    ):
        self.db = PineconeDBClient(
            model_embedding=model_embedding,
            chunk_size=chunk_size
        )

    def rag_query(self, query_text, top_k=3):
        results = self.db.query(query_text, top_k=top_k)

        if not results or 'documents' not in results:
            return "Không thể tìm thấy thông tin liên quan."

        retrieved_docs = results['documents'][0]

        print(f"retrieved_docs: {retrieved_docs}")

        # context = "\n\n".join(retrieved_docs)
        context = retrieved_docs[:256]

        print(f"retrieved_docs: {type(retrieved_docs)}")

        augmented_prompt = f"""
Dựa vào các thông tin bổ sung dưới đây, hãy trả lời câu hỏi thật ngắn gọn và chính xác.
### Thông tin: {context}
### Câu hỏi: {query_text}
### Câu trả lời: """

        print(f"augmented_prompt: {augmented_prompt}")

        return augmented_prompt
