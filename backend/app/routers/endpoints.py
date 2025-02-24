# In backend/app/routers/endpoints.py


from fastapi import APIRouter, Depends, HTTPException
from typing import List
from backend.app.services.azure_devops_services import AzureDevOpsService
from backend.app.utils.config import (authentication_headers_azure, azure_devops_org, azure_devops_project,
                                      azure_devops_team,azure_devops_iteration_team)
from backend.app.models.models import Sprint, LLMResponse
import logging
from azure_authentication_client import authenticate_openai
from langchain_openai import AzureChatOpenAI
from backend.app.services.llm_services.generating_policies import BasicGenerator
from backend.app.services.azure_devops_services import AzureDevOpsService
from backend.app.utils.useful_functions import get_azure_llm




router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_platform(
    auth_headers: dict = Depends(lambda: authentication_headers_azure),
    org: str = Depends(lambda: azure_devops_org),
    project: str = Depends(lambda: azure_devops_project),
    team: str = Depends(lambda: azure_devops_team),
    iteration_team: str = Depends(lambda: azure_devops_iteration_team)
) -> AzureDevOpsService:
    print(f"Injecting into AzureDevOpsService: org={org}, project={project}, team={team}, iteration_team={iteration_team}")
    return AzureDevOpsService(
        auth_headers=auth_headers,
        azure_devops_org=org,
        azure_devops_project=project,
        azure_devops_team=team,
        azure_devops_iteration_team=iteration_team
    )

async def get_generator():
    try:
        llm = get_azure_llm()
        return BasicGenerator(llm)
    except Exception as e:
        logger.error(f"Unexpected error occurred while creating the generator: {e}")


@router.get("/sprints/", response_model=List[Sprint])
async def get_sprints(platform: AzureDevOpsService = Depends(get_platform)) -> List[Sprint]:
    try:
        logger.info("Fetching sprints...")
        sprints = await platform.fetch_sprints()
        logger.info(f"Fetched sprints: {sprints}")
        return sprints
    except HTTPException as e:
        logger.error(f"HTTPException occurred: {e}")
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


#TODO: use cached for the platofrm object
@router.post("/generate/", response_model=LLMResponse)
async def generate_rn(sprints: List[str], generator: BasicGenerator = Depends(get_generator),
                      platform: AzureDevOpsService = Depends(get_platform)) -> LLMResponse:
    try:
        logger.info("Starting RN generation...")
        work_items = await platform.fetch_work_items_for_multiple_sprints(sprints)
        logger.info("Successfully pulled the work items...")
        response = await generator.generate(work_items)
        logger.info("Successfully generated the release notes...")
        return response
    except HTTPException as e:
        logger.error(f"HTTPException occurred: {e}")
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Use Depends to inject the platform dependency
@router.get("/test/", response_model=str)
async def test() -> str:
    try:
        result = "hello world 44444"
        return result
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))



