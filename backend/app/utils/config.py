# backend/app/utils/config.py

import os
import base64
from dotenv import load_dotenv
import json


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


# # Load prompts from JSON config
# def load_prompts_from_json(file_path: str):
#     with open (file_path , 'r') as file:
#         return json.load(file)
#
# # the prompts are located by default at config/prompts.json
# prompts = load_prompts_from_json('prompts.json')
#
# # Access the individual prompts
# summarize_prompt_text = prompts['summarize_prompt']['template']
# format_prompt_text = prompts['format_prompt']['template']
# release_notes_prompt_text = prompts['release_notes_prompt']['template']







