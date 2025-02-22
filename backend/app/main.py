from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from fastapi.params import Depends
from backend.app.routers.endpoints import router
from backend.app.services.azure_devops_services import AzureDevOpsService
from backend.app.services.storage_services import SharePointStorageService
from backend.app.utils.config import sharepoint_site, sharepoint_folder, sharepoint_username, sharepoint_password

# SETUP
app = FastAPI()
platform = AzureDevOpsService()
# database = SharePointStorageService(sharepoint_site, sharepoint_folder,
#                                     {"username": sharepoint_username, "password": sharepoint_password})

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
app.include_router(router, dependencies=[Depends(lambda: platform)])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Automated Release Notes Generator API"}
