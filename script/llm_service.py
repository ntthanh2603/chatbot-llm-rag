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
        self.use_rag = use_rag

        # Initialize RAG if needed regardless of API use
        if self.use_rag:
            self.rag = RAG(model_embedding=model_embedding)

        if self.use_llm_api:
            self.api_key = os.getenv("GEMINI_API_KEY")
            if not self.api_key:
                raise ValueError("GEMINI_API_KEY is not set in the environment.")
            genai.configure(api_key=self.api_key)
            print("Configured Gemini API.")
            return  # Early return for API usage
       
        os.environ["CUDA_LAUNCH_BLOCKING"] = "1"

        self.model_list = [
            'mistralai/Mistral-7B-Instruct-v0.3',
            'Qwen/Qwen2.5-7B-Instruct',
            'meta-llama/Llama-3.1-8B-Instruct',
            'google/gemma-3-4b-it',
            'TinyLlama/TinyLlama-1.1B-Chat-v1.0',
        ]

        self.model_name = model_name if model_name else self.model_list[4]
        self.model_embedding = model_embedding

        self.cuda_available = torch.cuda.is_available() and use_gpu

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

    async def generate_text(self, prompt):
        # Check if self.rag exists and use_rag is True before using RAG
        # input_prompt = self.rag.rag_query(query_text=prompt, top_k=1) if self.use_rag and hasattr(self, 'rag') else prompt
        input_prompt = self.rag.rag_query(query_text=prompt, top_k=1) if self.use_rag  else prompt
        print("input_prompt", input_prompt)
        if self.use_llm_api:
            try:
                # Configure generation parameters
                generation_config = genai.GenerationConfig(
                    temperature=1.0,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=8192,
                )
                
                # Create the model with generation config
                model = genai.GenerativeModel(
                    model_name="gemini-2.0-flash",
                    generation_config=generation_config
                )
                
                # Start a chat session without passing generation_config again
                chat_session = model.start_chat(history=[])
                
                # Send message and await response
                response = await chat_session.send_message_async(input_prompt)
                return response.text
            except Exception as e:
                return f"Error using Gemini API: {str(e)}"

        try:
            inputs = self.tokenizer(input_prompt, return_tensors="pt")
            device = next(self.model.parameters()).device
            inputs = {k: v.to(device) for k, v in inputs.items()}

            with torch.inference_mode():
                output = self.model.generate(
                    **inputs,
                    do_sample=False,
                    num_beams=1,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )

            return self.tokenizer.decode(output[0], skip_special_tokens=True)
        except Exception as e:
            print(f"Error when generating text: {e}")
            return f"Cannot answer this question. Error: {str(e)[:100]}..."

    def test(self, path: str):
        pass