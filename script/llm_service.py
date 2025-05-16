import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from script.rag_module import RAG
from dotenv import load_dotenv
import google.generativeai as genai

class LLMService:
    def __init__(self, use_rag=True, use_llm_api=False, model_name=None, model_embedding="bkai-foundation-models/vietnamese-bi-encoder", 
                 use_gpu=False, use_4bit=False):
        # Load environment variables
        load_dotenv()

        self.use_llm_api = use_llm_api

        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set in the environment.")
        genai.configure(api_key=self.api_key)
        
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
                print(f"Downloading model {self.model_name} on GPU with quantize 4-bit...")

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
                print(f"Unable to load model with quantization 4-bit: {e}")
                print("Switch to GPU without quantization...")
                self.cuda_available = True
                use_4bit = False
                
        if self.cuda_available and not use_4bit:
            print(f"Downloading model {self.model_name} on GPU...")
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                device_map="auto",
                trust_remote_code=True,
                torch_dtype=torch.float16 
            )
        else:
            print(f"Downloading model {self.model_name} on CPU.")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                device_map="cpu",
                trust_remote_code=True,
                torch_dtype=torch.float32
            )
        
        print("Model loaded successfully.")
        
    async def generate_text(self, prompt, use_rag=None):
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
            if self.use_llm_api :
                model = genai.GenerativeModel(model_name="gemini-2.0-flash")

                generation_config = {
                    "temperature": 1,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 8192,
                    "response_mime_type": "text/plain",
                }

                chat_session = model.start_chat(
                    history=[],
                    generation_config=generation_config,
                )

                response = await chat_session.send_message(inputs)
                return {"result": response.text}
            else:
                with torch.inference_mode():
                    output = self.model.generate(
                        **inputs, 
                        do_sample=False,
                        num_beams=1,
                        pad_token_id=self.tokenizer.pad_token_id,
                        eos_token_id=self.tokenizer.eos_token_id
                    )
                
                # Decode and return the response
                return self.tokenizer.decode(output[0], skip_special_tokens=True)
        
        except Exception as e:
            print(f"Error when gen word: {e}")
            return f"Cannot answer this question. Error: {str(e)[:100]}..."\
            
   
    def test(self, path: str):
        pass