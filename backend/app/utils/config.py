# backend/app/utils/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


azure_devops_org = os.getenv('AZURE_DEVOPS_ORG')
azure_devops_pat = os.getenv('AZURE_DEVOPS_PAT')
azure_devops_project = os.getenv('AZURE_DEVOPS_PROJECT')
azure_devops_team = os.getenv('AZURE_DEVOPS_TEAM')
llm_api_url = os.getenv('LLM_API_URL')
llm_api_key = os.getenv('LLM_API_KEY')