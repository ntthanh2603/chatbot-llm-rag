from pinecone_module import PineconeDBClient


class RAG:
    def __init__(
        self,
        model_embedding="bkai-foundation-models/vietnamese-bi-encoder",
        chunk_size=256
    ):
        self.chroma_db = PineconeDBClient(
            model_embedding=model_embedding,
            chunk_size=chunk_size
        )

    def rag_query(self, query_text, top_k=3):
        results = self.chroma_db.query(query_text, top_k=top_k)

        if not results or 'documents' not in results:
            return "Không thể tìm thấy thông tin liên quan."

        retrieved_docs = results['documents'][0]

        # context = "\n\n".join(retrieved_docs)
        context = retrieved_docs[0][:256]
        augmented_prompt = f"""
        Dựa vào ngữ cảnh dưới đây, hãy trả lời câu hỏi.
        Ngữ cảnh: {context}
        Câu hỏi: {query_text}
        """

        return augmented_prompt
