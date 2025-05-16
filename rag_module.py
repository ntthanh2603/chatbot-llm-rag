from pinecone_module import PineconeDBClient
import re


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

    def clean_rag_output(self, raw_text: str) -> str:
        # Step 1: Remove bracketed numbers like [3, [5, [6, etc.
        text = re.sub(r'\[\d+', '', raw_text)

        # Step 2: Remove all <unk> tokens
        text = text.replace('<unk>', '')

        # Step 3: Remove stray punctuation and normalize spaces
        text = re.sub(
            r'[,:;()]+', lambda m: m.group(0)
            if m.group(0) in (',', '.', '?', '!') else '', text
        )
        text = re.sub(r'\s+', ' ', text)  # Normalize spaces

        # Step 4: Strip leading/trailing whitespace
        return text.strip()

    def rag_query(self, query_text, top_k=3):
        results = self.db.query(query_text, top_k=top_k)

        if not results or 'documents' not in results:
            return "Không thể tìm thấy thông tin liên quan."

        retrieved_docs = results['documents'][0]

        retrieved_docs = self.clean_rag_output(retrieved_docs)

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
