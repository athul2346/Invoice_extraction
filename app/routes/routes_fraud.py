# app/routes/routes_fraud.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.fraud_detection import detect_fraud
from app.models import Invoice

router = APIRouter()

@router.post("/detect-fraud")
async def detect_invoice_fraud(invoice_data: dict, db: Session = Depends(get_db)):
    """
    API to detect invoice fraud based on predefined rules.
    """
    if not invoice_data:
        raise HTTPException(status_code=400, detail="Invoice data is required")
    
    result = detect_fraud(invoice_data, db)
    return result
