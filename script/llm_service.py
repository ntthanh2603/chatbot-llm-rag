import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from script.rag_module import RAG
from dotenv import load_dotenv

class LLMService:
    def __init__(self, use_rag=True, model_name=None, model_embedding="bkai-foundation-models/vietnamese-bi-encoder", 
                 use_gpu=False, use_4bit=False):
        # Load environment variables
        load_dotenv()
        
        # Set CUDA environment variables for better error reporting
        os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
        
        # Define available models
        self.model_list = [
            'mistralai/Mistral-7B-Instruct-v0.3', # 14gb
            'Qwen/Qwen2.5-7B-Instruct', # 14gb
            'meta-llama/Llama-3.1-8B-Instruct', # 16gb
            'google/gemma-3-4b-it', # 8gb
            'TinyLlama/TinyLlama-1.1B-Chat-v1.0', # 2.2gb
        ]
        
        # Set the model name (default to smallest model if not specified)
        self.model_name = model_name if model_name else self.model_list[3]  # Chọn mô hình nhỏ nhất TinyLlama
        self.model_embedding = model_embedding
        
        # Kiểm tra xem CUDA có sẵn không
        self.cuda_available = torch.cuda.is_available() and use_gpu
        
        # Initialize the RAG system if enabled
        self.use_rag = use_rag
        if self.use_rag:
            self.rag = RAG(model_embedding=model_embedding)
        
        # Initialize tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )

        if self.tokenizer.pad_token is None:
            if self.tokenizer.eos_token is not None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            else:
                self.tokenizer.pad_token = self.tokenizer.eos_token = "</s>"

        if self.cuda_available and use_4bit:
            try:
                print(f"Đang tải mô hình {self.model_name} trên GPU với lượng tử hóa 4-bit...")

                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_use_double_quant=False,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.bfloat16
                )
                

                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    device_map="auto",
                    trust_remote_code=True,
                    quantization_config=quantization_config
                )
            except Exception as e:
                print(f"Không thể tải mô hình với lượng tử hóa 4-bit: {e}")
                print("Chuyển sang sử dụng GPU mà không có lượng tử hóa...")
                self.cuda_available = True
                use_4bit = False
                
        if self.cuda_available and not use_4bit:
            print(f"Đang tải mô hình {self.model_name} trên GPU...")
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                device_map="auto",
                trust_remote_code=True,
                torch_dtype=torch.float16 
            )
        else:
            print(f"Đang tải mô hình {self.model_name} trên CPU. Quá trình này có thể mất nhiều thời gian...")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                device_map="cpu",
                trust_remote_code=True,
                torch_dtype=torch.float32
            )
        
        print("Model loaded successfully.")
        
    def generate_text(self, prompt, max_length=2048, use_rag=None):
        # Determine whether to use RAG
        should_use_rag = self.use_rag if use_rag is None else use_rag

        if should_use_rag:
            # Get RAG-augmented prompt
            rag_prompt = self.rag.rag_query(query_text=prompt, top_k=1)
            input_prompt = rag_prompt
        else:
            input_prompt = prompt

        # Prepare model inputs
        inputs = self.tokenizer(input_prompt, return_tensors="pt")

        # Move inputs to the correct device
        device = next(self.model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # Generate response with error handling
        try:
            with torch.inference_mode():
                output = self.model.generate(
                    **inputs, 
                    max_length=max_length,
                    do_sample=False,
                    num_beams=1,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode and return the response
            return self.tokenizer.decode(output[0], skip_special_tokens=True)
        
        except Exception as e:
            print(f"Lỗi khi sinh văn bản: {e}")
            return f"Không thể trả lời câu hỏi này. Lỗi: {str(e)[:100]}..."
    
    def test(self, path: str):
        pass