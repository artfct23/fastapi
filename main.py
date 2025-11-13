from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.endpoints import auth, currency
from app.core.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(
    title="Currency Exchange API",
    version="2.0.0",
    description="Асинхронный API обмена валют с JWT аутентификацией",
    lifespan=lifespan
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(currency.router, prefix="/api/v1")


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Currency Exchange API v2.0 работает!"}


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy"}
