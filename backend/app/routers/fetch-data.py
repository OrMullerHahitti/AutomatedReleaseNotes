import datetime
from typing import List,Annotated

from fastapi import APIRouter,HTTPException,Query,Body,Path

from app.tests.azure_devops_api import azure_devops_service
from ..services.base_service import BasePlatform
from fastapi.exception_handlers import http_exception_handler
from requests_toolbelt.multipart.decoder import BodyPart

from app.models.models import Commit, Sprint, WorkItem
from app.services.azure_devops_services import AzureDevOpsService

router = APIRouter()

@router.post("/get-work-items", response_model=List[WorkItem])
async def get_work_items(request:Annotated[List[str],Body(...,description="list of Sprints")] ):
    '''
    
    Fetch work items (User Stories,Features,Tasks) from azure devops based on range
    '''
    work_items=[]
    try:
        for sprint_name in request:
            work_item = await AzureDevOpsService.fetch_work_items(sprint_name)
            work_items.extend(work_item)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    return work_items






@router.get("/sprints/" ,response_model=List[Sprint])
async def get_sprints(platform : Annotated[str,Path("Azure",title="The platform we fetch from")]):
    '''
    
    Fetch sprints from azure devops
    '''
    if platform == 'Azure':

        try:

            sprints =await AzureDevOpsService.fetch_sprints()
            return sprints
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))


