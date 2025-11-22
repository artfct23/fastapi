from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.endpoints import auth, currency
from app.core.database import db


@asynccontextmanager
async def lifespan(app: FastAPI):
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
        "message": "Currency Exchange API is running!",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy"}
