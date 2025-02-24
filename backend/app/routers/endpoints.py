# In backend/app/routers/endpoints.py
import math

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from backend.app.services.azure_devops_services import AzureDevOpsService
from backend.app.utils.config import (authentication_headers_azure, azure_devops_org, azure_devops_project,
                                      azure_devops_team,azure_devops_iteration_team)
from backend.app.utils.config import testy, load_dotenv
from backend.app.models.models import Sprint
import logging
import pdb

# load_dotenv()
# print(testy.check)

router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_platform(
    auth_headers: dict = Depends(lambda: authentication_headers_azure),
    org: str = Depends(lambda: f'{testy.test}'),
    project: str = Depends(lambda: f'{azure_devops_project}'),
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



# Use Depends to inject the platform dependency
# @router.get("/sprints/", response_model=List[Sprint])
# async def get_sprints(platform: AzureDevOpsService = Depends(get_platform)) -> List[Sprint]:
#     try:
#         logger.info("Fetching sprints...")
#         # pdb.set_trace()
#         sprints = await platform.fetch_sprints()
#         logger.info(f"Fetched sprints: {sprints}")
#         return sprints
#     except HTTPException as e:
#         logger.error(f"HTTPException occurred: {e}")
#         raise HTTPException(status_code=e.status_code, detail=str(e))
#     except Exception as e:
#         logger.error(f"Unexpected error occurred: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")


# Use Depends to inject the platform dependency
@router.get("/test/", response_model=str)
async def test() -> str:
    try:
        result = "hello world 6666666"
        return result
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.get("/test-platform/")
async def test_platform(platform: AzureDevOpsService = Depends(get_platform)):
    return {
        "auth headrs": platform.auth_headers,
        "org": platform.azure_devops_org,
        "project": platform.azure_devops_project,
        "team": platform.azure_devops_team,
        "iteration_team": platform.azure_devops_iteration_team
    }



