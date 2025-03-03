# In backend/app/routers/endpoints.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from backend.app.services.azure_devops_services import AzureDevOpsService
from backend.app.utils.config import (authentication_headers_azure, azure_devops_org, azure_devops_project, azure_devops_team, azure_devops_iteration_team)
from backend.app.models.models import Sprint, WorkItem, LLMResponse
import logging
from azure_authentication_client import authenticate_openai
from langchain_openai import AzureChatOpenAI
from backend.app.services.llm_services.generate import BasicGenerator
from backend.app.utils.useful_functions import get_azure_llm

# Initialize FastAPI router for the endpoints
router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dependency to get AzureDevOpsService platform connection
async def get_platform(
    auth_headers: dict = Depends(lambda: authentication_headers_azure),
    org: str = Depends(lambda: azure_devops_org),
    project: str = Depends(lambda: azure_devops_project),
    team: str = Depends(lambda: azure_devops_team),
    iteration_team: str = Depends(lambda: azure_devops_iteration_team)
) -> AzureDevOpsService:
    """
    Creates and returns an instance of AzureDevOpsService based on the provided configuration.
    This is used as a dependency for endpoints that require access to Azure DevOps API.
    """
    logger.info(f"Injecting into AzureDevOpsService: org={org}, project={project}, team={team}, iteration_team={iteration_team}")
    return AzureDevOpsService(
        auth_headers=auth_headers,
        azure_devops_org=org,
        azure_devops_project=project,
        azure_devops_team=team,
        azure_devops_iteration_team=iteration_team
    )

# Dependency to create an instance of BasicGenerator
# async def get_generator():
#     """
#     Creates and returns a BasicGenerator instance for generating release notes.
#     This function handles the creation of the LLM configuration and its associated generator.
#     """
#     try:
#         llm = get_azure_llm()
#         logger.info(f"Injecting llm configuration into BasicGenerator {llm}")
#         return BasicGenerator(llm)
#     except Exception as e:
#         logger.error(f"Unexpected error occurred while creating the generator: {e}")


# Endpoint to fetch all sprints from Azure DevOps platform
@router.get("/sprints/", response_model=List[Sprint])
async def get_sprints(platform: AzureDevOpsService = Depends(get_platform)) -> List[Sprint]:
    """
    Fetches a list of sprints from Azure DevOps.
    This endpoint interacts with AzureDevOpsService to get sprint details.
    """
    try:
        logger.info("Fetching sprints...")
        sprints = await platform.fetch_sprints()
        logger.info(f"Fetched sprints: {sprints}")
        return sprints
    except HTTPException as e:
        logger.error(f"HTTPException occurred a call to /sprints/ API: {e}")
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error occurred during a call to /sprints/ API: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Endpoint to generate release notes based on work items from chosen sprints
# @router.post("/generate/", response_model=LLMResponse)
# async def generate_release_notes(sprints: List[str], generator: BasicGenerator = Depends(get_generator),
#                       platform: AzureDevOpsService = Depends(get_platform)) -> LLMResponse:
#     """
#     Generates release notes based on work items from one or more sprints.
#     This endpoint fetches work items and feeds them to a language model for release note generation,
#     and returns the GenAI response.
#     """
#     try:
#         logger.info("Starting RN generation process...")
#         work_items = await platform.fetch_work_items_for_multiple_sprints(sprints)
#         logger.info(f"Successfully pulled {len(work_items)} work items...: {[item.id for item in work_items]}")
#         logger.info(f"Feeding the data to the LLM: ")
#         response = await generator.generate(work_items)
#         logger.info("Successfully generated the release notes.")
#         return response
#     except HTTPException as e:
#         logger.error(f"HTTPException occurred during a call to /generate/ API : {e}")
#         raise HTTPException(status_code=e.status_code, detail=str(e))
#     except Exception as e:
#         logger.error(f"Unexpected error occurred during a call to /generate/ API: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")



# A simple test endpoint that returns a "hello world" string
@router.get("/test/", response_model=str)
async def test() -> str:
    """
    A simple test endpoint to ensure the API is working correctly.
    It returns a "hello world" string for testing purposes.
    """
    try:
        result = "@@@@"
        return result
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
