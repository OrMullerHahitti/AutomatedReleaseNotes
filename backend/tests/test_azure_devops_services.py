
import asyncio
from backend.app.services.azure_devops_services import AzureDevOpsService
from backend.app.utils.config import *
from backend.app.utils.useful_functions import format_work_items_light

async def test1():
    azure_test = AzureDevOpsService()
    # sprints_test = await azure_test.fetch_sprints()
    # await azure_test.fetch_work_items("Sprint 56")
    test = await azure_test.fetch_work_items_for_multiple_sprints(["Sprint 53", "Sprint 57"])
    output = format_work_items_light(test)
    print(output)


asyncio.run(test1())


