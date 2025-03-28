# In backend/app/routers/endpoints.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from typing import List
from backend.app.services.azure_devops_services import AzureDevOpsService
from backend.app.services.storage_services import BlobStorageService
from backend.app.utils.config import (authentication_headers_azure, azure_devops_org, azure_devops_project, azure_devops_team,
                                      azure_devops_iteration_team, blob_storage_account_url, blob_storage_container_name, logging_level)
from backend.app.models.models import Sprint, SprintRequest
from backend.app.utils.useful_functions import convert_text_to_docx, convert_docx_to_bytes, get_container_id
import logging
from backend.app.services.llm_services.generate import BasicGenerator
from backend.app.utils.useful_functions import get_azure_llm
from io import BytesIO



# Initialize FastAPI router for the endpoints
router = APIRouter()
logging.basicConfig(level=getattr(logging, logging_level , logging.INFO))
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
async def get_generator():
    """
    Creates and returns a BasicGenerator instance for generating release notes.
    This function handles the creation of the LLM configuration and its associated generator.
    """
    try:
        llm = get_azure_llm()
        logger.info(f"Injecting llm configuration into BasicGenerator {llm}")
        return BasicGenerator(llm)
    except Exception as e:
        logger.error(f"Unexpected error occurred while creating the generator: {e}")


# Dependency to create an instance of StorageService
async def get_storage_service():
    """
       Creates and returns a BlobStorageService instance to fetch and save release notes.
       This function handles the creation of the storage service.
       """
    try:
        logger.info(f"Injecting Storage configuration into the BlobStorageService")
        storage_service = BlobStorageService(blob_storage_account_url, blob_storage_container_name)
        return storage_service
    except Exception as e:
        logger.error(f"Unexpected error occurred while creating the storage service: {e}")
        raise HTTPException(status_code=500, detail="Storage service initialization failed")


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



@router.post("/generate/")
async def generate_release_notes(request: SprintRequest,
                                  generator: BasicGenerator = Depends(get_generator),
                                  platform: AzureDevOpsService = Depends(get_platform),
                                  storage = Depends(get_storage_service)):
    """
    Generates release notes by fetching work items from specified sprints,
    feeding them to a language model, and returning the generated notes.
    """

    try:
        logger.info("Starting release note process...")

        # Construct the file signature based on sprint identifiers + container id
        sprints = request.sprints
        container_id = get_container_id()
        file_signature = "_".join(sprints) + "_" + container_id + ".docx"
        logging.info(f"requested file signature is: {file_signature}")

        # Try to fetch the file from storage
        doc = storage.fetch_file(file_signature)
        if doc:
            logger.info(f"File {file_signature} found in storage.")
            doc_bytes = convert_docx_to_bytes(doc)
            return StreamingResponse(BytesIO(doc_bytes), media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", headers={"Content-Disposition": f"attachment; filename={file_signature}"})

        # if the document is not found, initiate the process E2E
        logger.info(f"File {file_signature} not found in storage. starting generation... ")

        # fetch the work items associated with the sprints
        work_items = await platform.fetch_work_items_for_multiple_sprints(sprints)
        logger.info(f"Fetched {len(work_items)} work items: {[item.id for item in work_items]}")

        # Generate release notes using the language model
        logger.info("Generating release notes...")
        response = await generator.generate(work_items)
        logger.info("Release notes generated successfully.")

        # Convert the response to a DOCX file and upload to storage
        logger.info(f"Uploading {file_signature} to storage...")
        doc = convert_text_to_docx(response.title, response.content)
        if storage.save_file(doc, file_signature):
            logger.info(f"Successfully uploaded {file_signature} to storage.")
        else:
            logger.error(f"Failed to upload {file_signature} to storage.")

        # Convert the Document to bytes for response
        doc_bytes = convert_docx_to_bytes(doc)
        # print(doc_bytes)

        # Return the document as bytes in the response
        return StreamingResponse(BytesIO(doc_bytes),
                                 media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                 headers={"Content-Disposition": f"attachment; filename={file_signature}"})


    except HTTPException as e:
        logger.error(f"HTTP error during release note generation: {e}")
        raise e  # Re-raise HTTPException with the same status code

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")