
from typing import List
from azure_authentication_client import authenticate_openai
from langchain.chat_models import AzureChatOpenAI
from backend.app.models.base_service import BasePlatform
from backend.app.services.generating_policies import DefaultGenerator

from backend.app.models.base_service import BaseGenerator
from backend.app.services.azure_devops_services import AzureDevOpsService

#from backend.app.utils.config import summarize_prompt_text, format_prompt_text, release_notes_prompt_text



api_key = authenticate_openai().api_key

llm =AzureChatOpenAI(deployment_name= "gpt-4o-deployment",
                               temperature=0.7,
                               api_key=api_key,
                               azure_endpoint='https://function-app-open-ai-prod-apim.azure-api.net/proxy-api/')

async def generate_doc(sprints:List[str],generator:BaseGenerator = DefaultGenerator(llm),platform:BasePlatform=AzureDevOpsService()) -> Document:
    """
    Generates release notes for a given list of sprints using the specified generator.

    :param sprints: A list of sprints to generate release notes for.
    :param generator: The generator to use for generating release notes.
    :param platform: The platform to fetch work items from.
    :return: A Document object containing the generated release notes.
    """
    work_items = await platform.fetch_work_items_for_multiple_sprints(sprints)


    response = await generator.generate_doc(work_items)





