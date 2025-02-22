from typing import List, Annotated
from fastapi import APIRouter, HTTPException, Query, Path
# from backend.app.services.azure_devops_services import AzureDevOpsService
from fastapi import APIRouter, HTTPException, Depends
from ..models.models import *
import logging
# from azure_authentication_client import authenticate_openai
from backend.app.models.base_service import BasePlatform
# from backend.app.services.llm_service import generate_doc
from typing import List
# from backend.app.services.llm_services.main_function import generate_doc





# authenticate_openai()
router = APIRouter()

#TODO: how will it receive the platform objects if its in router?
@router.get("/sprints/", response_model=List[Sprint])
async def get_sprints(platform: BasePlatform = Depends()) -> List[Sprint]:
        try:
            sprints = await platform.fetch_sprints()
            return sprints
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))



#TODO:we need a function that receives sprints list and runs the llm on it
# TODO: also we need a function to check if the file already exists and return it...
# @router.post("/generate", response_model=LLMResponse)
# async def generate_release_notes(sprints: List[str], platform: BasePlatform = Depends()):
#     try:
#         doc = await generate_doc(sprints)
#     except:
#         pass



