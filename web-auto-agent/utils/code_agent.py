import os
from dotenv import load_dotenv
from transformers import pipeline

# Load environment variables
load_dotenv()

def generate_code(prompt):
    huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
    code_generator = pipeline("text-generation", model="bigcode/starcoder", use_auth_token=huggingface_api_key)
    return code_generator(prompt)[0]['generated_text']
