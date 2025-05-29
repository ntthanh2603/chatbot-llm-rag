# import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from rag_module import RAG
# from huggingface_hub import login
from dotenv import load_dotenv


class LLMService:
    def __init__(
        self, use_rag=True, model_name=None, 
        model_embedding="bkai-foundation-models/vietnamese-bi-encoder"
    ):
        # Load environment variables
        load_dotenv()

        self.model_name = model_name
        self.model_embedding = model_embedding

        # Initialize the RAG system if enabled
        self.use_rag = use_rag
        if self.use_rag:
            self.rag = RAG(model_embedding=model_embedding)

        print(f"Using LLM model for generation: {self.model_name}")
        if self.use_rag:
            print(f"Using embedding model for RAG: {self.model_embedding}")

        # Initialize tokenizer
        print(f"Loading tokenizer for {self.model_name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )
        print("Tokenizer loaded.")

        # Load the model without quantization
        print(f"Loading model {self.model_name}...")
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map="cuda",
            trust_remote_code=True
        )
        print("Model loaded successfully.")

    def through_llm(self, prompt, max_length):
        # Prepare model inputs
        inputs = self.tokenizer(prompt, return_tensors="pt")
        # Move inputs to the correct device
        device = next(self.model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        # Generate response
        output = self.model.generate(**inputs, max_new_tokens=max_length)

        answer = self.tokenizer.decode(
            output[0], skip_special_tokens=True
        )

        return answer

    def generate_text(self, prompt, max_length=512, use_rag=None, top_k=5):
        # Determine whether to use RAG
        should_use_rag = self.use_rag if use_rag is None else use_rag

        normal_answer = self.through_llm(prompt, max_length=max_length)

        return_dict = {
            "normal_answer": normal_answer
        }

        if should_use_rag:
            rag_prompt = self.rag.rag_query(prompt, top_k=top_k)
            rag_answer = self.through_llm(prompt, max_length=max_length)

            return_dict["rag_prompt"] = rag_prompt
            return_dict["rag_answer"] = rag_answer

        return return_dict

    def test(self, path: str):
        pass
