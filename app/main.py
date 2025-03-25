from fastapi import FastAPI
from app.routes.routes import router as invoice_router
from app.routes.routes_categorisation import router as categorization_router

app = FastAPI(title="Invoice Processing API", version="1.0")

# Include existing invoice extraction API
app.include_router(invoice_router)

# Include new invoice categorization API
app.include_router(categorization_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)