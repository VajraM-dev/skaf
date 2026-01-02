from fastapi import APIRouter

router = APIRouter()

@app.get("/health")
async def health():
    return {"status": "healthy"}
