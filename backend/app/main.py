# In backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from backend.app.routers.endpoints import router


# Run: uvicorn backend.app.main:app --reload --log-level debug

# SETUP
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure CORS
origins = [
    "http://localhost:3000",  # Frontend during development
    "https://your-frontend-domain.com"  # Frontend in production
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

