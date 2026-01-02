from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="{{project_name}}", version="{{version}}")
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to {{project_name}} API"}
