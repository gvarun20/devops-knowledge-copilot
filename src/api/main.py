"""FastAPI application entrypoint."""

import logging

from dotenv import load_dotenv
from fastapi import FastAPI

from src.api.routes import router

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI(
    title="DevOps Knowledge Copilot",
    description="RAG Q&A over Terraform and Kubernetes official documentation.",
    version="0.2.0",
)
app.include_router(router)
