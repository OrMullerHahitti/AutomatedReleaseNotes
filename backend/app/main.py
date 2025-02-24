# In backend/app/main.py
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from backend.app.routers.endpoints import router
from backend.app.utils.useful_functions import make_request
from backend.app.utils.config import authentication_headers_azure
from backend.app.services.azure_devops_services import AzureDevOpsService
from backend.app.services.azure_devops_services import AzureDevOpsService
from backend.app.utils.config import authentication_headers_azure


# uvicorn backend.app.main:app --reload
# uvicorn backend.app.main:app --reload --log-level debug

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



# # Define the async function for testing
# async def test_sprints():
#     try:
#         logger.info("Making a request to /sprints/")
#         response = await make_request("http://127.0.0.1:8000/sprints/", "GET")
#         logger.info(f"Status Code: {response.status_code}")
#         logger.info(f"Response: {response.json()}")
#     except Exception as e:
#         logger.error(f"Error occurred: {e}")
#
# # Call the test_sprints function directly (for testing purposes)
# asyncio.run(test_sprints())

