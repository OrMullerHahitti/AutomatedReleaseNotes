# backend/app/utils/config.py

import os
import base64
from dotenv import load_dotenv


# Get the absolute path of the directory where the config.py is located
config_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the .env file
dotenv_path = os.path.join(config_dir, '../../.env')

# Load the .env file
load_dotenv(dotenv_path=dotenv_path)


# Check if the environment variable is loaded properly
print(os.getenv('AZURE_DEVOPS_TEAM'))  # Debugging line

azure_devops_org = os.getenv('AZURE_DEVOPS_ORG')
azure_devops_project = os.getenv('AZURE_DEVOPS_PROJECT')
azure_devops_team = os.getenv('AZURE_DEVOPS_TEAM')
azure_devops_repo = os.getenv('AZURE_DEVOPS_REPO')
azure_devops_iteration_team = os.getenv('AZURE_DEVOPS_ITERATION_TEAM')
# Authentication Headers
azure_devops_pat_encoded = base64.b64encode(f":{os.getenv('AZURE_DEVOPS_PAT')}".encode()).decode()
authentication_headers_azure = {
    'Authorization': f'Basic {azure_devops_pat_encoded}'
}
# Logging
log_directory_path = os.getenv('LOG_DIRECTORY_PATH')
log_file_name = os.getenv('LOG_FILE_NAME')
logging_level = os.getenv('LOGGING_LEVEL')
sharepoint_site = os.getenv("SHAREPOINT_SITE")
sharepoint_folder = os.getenv("SHAREPOINT_FOLDER")
sharepoint_username = os.getenv("SHAREPOINT_USERNAME")
sharepoint_password = os.getenv("SHAREPOINT_PASSWORD")

class settings:
    def __init__(self):
        self.testa = "test!!!!!"
        self.check = azure_devops_team

testy = settings()
print(testy.check)



