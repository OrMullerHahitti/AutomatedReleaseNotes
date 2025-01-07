# backend/app/utils/config.py

import os
import base64
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

''
azure_devops_org = os.getenv('AZURE_DEVOPS_ORG')
azure_devops_project = os.getenv('AZURE_DEVOPS_PROJECT')
azure_devops_team = os.getenv('AZURE_DEVOPS_TEAM')
azure_devops_repo = os.getenv('AZURE_DEVOPS_REPO')
azure_devops_iteration_team = os.getenv('AZURE_DEVOPS_ITERATION_TEAM')
# llm_api_url = os.getenv('LLM_API_URL')
# llm_api_key = os.getenv('LLM_API_KEY')
# Authentication Headers
azure_devops_pat_encoded = base64.b64encode(f":{os.getenv('AZURE_DEVOPS_PAT')}".encode()).decode()
authentication_headers_azure = {
    'Authorization': f'Basic {azure_devops_pat_encoded}'
}
# Logging
log_directory_path = os.getenv('LOG_DIRECTORY_PATH')
log_file_name = os.getenv('LOG_FILE_NAME')
logging_level = os.getenv('LOGGING_LEVEL')
summarize_prompt_template = os.getenv('SUMMARIZE_PROMPT_TEMPLATE')
format_prompt_template = os.getenv('FORMAT_PROMPT_TEMPLATE')
release_notes_prompt_template = os.getenv('RELEASE_NOTES_PROMPT_TEMPLATE')
