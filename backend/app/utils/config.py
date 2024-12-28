# backend/app/utils/config.py

import os
import base64
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


azure_devops_org = os.getenv('AZURE_DEVOPS_ORG')

azure_devops_project = os.getenv('AZURE_DEVOPS_PROJECT')
azure_devops_team = os.getenv('AZURE_DEVOPS_TEAM')
azure_devops_repo = os.getenv('AZURE_DEVOPS_REPO')
llm_api_url = os.getenv('LLM_API_URL')
llm_api_key = os.getenv('LLM_API_KEY')

# Authentication Headers
azure_devops_pat_encoded = base64.b64encode(f":{os.getenv('AZURE_DEVOPS_PAT')}".encode()).decode()
authentication_headers = {
    'Authorization': f'Basic {azure_devops_pat_encoded}'
}