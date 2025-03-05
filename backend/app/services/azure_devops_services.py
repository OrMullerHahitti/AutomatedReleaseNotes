import asyncio
from fastapi import HTTPException
from backend.app.utils.useful_functions import make_request
from backend.app.models.models import *
from backend.app.models.base_service import BasePlatform
from datetime import datetime
from backend.app.utils.useful_functions import parse_html
from backend.app.utils.config import logging_level
import logging

logging.basicConfig(level=getattr(logging, logging_level, logging.INFO))
logger = logging.getLogger(__name__)


class AzureDevOpsService(BasePlatform):
    """
    AzureDevOpsService interacts with the Azure DevOps API to fetch sprint and work item data.
    It leverages Azure DevOps REST API to pull sprint information and work item details.
    """

    def __init__(self, auth_headers, azure_devops_org, azure_devops_project,
                 azure_devops_team, azure_devops_iteration_team):
        """
        Initializes the AzureDevOpsService with necessary authentication and configuration.

        Args:
            auth_headers (dict): Headers containing authorization for Azure DevOps.
            azure_devops_org (str): The Azure DevOps organization name.
            azure_devops_project (str): The Azure DevOps project name.
            azure_devops_team (str): The Azure DevOps team name.
            azure_devops_iteration_team (str): The Azure DevOps iteration team name.
        """
        super().__init__(auth_headers)
        self.azure_devops_org = azure_devops_org
        self.azure_devops_project = azure_devops_project
        self.azure_devops_team = azure_devops_team
        self.azure_devops_iteration_team = azure_devops_iteration_team

    async def fetch_sprints(self) -> List[Sprint]:
        """
        Fetches the list of sprints for a specific team within the Azure DevOps organization.

        Returns:
            List[Sprint]: A list of Sprint objects containing sprint information.

        Raises:
            HTTPException: If an error occurs while fetching sprint data.
        """
        try:
            logger.info(f"Fetching sprints for project: {self.azure_devops_project} from Azure DevOps.")
            base_url = f'https://dev.azure.com/{self.azure_devops_org}/{self.azure_devops_project}/{self.azure_devops_team}/_apis/work/teamsettings/iterations?api-version=7.1'
            logger.info(f"Base URL for fetching sprints: {base_url}")

            response = await make_request(url=base_url, method='GET', headers=self.auth_headers)
            sprints_data = response.json()

            # Extract and map the sprints
            sprints = []
            for sprint in sprints_data.get("value", {}):
                sprint_id = sprint.get("id")
                sprint_name = sprint.get("name")
                start_date_str = sprint.get("attributes", {}).get("startDate")
                finish_date_str = sprint.get("attributes", {}).get("finishDate")

                # Convert the start and finish dates from string to datetime.date
                start_date = None
                finish_date = None
                if start_date_str:
                    start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%SZ").date()
                if finish_date_str:
                    finish_date = datetime.strptime(finish_date_str, "%Y-%m-%dT%H:%M:%SZ").date()

                # Create and append Sprint object to the list
                sprint = Sprint(
                    id=sprint_id,
                    name=sprint_name,
                    start_date=start_date,
                    finish_date=finish_date
                )
                sprints.append(sprint)

            logger.info(f"Successfully fetched {len(sprints)} sprints.")
            return sprints

        except Exception as e:
            logger.error(f"Failed to fetch sprints: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to fetch_sprints: {str(e)}")

    async def fetch_work_items(self, sprint_name: str) -> List[WorkItem]:
        """
        Fetches work items for a specific sprint in Azure DevOps.

        Args:
            sprint_name (str): The name of the sprint to fetch work items for.

        Returns:
            List[WorkItem]: A list of WorkItem objects containing work item details.

        Raises:
            HTTPException: If an error occurs while fetching work item data.
        """
        try:
            logger.info(f"Fetching work items for sprint: {sprint_name}")

            # Define WIQL query to fetch all work items for the sprint
            wiql_query = {
                "query": f"""
                    SELECT [System.Id], [System.WorkItemType]
                    FROM WorkItems
                    WHERE [System.IterationPath] = '{self.azure_devops_project}\\{self.azure_devops_iteration_team}\\{sprint_name}'
                    AND [System.TeamProject] = '{self.azure_devops_project}'
                    AND [System.State] = 'Closed'
                    ORDER BY [System.Id]
                """
            }

            wiql_url = f'https://dev.azure.com/{self.azure_devops_org}/{self.azure_devops_project}/_apis/wit/wiql?api-version=7.1'
            wiql_response = await make_request(url=wiql_url, method='POST', headers=self.auth_headers, data=wiql_query)
            wiql_json_response = wiql_response.json()

            work_item_ids = [item['id'] for item in wiql_json_response['workItems']]
            logger.info(f"Detected {len(work_item_ids)} closed work items for sprint: {sprint_name}")

            # Fetch detailed work item information
            work_item_url = f'https://dev.azure.com/{self.azure_devops_org}/{self.azure_devops_project}/_apis/wit/workitems?ids={",".join(map(str, work_item_ids))}&api-version=7.1'
            work_item_response = await make_request(url=work_item_url, method='GET', headers=self.auth_headers)
            work_item_data = work_item_response.json()

            # Map the response to WorkItem models
            work_items = []
            for work_item in work_item_data['value']:
                item_id = str(work_item['id'])
                title = work_item['fields']['System.Title']
                item_type = work_item['fields']['System.WorkItemType']
                state = work_item['fields']['System.State']
                description = parse_html(work_item['fields'].get('System.Description', ''))

                item_to_add = WorkItem(id=item_id, title=title, type=item_type, state=state, description=description)
                work_items.append(item_to_add)

            logger.info(f"Successfully fetched {len(work_items)} work items for sprint: {sprint_name}.")
            return work_items

        except Exception as e:
            logger.error(f"Failed to fetch work items for sprint '{sprint_name}': {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to fetch_work_items: {str(e)}")

    async def fetch_work_items_for_multiple_sprints(self, sprint_names: List[str]) -> List[WorkItem]:
        """
        Fetches work items for multiple sprints concurrently.

        Args:
            sprint_names (List[str]): A list of sprint names to fetch work items for.

        Returns:
            List[WorkItem]: A combined list of work items from all the sprints.

        Raises:
            HTTPException: If an error occurs while fetching work item data for multiple sprints.
        """
        try:
            logger.info(f"Fetching work items for multiple sprints: {sprint_names}")

            # Create a task for each sprint
            tasks = [self.fetch_work_items(sprint_name) for sprint_name in sprint_names]

            # Run tasks concurrently using asyncio.gather
            all_work_items = await asyncio.gather(*tasks)

            # Flatten the list of work items
            flat_work_items = [item for sprint_work_items in all_work_items for item in sprint_work_items]

            logger.info(f"Successfully fetched {len(flat_work_items)} work items across {len(sprint_names)} sprints.")
            return flat_work_items

        except Exception as e:
            logger.error(f"Failed to fetch work items for multiple sprints: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to fetch_work_items for multiple sprints: {str(e)}")
