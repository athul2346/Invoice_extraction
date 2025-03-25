from pydantic import BaseModel
from typing import List, Optional

class InvoiceExtractionResponse(BaseModel):
    invoice_number: Optional[str]
    date: Optional[str]
    total_amount: Optional[float]
    currency: Optional[str]
    vendor_name: Optional[str]
    line_items: List[dict]
