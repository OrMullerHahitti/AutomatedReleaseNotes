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
logging_level = os.getenv('LOGGING_LEVEL')
azure_openai_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
azure_app_tenant_id = os.getenv('AZURE_APP__TENANT_ID')
azure_app_client_secret = os.getenv('AZURE_APP__CLIENT_SECRET')
azure_app_client_id = os.getenv('AZURE_APP__CLIENT_ID')
azure_app_scope = os.getenv('AZURE_APP__SCOPE')
blob_storage_account_url = os.getenv('BLOB_STORAGE_ACCOUNT_URL')
blob_storage_container_name = os.getenv('BLOB_STORAGE_CONTAINER_NAME')
allowed_origins_dev = os.getenv('ALLOWED_ORIGINS_DEV')
allowed_origins_prod = os.getenv('ALLOWED_ORIGINS_PROD')



