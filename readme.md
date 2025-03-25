# Invoice Extraction API 🚀

This FastAPI project extracts invoice details from PDFs using Qwen LLM.

## Features
✅ Extracts invoice data (vendor, date, amount, etc.)  
✅ Cleans extracted text with regex  
✅ Uses LLM (Qwen 7B) to generate structured JSON  

## Installation
```sh
git clone https://github.com/yourusername/invoice_extraction_api.git
cd invoice_extraction_api
pip install -r requirements.txt



uvicorn app.main:app --reload
