from fastapi import FastAPI

from app.database import engine

app = FastAPI(
    title="Advanced SqlAlchemy with FastAPI"
)

@app.get("/")
async def home():
    return {
        "message":"Advanced SqlAlchemy App Started"
    }

@app.get("/health")
async def health_check():
    async with engine.connect() as connection:
        await connection.exec_driver_sql("SELECT 1")
        
    return {
        "status":"healthy",
        "database":"connected"
    }