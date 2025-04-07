from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Float, Date

class InvoiceExtractionResponse(BaseModel):
    invoice_number: Optional[str]
    date: Optional[str]
    total_amount: Optional[float]
    currency: Optional[str]
    vendor_name: Optional[str]
    line_items: List[dict]


class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, index=True)
    vendor = Column(String, index=True)
    invoice_date = Column(Date)
    total_amount = Column(Float)