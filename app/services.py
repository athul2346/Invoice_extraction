import json
import re
from .utils import extract_text_from_pdf, clean_text, generate_invoice_json, generate_invoice_category

async def process_invoice(file):
    pdf_bytes = await file.read()
    extracted_text = extract_text_from_pdf(pdf_bytes)
    cleaned_text = clean_text(extracted_text)
    invoice_json = generate_invoice_json(cleaned_text)
    
    match = re.search(r'\{.*\}', invoice_json, re.DOTALL)
    if not match:
        raise ValueError("Failed to extract valid JSON")
    
    return json.loads(match.group(0))  


async def categorise_invoice(file):
    pdf_bytes = await file.read()
    extracted_text = extract_text_from_pdf(pdf_bytes)
    cleaned_text = clean_text(extracted_text)
    category = generate_invoice_json(cleaned_text)
    word_count = len(str(category).split())
    if word_count > 1:
        raise ValueError("More than one word output")
    return category