
import asyncio
from app.services.azure_devops_services import AzureDevOpsService
from app.utils.config import *

async def test1():
    azure_test = AzureDevOpsService()
    # sprints_test = await azure_test.fetch_sprints()
    # await azure_test.fetch_work_items("Sprint 56")
    test = await azure_test.fetch_work_items_for_multiple_sprints(["Sprint 30" , "Sprint 31" , "Sprint 32"])


asyncio.run(test1())


