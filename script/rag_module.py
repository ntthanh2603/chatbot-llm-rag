from script.chromadb_module import ChromaDBClient

class RAG:
    def __init__(self, model_embedding="bkai-foundation-models/vietnamese-bi-encoder", chunk_size=512):
        self.chroma_db = ChromaDBClient(model_embedding=model_embedding, chunk_size=chunk_size)

    def rag_query(self, query_text, top_k=3):
        results = self.chroma_db.query(query_text, top_k=top_k)

        if not results or 'documents' not in results:
            return "Không thể tìm thấy thông tin liên quan."
        
        
        retrieved_docs = results['documents'][0]

        context = "\n\n".join(retrieved_docs)
        # context = retrieved_docs[0][:512]
        # augmented_prompt = f"""
        # Dựa vào ngữ cảnh dưới đây, hãy trả lời câu hỏi.
        # Ngữ cảnh: {context}
        # Câu hỏi: {query_text}
        # """

        augmented_prompt = f"""
        Dựa vào 1 phần ngữ cảnh sau hãy trả lời các câu hỏi bên dưới: {context}
        Câu hỏi: {query_text}
        """
        print("Augment", augmented_prompt)
    
        return augmented_prompt