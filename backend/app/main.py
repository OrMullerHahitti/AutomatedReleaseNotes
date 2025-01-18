# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import LLM
import logging
from app.models.LLM import WorkItemsRequest
from app.services.azure_devops_services import *

app = FastAPI(
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure CORS
origins = [
    "http://localhost:3000",  # Frontend during development
    "https://your-frontend-domain.com"  # Frontend in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(generate.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Automated Release Notes Generator API"}

