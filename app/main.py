from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.api.routes import router
from app.core.config import settings
from app.core.logging import logger, setup_logging
from app.core.qdrant import client

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    client.get_collections()
    logger.info("Connected to Qdrant")
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Agentic RAG for Software Engineering Question Answering",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "healthy",
        "environment": settings.app_env,
        "version": "1.0.0",
    }


@app.get("/", tags=["Root"])
async def root():
    return {"message": f"Welcome to {settings.app_name}"}


frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if (frontend_dir / "index.html").exists():
    app.mount("/app", StaticFiles(directory=frontend_dir, html=True), name="frontend")
