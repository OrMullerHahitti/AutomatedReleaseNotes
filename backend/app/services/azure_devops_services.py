import asyncio
from typing import List
from fastapi import HTTPException
from backend.app.utils.requests import make_request
from backend.app.models.models import *
from backend.app.utils.config import *
from backend.app.utils.CustomLogger import CustomLogger
from backend.app.models.base_service import BasePlatform
from datetime import datetime


class AzureDevOpsService(BasePlatform):

    def __init__(self):
        super().__init__(authentication_headers_azure)
        self.logger = CustomLogger(log_directory_path,log_file_name,
                                   logging_level).get_logger()

    async def fetch_sprints(self) -> List[Sprint]:
        try:
            self.logger.info("fetching sprints from Azure Devops")
            base_url = f'https://dev.azure.com/{azure_devops_org}/{azure_devops_project}/{azure_devops_team}/_apis/work/teamsettings/iterations?api-version=7.1'
            response = await make_request(url=base_url, method='GET', headers=self.auth_headers)
            sprints_data = response.json()

            # Extract sprints and map them to the Sprint model
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

                # Create a Sprint model and append to the list
                sprint = Sprint(
                    id=sprint_id,
                    name=sprint_name,
                    start_date=start_date,
                    finish_date=finish_date
                )
                sprints.append(sprint)

            self.logger.info(f"Successfully fetched {len(sprints)} sprints.")
            return sprints


        except Exception as e:
            self.logger.error(f"Failed to fetch sprints: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to fetch_sprints: {str(e)}")

# from backend.app.models.models import WorkItem, Sprint
# from backend.app.utils.config import azure_devops_org, azure_devops_project, azure_devops_team, \
#     authentication_headers_azure, log_directory_path, logging_level, log_file_name


    async def fetch_work_items(self, sprint_name: str) -> List[WorkItem]:
            try:

                # Step 1: Extract the work item ids relevant to the input sprint

                # Define WIQL query to fetch all work items for the sprint
                self.logger.info(f"Fetching work items for sprint '{sprint_name}'.")
                wiql_query = {
                    "query": f"""
                        SELECT [System.Id], [System.WorkItemType]
                        FROM WorkItems
                        WHERE [System.IterationPath] = '{azure_devops_project}\\{azure_devops_iteration_team}\\{sprint_name}'
                        AND [System.TeamProject] = '{azure_devops_project}'
                        AND [System.State] = 'Closed'
                        ORDER BY [System.Id]
                    """
                }

                # URL to run the WIQL query
                wiql_url = f'https://dev.azure.com/{azure_devops_org}/{azure_devops_project}/_apis/wit/wiql?api-version=7.1'

                # Make the request to the WIQL API
                wiql_response = await make_request(url=wiql_url, method='POST', headers=self.auth_headers, data=wiql_query)
                wiql_json_response = wiql_response.json()

                # Fetch the work item identifiers
                work_item_ids = [item['id'] for item in wiql_json_response['workItems']]
                self.logger.info(f"detected {len(work_item_ids)} CLOSED workitems for the following query: \n {wiql_query}")



                # Step 2: Fetch the detailed work items information
                work_item_url = f'https://dev.azure.com/{azure_devops_org}/{azure_devops_project}/_apis/wit/workitems?ids={",".join(map(str, work_item_ids))}&api-version=7.1'
                work_item_response = await make_request(url=work_item_url, method='GET', headers=self.auth_headers)
                work_item_data = work_item_response.json()
                self.logger.info(f"Successfully fetched {len(work_item_data['value'])} work items for sprint '{sprint_name}'.")

                # Step 3: Map the response to the WorkItem model
                work_items = []
                for work_item in work_item_data['value']:
                    item_id = str(work_item['id'])
                    title = work_item['fields']['System.Title']
                    item_type = work_item['fields']['System.WorkItemType']
                    state = work_item['fields']['System.State']
                    description = work_item['fields'].get('System.Description', '')

                    # Append the work item to the list
                    item_to_add = WorkItem(id=item_id, title=title, type=item_type, state=state, description=description)
                    work_items.append(item_to_add)
                    self.logger.info(f"added: {item_to_add}")

                return work_items


            except Exception as e:
                self.logger.error(f"Failed to fetch work items for sprint '{sprint_name}': {str(e)}")
                raise HTTPException(status_code=500, detail=f"Failed to fetch_work_items: {str(e)}")






    async def fetch_work_items_for_multiple_sprints(self, sprint_names: List[str]) -> List[WorkItem]:
        try:
            # Create a task per each sprint
            tasks = [self.fetch_work_items(sprint_name) for sprint_name in sprint_names]

            # Run tasks concurrently using asyncio.gather
            all_work_items = await asyncio.gather(*tasks)

            #TODO: resolve the duplicate issue
            # all_work_item_unique = set(item.id for sprint_work_items in all_work_items for item in sprint_work_items)

            # Extract the work items from all sprints into a single list
            flat_work_items = [item for sprint_work_items in all_work_items for item in sprint_work_items]
            self.logger.info(f"Successfully fetched {len(flat_work_items)} work items from {len(sprint_names)} sprints.")

            return flat_work_items

        except Exception as e:
            self.logger.error(f"Failed to fetch work items for multiple sprints: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to fetch_work_items for multiple sprints: {str(e)}")