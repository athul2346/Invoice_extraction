import pdfplumber
import re
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from io import BytesIO

# Load Qwen model
MODEL_NAME = "Qwen/Qwen2.5-Coder-7B-Instruct"
CACHE_DIR = "/home/ubuntu/huggingface_models"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=CACHE_DIR)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, torch_dtype="auto", device_map="auto", cache_dir=CACHE_DIR
)

def extract_text_from_pdf(file: BytesIO) -> str:
    extracted_text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text(x_tolerance=2, y_tolerance=2) or ""
            extracted_text += text + "\n"
    return extracted_text.strip()

def clean_text(text: str) -> str:
    text = re.sub(r'(Page|Seite|Pág|Pagina)\s*\d+\s*(of|von|de|di)?\s*\d*', '', text, flags=re.IGNORECASE)
    irrelevant_sections = [
        "Terms and Conditions", "Thank you for your business", "If you have any questions",
        "For inquiries contact", "This is a computer-generated document", "Please remit payment to"
    ]
    for section in irrelevant_sections:
        text = re.sub(rf'{re.escape(section)}.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\n+', '\n', text).strip()
    text = re.sub(r'(\d+)\n+(\D)', r'\1 \2', text)
    text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
    text = re.sub(r'(\w+)\n(\w+)', r'\1 \2', text)
    text = re.sub(r'[\|_]+', '', text)
    text = re.sub(r'(\d{1,2})(st|nd|rd|th)\b', r'\1', text)
    return text

def generate_invoice_json(extracted_text: str) -> str:
    prompt = f"Extract details from the following invoice text and return only a valid JSON object. {extracted_text}"
    
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        output_tokens = model.generate(**inputs, max_length=4096, temperature=0.2)
    
    return tokenizer.decode(output_tokens[0], skip_special_tokens=True).strip()


def generate_invoice_category(extracted_text: str) ->str:
    prompt = f"""Analyse the following text and identify the category of Invoice it belongs to and give a single word answer. {extracted_text}
                Only one word answer is needed showing which category the invoice is. No need of explanation or any other
                words."""

    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        output_tokens = model.generate(**inputs, max_length=4096, temperature=0.2)
    
    return tokenizer.decode(output_tokens[0], skip_special_tokens=True).strip()