import os
from typing import List
import httpx
from azure_authentication_client import authenticate_openai
from langchain_openai import AzureChatOpenAI
from backend.app.models.models import WorkItem
from bs4 import BeautifulSoup
from docx import Document
from io import BytesIO



# import certifi
# import json
# import urllib.request
# import urllib.parse
# from backend.app.utils.config import azure_openai_endpoint, azure_app_tenant_id, azure_app_client_secret, azure_app_client_id, azure_app_scope
# import msal
# import requests
# from urllib.parse import urlparse, parse_qs
# import jwt


# <<<<<<< HEAD
# =======
from backend.app.utils.token_getter_llm import get_token_urlib
# >>>>>>> 20d549765888f3e22fe62d31f2ac15bcf9043a41


def format_work_items(work_items:List[WorkItem]):
    return "\n".join(f"- {item.title}: {item.description} (Type: {item.type}, State: {item.state} , {item.id})"
                     for item in work_items)

def format_work_items_light(work_items:List[WorkItem]):
    return "\n".join(f"{item.title}"
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
            response = await client.get(url, headers=headers, follow_redirects=False)
        elif method == 'POST':
            response = await client.post(url, headers=headers, json=data)
        else:
            raise ValueError(method)
        response.raise_for_status()
        return response
def get_azure_llm():
    api_key = get_token_urlib()
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = api_key
    return AzureChatOpenAI(
        deployment_name="gpt-4o-deployment",
        temperature=0.7,
        azure_endpoint="https://function-app-open-ai-prod-apim.azure-api.net/proxy-api/"
    )
# llm = get_azure_llm()
# print("sop")

def parse_html(html_string: str) -> str:
    soup = BeautifulSoup(html_string, 'html.parser')
    return soup.get_text()



def convert_text_to_docx(title: str , content: str) -> Document:

    """
        Converts the given text content into a Word document with a title and content.

        Args:
        - title (str): The title of the document.
        - content (str): The content to be included in the document.

        Returns:
        - Document: A python-docx Document object containing the title and content.
    """
    doc = Document()
    doc.add_heading(title, level=1) # Add the title
    doc.add_paragraph(content) # Add the generated release note content
    return doc
import pickle

def save_object_to_pickle(data, filename):
    """Saves a dictionary to a pickle file."""
    with open(filename, 'wb') as f:  # 'wb' for binary write
        pickle.dump(data, f)

def load_dict_from_pickle(filename):
    """Loads a dictionary from a pickle file."""
    with open(filename, 'rb') as f:  # 'rb' for binary read
        return pickle.load(f)

def convert_docx_to_text(doc: Document) -> str:
    """
        Extracts all text from the given Document object.

        Args:
        - doc (Document): The Document object to extract text from.

        Returns:
        - str: The extracted text as a single string.
        """
    # Initialize an empty string to hold all text
    full_text = []

    # Loop through all paragraphs in the document
    for para in doc.paragraphs:

        full_text.append(para.text)

    # Join all the paragraphs into one string
    document_text = '\n'.join(full_text)

    return document_text


def convert_docx_to_bytes(doc: Document) -> bytes:
    """Converts a `Document` object to bytes."""
    byte_io = BytesIO()
    doc.save(byte_io)
    return byte_io.getvalue()

# class TokenResponse():
#     def __init__(self, tokenType, accessToken):
#         self.tokenType = tokenType
#         self.accessToken = accessToken


# def get_token_as_jsontoken() -> TokenResponse:
#     os.environ['SSL_CERT_FILE'] = certifi.where()
#     auth_url = f'https://login.microsoftonline.com/{azure_app_tenant_id}/oauth2/v2.0/token'  # Construct the scope as before
#     body = {'grant_type': 'client_credentials', 'client_id': azure_app_client_id,
#             'client_secret': azure_app_client_secret,
#             'scope': azure_app_scope}
#     # Encode the body to a URL-encoded format and then to bytes
#     data = urllib.parse.urlencode(body).encode('ascii')  # data must be bytes    # Set the appropriate headers
#     headers = {'Content-Type': 'application/x-www-form-urlencoded',
#                'Host': 'login.microsoftonline.com'}  # Create a Request object with the URL, data, and headers
#     req = urllib.request.Request(auth_url, data=data, headers=headers)  # Send the request and read the response
#     with urllib.request.urlopen(req) as response:
#         response_dict = json.loads(response.read().decode('utf-8'))
#         output = TokenResponse(tokenType=response_dict['token_type'], accessToken=response_dict['access_token'])
#         return output


# def get_token_delegated():
#
#     client_id = azure_app_client_id
#     client_secret = azure_app_client_secret
#     tenant_id = azure_app_tenant_id
#     redirect_uri = "http://localhost"  # For redirect URI (can be any valid URI for your app)
#     scopes = ["Files.ReadWrite", "Sites.ReadWrite.All", "User.Read"]
#
#     try:
#         # OAuth2 flow to get authorization code and access token
#         # Use ConfidentialClientApplication because you have a client secret
#         app = msal.ConfidentialClientApplication(client_id, client_credential=client_secret,
#                                                  authority=f"https://login.microsoftonline.com/{tenant_id}")
#
#         # Step 1: Get the authorization URL for the user to sign in
#         # Initiate the authorization code flow and get the auth_url (no need to unpack, it's a dict)
#         flow = app.initiate_auth_code_flow(scopes, redirect_uri=redirect_uri)
#
#         # Extract the authorization URL
#         auth_url = flow['auth_uri']
#         state = flow['state']
#
#         print(f"Go to the following URL and sign in:\n{auth_url}")
#
#         # After the user signs in, they will be redirected to the redirect_uri with a code and state in the URL
#         # Get the full redirected URL (which contains the authorization code)
#         auth_response_url = input("Paste the full redirected URL here: ")
#
#         # Step 2: Parse the URL to create the 'auth_response' dictionary
#         parsed_url = urlparse(auth_response_url)
#         query_params = parse_qs(parsed_url.query)
#
#         # Create the auth_response dictionary
#         auth_response = {key: value[0] for key, value in query_params.items()}
#
#         # Ensure the 'auth_response' dictionary contains 'code' and 'state'
#         if 'code' not in auth_response or 'state' not in auth_response:
#             print("Error: The URL does not contain the required 'code' or 'state' parameters.")
#             exit()
#
#         # Step 3: Exchange the authorization code for an access token
#         # Use the parsed code and state to continue the flow
#         result = app.acquire_token_by_auth_code_flow(auth_code_flow=flow, auth_response=auth_response)
#
#         # Check if an access token was returned
#         access_token = result.get("access_token")
#         token_type = result.get("token_type")
#         return TokenResponse(tokenType=token_type, accessToken=access_token)
#
#     except Exception as e:
#         raise Exception(f"unknown exception: {e}")


# def get_token_delegated():
#     client_id = azure_app_client_id
#     client_secret = azure_app_client_secret
#     tenant_id = azure_app_tenant_id
#     redirect_uri = "http://localhost"  # For redirect URI (can be any valid URI for your app)
#     scopes = ["Files.ReadWrite", "Sites.ReadWrite.All", "User.Read"]
#
#     try:
#         # OAuth2 flow to get authorization code and access token
#         app = msal.ConfidentialClientApplication(client_id, client_credential=client_secret,
#                                                  authority=f"https://login.microsoftonline.com/{tenant_id}")
#
#         # Step 1: Get the authorization URL for the user to sign in
#         flow = app.initiate_auth_code_flow(scopes, redirect_uri=redirect_uri)
#
#         # Extract the authorization URL
#         auth_url = flow['auth_uri']
#         state = flow['state']
#
#         print(f"Go to the following URL and sign in:\n{auth_url}")
#
#         # After the user signs in, they will be redirected to the redirect_uri with a code and state in the URL
#         auth_response_url = input("Paste the full redirected URL here: ")
#
#         # Step 2: Parse the URL to create the 'auth_response' dictionary
#         parsed_url = urlparse(auth_response_url)
#         query_params = parse_qs(parsed_url.query)
#
#         # Create the auth_response dictionary
#         auth_response = {key: value[0] for key, value in query_params.items()}
#
#         # Ensure the 'auth_response' dictionary contains 'code' and 'state'
#         if 'code' not in auth_response or 'state' not in auth_response:
#             print("Error: The URL does not contain the required 'code' or 'state' parameters.")
#             exit()
#
#         # Step 3: Exchange the authorization code for an access token
#         result = app.acquire_token_by_auth_code_flow(auth_code_flow=flow, auth_response=auth_response)
#
#         # Check if an access token was returned
#         access_token = result.get("access_token")
#         token_type = result.get("token_type")
#
#         # Decode the JWT token and print its contents
#         decoded_token = jwt.decode(access_token,
#                                    options={"verify_signature": False})  # Decoding without verifying the signature
#         print("Decoded token contents:")
#         print(decoded_token)
#
#         # To force a new token (if cached token is being reused)
#         if not access_token:
#             print("Error: No access token returned.")
#             exit()
#
#         return TokenResponse(tokenType=token_type, accessToken=access_token)
#
#     except Exception as e:
#         raise Exception(f"Unknown exception: {e}")


