# backend/app/services/langchain_llm_service.py
from app.models.models import WorkItem
from app.utils.config import llm_api_url, llm_api_key
from app.utils.requests import make_request
import logging

logger = logging.getLogger(__name__)

async def generate_response(self, work_items: list[WorkItem]) -> str:
    headers = {
        "Authorization": f"Bearer {llm_api_key}",
        "Content-Type": "application/json"
    }
    # Construct the prompt from the work items
    prompt = "\n".join([f"{item.title}: {item.description}" for item in work_items])
    payload = {
        "prompt": prompt,
        "max_tokens": 150,
        "temperature": 0.7,
        "n": 1,
        "stop": None
    }
    logger.info(f"Sending request to LLM API at {llm_api_url}")
    response = await make_request(url=llm_api_url, method='POST', headers=headers, data=payload)
    if response.status_code != 200:
        logger.error(f"LLM API error: {response.status_code} - {response.text}")
        response.raise_for_status()
    data = response.json()
    release_notes = data.get("choices", [{}])[0].get("text", "").strip()
    if not release_notes:
        release_notes = "No release notes generated."
    logger.info("Release notes generated successfully.")
    return release_notes