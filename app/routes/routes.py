from fastapi import APIRouter, File, UploadFile, HTTPException
from ..services import process_invoice
from ..models import InvoiceExtractionResponse

router = APIRouter()

@router.post("/extract-invoice", response_model=InvoiceExtractionResponse)
async def extract_invoice(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        response = await process_invoice(file)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
