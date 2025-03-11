
import asyncio
from backend.app.services.azure_devops_services import AzureDevOpsService
from backend.app.utils.config import authentication_headers_azure
from backend.app.utils.useful_functions import format_work_items
from backend.app.utils.config import *



async def test1():
    azure_test = AzureDevOpsService(authentication_headers_azure, azure_devops_org,
                                    azure_devops_project, azure_devops_team, azure_devops_iteration_team)
    sprints_test = await azure_test.fetch_sprints()
    print(sprints_test)
    test = await azure_test.fetch_work_items_for_multiple_sprints(["Sprint 53", "Sprint 57"])
    output = format_work_items(test)
    print(output)


asyncio.run(test1())
