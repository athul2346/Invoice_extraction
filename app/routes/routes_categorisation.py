from fastapi import APIRouter, File, UploadFile, HTTPException
from ..services import categorise_invoice

router =APIRouter()


@router.post("/categorise-invoice)")
async def invoice_categorisation(
    file: UploadFile = File(...)
):
    if not file.filename.endswith("pdf"):
        raise HTTPException(status_code=400, detail="Only pDF files allowed")
    try:
        response = await categorise_invoice(file)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))