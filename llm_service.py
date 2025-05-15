import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from script.rag_module import RAG
# from huggingface_hub import login
from dotenv import load_dotenv

class LLMService:
    def __init__(self, use_rag=True, model_name=None, model_embedding="bkai-foundation-models/vietnamese-bi-encoder"):
        # Load environment variables
        load_dotenv()
        
        # Login to HuggingFace
        # token = os.getenv("HF_TOKEN")
        # if token:
        #     login(token=token)
        
        # Define available models
        self.model_list = [
            'mistralai/Mistral-7B-Instruct-v0.3', # 14gb
            'Qwen/Qwen2.5-7B-Instruct', # 14gb
            'meta-llama/Llama-3.1-8B-Instruct', # 16gb
            'google/gemma-3-4b-it', # 8gb
            'TinyLlama/TinyLlama-1.1B-Chat-v1.0', # 2.2gb
        ]
        
        # Set the model name (default to first model if not specified)
        self.model_name = model_name if model_name else self.model_list[-1]
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
            device_map="auto",
            trust_remote_code=True
        )
        print("Model loaded successfully.")
    
    def generate_text(self, prompt, max_length=512, use_rag=None):
        # Determine whether to use RAG
        should_use_rag = self.use_rag if use_rag is None else use_rag
        
        if should_use_rag:
            # Get RAG-augmented prompt
            rag_prompt = self.rag.rag_query(prompt)
            input_prompt = rag_prompt
        else:
            input_prompt = prompt
        
        # Prepare model inputs
        inputs = self.tokenizer(input_prompt, return_tensors="pt")
        
        # Move inputs to the correct device
        device = next(self.model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # Generate response
        output = self.model.generate(**inputs, max_length=max_length)
        # print("output", output)
        
        # Decode and return the response
        return self.tokenizer.decode(output[0], skip_special_tokens=True)
    
    def test(self, path: str):
        pass