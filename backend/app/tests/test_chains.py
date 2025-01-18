import asyncio

from backend.app.services.azure_devops_services import AzureDevOpsService
from backend.app.services.llm_services.generating_policies import DefaultGenerator
from backend.config.config_functions import get_azure_llm
async def test1():

    llm = get_azure_llm()

    gen = DefaultGenerator()
    platform = AzureDevOpsService()
    work_items= await platform.fetch_work_items_for_multiple_sprints(["sprint 56"])
    response = await gen.generate(llm, work_items)
    return response
if __name__ == "__main__":

    asyncio.run(test1())