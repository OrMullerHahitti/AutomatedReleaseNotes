
from backend.app.services.azure_devops_services import AzureDevOpsService
from backend.app.utils.config import authentication_headers_azure, azure_devops_org, azure_devops_project, \
        azure_devops_team, azure_devops_iteration_team

def create_platform():
    return AzureDevOpsService(auth_headers=authentication_headers_azure,
                              azure_devops_org=azure_devops_org,
                              azure_devops_team=azure_devops_team,
                              azure_devops_project=azure_devops_project,
                              azure_devops_iteration_team=azure_devops_iteration_team)