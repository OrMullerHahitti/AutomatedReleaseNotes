# In backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from backend.app.routers.endpoints import router
from backend.app.utils.config import allowed_origins_dev, allowed_origins_prod , logging_level


# Run: uvicorn backend.app.main:app --reload --log-level debug

# SETUP
app = FastAPI()

# Configure logging
logging.basicConfig(level=getattr(logging, logging_level , logging.INFO))
logger = logging.getLogger(__name__)

# Configure CORS
origins = [
    allowed_origins_dev,  # Frontend during development
    allowed_origins_prod  # Frontend in production
]

# Instantiate the CORSMiddleware class
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Automated Release Notes Generator API"}

