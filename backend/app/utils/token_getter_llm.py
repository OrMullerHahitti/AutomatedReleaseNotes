import json
import os

from azure_authentication_client import authenticate_openai
from cachetools.func import ttl_cache
from dotenv import load_dotenv
from backend.app.utils.config import azure_app_client_secret, azure_app_client_id, azure_app_tenant_id, azure_app_scope, azure_openai_endpoint
import urllib.request

import urllib.parse



@ttl_cache(ttl=60 * 60)
def get_token_urlib():

    import certifi

    os.environ['SSL_CERT_FILE'] = certifi.where()
    auth_url = f'https://login.microsoftonline.com/{azure_app_tenant_id}/oauth2/v2.0/token'  # Construct the scope as before
    body = {'grant_type': 'client_credentials', 'client_id': azure_app_client_id,
            'client_secret': azure_app_client_secret,
            'scope': azure_app_scope}
    # Encode the body to a URL-encoded format and then to bytes
    data = urllib.parse.urlencode(body).encode('ascii')  # data must be bytes    # Set the appropriate headers
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Host': 'login.microsoftonline.com'}  # Create a Request object with the URL, data, and headers
    req = urllib.request.Request(auth_url, data=data, headers=headers)  # Send the request and read the response
    with urllib.request.urlopen(req) as response:
        response_dict = json.loads(response.read().decode('utf-8'))
        return response_dict['access_token']


# api_key = get_token_urlib()
# print("hi")