import os
import torch
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training, PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from huggingface_hub import login
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the token
token = os.getenv("HF_TOKEN")

# Log in with the token
login(token=token)


# add huggingFace access token to load LLMs (get token from huggingFace: https://huggingface.co/)

model_list = [
    'mistralai/Mistral-7B-Instruct-v0.3',
    'Qwen/Qwen2.5-7B-Instruct',
    'meta-llama/Llama-3.1-8B-Instruct', # login to huggingFace and agree its policy first
    'google/gemma-3-4b-it',
]

model_name = model_list[0]

# load model and tokenizer

# load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

# quantize model to 4bit to reduce the memory, reference: https://arxiv.org/pdf/2305.14314
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=False,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

# load model
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    quantization_config=quantization_config,
    trust_remote_code=True,
)

# inference function
def generate_text(prompt, max_length=512):
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    output = model.generate(**inputs, max_length=max_length)
    return tokenizer.decode(output[0], skip_special_tokens=True)

# test
prompt = "Tell a funny story!"
output = generate_text(prompt)
print(output)

prompt2 = "Hoàng Sa, Trường Sa là của nước nào?"
output2 = generate_text(prompt2)
print(output2)

