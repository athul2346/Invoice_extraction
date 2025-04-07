import json
import re
from .utils import extract_text_from_pdf, clean_text, generate_invoice_json, generate_invoice_category
from sqlalchemy.orm import Session
from .utils import detect_duplicate_invoice, detect_amount_anomaly, detect_date_anomaly 


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


def detect_fraud(invoice_data: dict, db: Session):
    """Runs all fraud checks on an invoice."""
    anomalies = []
    
    # Check for duplicate invoices
    if detect_duplicate_invoice(db, invoice_data["invoice_number"], invoice_data["vendor"]):
        anomalies.append("Duplicate Invoice Detected")
    
    # Check for amount anomalies (assuming we have a history of past amounts)
    previous_amount = 1000  # Placeholder: Fetch from DB in a real setup
    if detect_amount_anomaly(previous_amount, invoice_data["total_amount"]):
        anomalies.append("Unusual Amount Change Detected")
    
    # Check for date inconsistencies
    if detect_date_anomaly(invoice_data["invoice_date"]):
        anomalies.append("Invalid or Future-Dated Invoice")

    return {"fraud_detected": len(anomalies) > 0, "anomalies": anomalies}