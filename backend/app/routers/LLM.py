# backend/app/routers/LLM.py
from types import new_class

import httpx
from fastapi import APIRouter, HTTPException,Body
from ..models.models import *
import logging
from azure_authentication_client import authenticate_openai
import openai
authenticate_openai()
from backend.app.services.llm_service import generate_doc
from typing import List
from backend.app.models import Sprint
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate

from ..services.llm_service import get_llm
from backend.app.services.azure_devops_services import BasePlatform,AzureDevOpsService
from backend.app.services.llm_service import generate_doc


router = APIRouter(
    prefix="/api",
    tags=["Generate Release Notes"]
)
work_items =[]
logger = logging.getLogger(__name__)

@router.post("/generate-release-notes", response_model=Document)
async def generate_text(request: List[str] = Body(...,description="List of sprint names selected by the user"),base:BasePlatform=AzureDevOpsService()):
    try:
        #example dict:

        work_items = await base.fetch_work_items(request)

        reposne_doc  = await generate_doc(work_items)





