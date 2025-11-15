from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.endpoints import auth, currency
from app.core.database import db, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_db()
    yield
    await db.close_db()

app = FastAPI(
    title="Currency Exchange API",
    version="2.0.0",
    description="Asynchronous currency exchange API with JWT authentication",
    lifespan=lifespan,
)
app.include_router(auth.router, prefix="/api/v1")
app.include_router(currency.router, prefix="/api/v1")

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Currency Exchange API v2.0 is running!",
        "docs": "/docs",
        "health": "/health"
    }
@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}