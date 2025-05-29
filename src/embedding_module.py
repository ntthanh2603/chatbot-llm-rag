from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer

import re


class Embedding:
    def __init__(
        self,
        model_embedding="bkai-foundation-models/vietnamese-bi-encoder",
        chunk_size=256
    ):
        self.model_embedding = model_embedding
        self.chunk_size = chunk_size
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_embedding, trust_remote_code=True
        )
        self.embedding_model = SentenceTransformer(model_embedding)
        self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()

    def chunk_text_old(self, text: str):
        tokens = self.tokenizer.encode(text, add_special_tokens=False)
        chunks = [
            tokens[i:i+self.chunk_size]
            for i in range(0, len(tokens), self.chunk_size)
        ]
        return [self.tokenizer.decode(chunk) for chunk in chunks]

    def chunk_text(self, text: str):
        def tokenize_and_check_length(text_chunk):
            tokens = self.tokenizer.encode(
                text_chunk, add_special_tokens=False
            )
            return tokens, len(tokens)

        def decode_tokens(tokens):
            return self.tokenizer.decode(tokens)

        def split_by_token(tokens, max_len):
            if len(tokens) <= max_len * 1.1:
                return [tokens]
            else:
                mid = len(tokens) // 2
                return split_by_token(
                    tokens[:mid], max_len
                ) + split_by_token(tokens[mid:], max_len)

        def process_chunk(text_chunk):
            tokens, length = tokenize_and_check_length(text_chunk)

            if length <= self.chunk_size * 1.1:
                return [decode_tokens(tokens)]
            elif length <= self.chunk_size * 1.5:
                return [
                    decode_tokens(chunk)
                    for chunk in split_by_token(tokens, self.chunk_size)
                ]
            else:
                # Step 2: Try splitting by comma
                subchunks = [
                    s.strip() for s in text_chunk.split(',') if s.strip()
                ]
                results = []
                for s in subchunks:
                    tokens_s, len_s = tokenize_and_check_length(s)
                    if len_s <= self.chunk_size * 1.1:
                        results.append(decode_tokens(tokens_s))
                    else:
                        # Step 3: Split by token
                        token_chunks = split_by_token(
                            tokens_s, self.chunk_size
                        )
                        results.extend(
                            [decode_tokens(t) for t in token_chunks]
                        )
                return results

        # Step 1: Initial split by sentence (dot or newline)
        rough_chunks = re.split(r'\.\s+|\n+', text)
        rough_chunks = [
            chunk.strip() for chunk in rough_chunks if chunk.strip()
        ]

        final_chunks = []
        for chunk in rough_chunks:
            final_chunks.extend(process_chunk(chunk))

        return final_chunks

    def embedding(self, text: str):
        return self.embedding_model.encode(text).tolist()
