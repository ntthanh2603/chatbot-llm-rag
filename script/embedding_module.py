from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer

class Embedding:
    def __init__(self, model_embedding="bkai-foundation-models/vietnamese-bi-encoder", chunk_size=512):
        self.model_embedding = model_embedding
        self.chunk_size = chunk_size
        self.tokenizer = AutoTokenizer.from_pretrained(model_embedding, trust_remote_code=True)
        self.embedding_model = SentenceTransformer(model_embedding)  

    def split_file_by_chunk_size(self, text: str):
        tokens = self.tokenizer.encode(text, add_special_tokens=False)
        chunks = [tokens[i:i+self.chunk_size] for i in range(0, len(tokens), self.chunk_size)]
        return [self.tokenizer.decode(chunk) for chunk in chunks]

    def embedding(self, text: str):
        return self.embedding_model.encode(text).tolist()
