import datetime
from typing import List

from fastapi import APIRouter,HTTPException,Query,Body
from fastapi.exception_handlers import http_exception_handler
from requests_toolbelt.multipart.decoder import BodyPart

from app.models.models import Commit, Sprint
from app.services.azure_devops_services import fetch_work_items

router = APIRouter()

@router.post("/get-work-items", response_model=List[Commit])
async def get_work_items(request: Body(...,description="list of commits")):
    '''
    
    Fetch work items (User Stories,Features,Tasks) from azure devops based on range
    '''
    try:
        work_items =await fetch_work_items(request.start_date, request.end_date)
        return work_items
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))




@router.get("/get-sprints" ,response_model=List[Sprint])
async def get_sprints(start_date: str = Query(...,description="start date of sprint"), end_date: str = Query(...,description="end date of sprint")):
    '''
    
    Fetch repositories from azure devops
    '''
    try:
        repositories =await fetch_sprints(start_date,end_date)
        return repositories
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


