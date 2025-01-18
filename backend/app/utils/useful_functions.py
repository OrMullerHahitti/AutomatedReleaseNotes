import os
from typing import List
import httpx
from azure_authentication_client import authenticate_openai
from langchain_openai import AzureChatOpenAI
from backend.app.models.models import WorkItem


def format_work_items(work_items:List[WorkItem]):
    return "\n".join(f"- {item.title}: {item.description} (Type: {item.type}, State: {item.state} , {item.id})"
                     for item in work_items)



async def make_request(url: str, method: str = 'POST', headers: dict = None, data: dict = None):
    """
    Makes an asynchronous HTTP request using the specified method.

    Args:
        url (str): The URL to which the request is made.
        method (str): The HTTP method to use for the request ('GET' or 'POST'). Defaults to 'POST'.
        headers (dict, optional): A dictionary of HTTP headers to include in the request. Defaults to None.
        data (dict, optional): A dictionary of data to include in the request body for POST requests. Defaults to None.

    Returns:
        httpx.Response: The response object from the HTTP request.

    Raises:
        ValueError: If an unsupported HTTP method is specified.
        httpx.HTTPStatusError: If the HTTP request returns an unsuccessful status code.
    """
    async with httpx.AsyncClient() as client:
        if method == 'GET':
            response = await client.get(url, headers=headers)
        elif method == 'POST':
            response = await client.post(url, headers=headers, json=data)
        else:
            raise ValueError(method)
        response.raise_for_status()
        return response

def get_azure_llm():
    api_key = authenticate_openai().api_key
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = api_key
        return AzureChatOpenAI(deployment_name="gpt-4o-deployment",
                          temperature=0.7,
                          azure_endpoint='https://function-app-open-ai-prod-apim.azure-api.net/proxy-api/')


def parse_html(html_string: str) -> str:
    soup = BeautifulSoup(html_string, 'html.parser')
    return soup.get_text()
