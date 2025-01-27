
from backend.app.services.storage_services import SharePoint_Storage_Service

#Secrets
secrets = {
    "username": "",
    "password": ""
}

site_url = "https://ts.accenture.com/sites/CoreTeam-SoftwareEngineering/"
folder_url = "/sites/CoreTeam-SoftwareEngineering/Shared Documents/ARN" #
test = SharePoint_Storage_Service(site_url,folder_url,secrets)





# Good documentation here!!!!! https://pypi.org/project/Office365-REST-Python-Client/
# Consider Interactive login for the testing






# you need to use OAuth authentication (through MSAL or client credentials flow), or App-only authentication.
"""

When authenticating with SharePoint, there are several different methods that you can use, depending on your setup and the type of application you're building. Each method has its own use cases and requirements. Below are the most common authentication methods available when working with SharePoint:

1. Basic Authentication (Username and Password)
Description: The simplest form of authentication. The client provides a username and password, and these are sent in the request header.
Use Case: Typically used for quick, internal applications or scripts where security is not the primary concern. It is not recommended for production applications, especially if sensitive data is involved.
How to do it:
The office365-sharepoint library supports basic authentication via the with_credentials method, as you have seen in your code (username and password).

Example:

python
Copy
context = ClientContext(site_url).with_credentials("username", "password")
2. OAuth Authentication (Client ID and Client Secret)
Description: OAuth is a token-based authentication system, and it is the recommended method for authenticating against SharePoint in production. It is more secure and avoids sending passwords in plain text.
Use Case: Used for cloud-based applications, particularly for web apps, mobile apps, and automated services. Often requires registering your app in Azure Active Directory (AAD) to obtain the client_id and client_secret.
How to do it:
Register your app in Azure Active Directory to obtain the client_id, client_secret, and tenant_id.
Use these credentials to authenticate via OAuth.
Use the ClientContext to authenticate with OAuth.
Example:
python
Copy
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.auth.authentication_context import AuthenticationContext

# Set up your app's details
client_id = "your_client_id"
client_secret = "your_client_secret"
tenant_id = "your_tenant_id"
site_url = "https://yourdomain.sharepoint.com/sites/yoursite"

# Authentication context for OAuth
auth_context = AuthenticationContext(site_url)
if auth_context.acquire_token_for_app(client_id, client_secret, tenant_id):
    context = ClientContext(site_url, auth_context)
else:
    print("Authentication failed!")
3. Interactive Authentication (Browser-based)
Description: This method uses a browser-based dialog to authenticate. It is often used for scenarios where the user needs to manually log in interactively.
Use Case: Common in scenarios where you want a user to authenticate via their own credentials in a web browser (e.g., for personal applications or testing environments).
How to do it:
The Office365-REST-Python-Client library supports this via the InteractiveBrowser class, which opens a browser window for the user to authenticate.
Example:
python
Copy
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.auth.authentication_context import AuthenticationContext
from office365.sharepoint.auth.auth_context import InteractiveBrowser

site_url = "https://yourdomain.sharepoint.com/sites/yoursite"

context = ClientContext(site_url).with_credentials(InteractiveBrowser())
4. Azure AD Token-based Authentication (Bearer Token)
Description: This method uses an OAuth access token (Bearer Token) for authentication. The token is acquired through an OAuth flow (using the client_id, client_secret, and tenant_id).

Use Case: This is suitable for production, especially for web or cloud applications that need access to SharePoint resources securely. It is typically used in scenarios with more stringent security requirements (like API-to-API communication).

How to do it:

Acquire a bearer token from Azure Active Directory using client_id, client_secret, and tenant_id.
Use the bearer token in the Authorization header of requests to SharePoint.
Example (getting an OAuth token):

python
Copy
import requests

# Details of your app registration in Azure AD
tenant_id = "your_tenant_id"
client_id = "your_client_id"
client_secret = "your_client_secret"

# Token request URL
token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': 'https://graph.microsoft.com/.default'
}

response = requests.post(token_url, headers=headers, data=data)
token = response.json().get("access_token")

# Use the access token in your requests to SharePoint
headers = {
    'Authorization': f'Bearer {token}'
}
response = requests.get("https://yourdomain.sharepoint.com/sites/yoursite/_api/web", headers=headers)
print(response.json())
5. SharePoint App-Only Authentication (Client ID and App-Only Token)
Description: This is a specific form of OAuth authentication for SharePoint apps that allows access without a user's context, using just the app’s credentials.
Use Case: Typically used for background services or daemons that need to access SharePoint without user involvement (app-only permissions).
How to do it:
Register an app in SharePoint (using Azure AD or directly in SharePoint).
Use app-only permissions to authenticate via client credentials.
Example (OAuth with App-Only token):
python
Copy
from office365.sharepoint.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext

client_id = "your_client_id"
client_secret = "your_client_secret"
site_url = "https://yourdomain.sharepoint.com/sites/yoursite"

context = ClientContext(site_url).with_credentials(client_id, client_secret)
6. Certificate-Based Authentication
Description: Certificate-based authentication allows a more secure way to authenticate by using a certificate (public/private key pair) rather than a client secret.

Use Case: Typically used in enterprise scenarios for applications that require a high level of security and cannot rely on client secrets.

How to do it:

Register your application in Azure AD.
Use a certificate for authentication.
Example:

python
Copy
from office365.sharepoint.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext

# Certificate-based authentication (using a private key file)
tenant_id = "your_tenant_id"
client_id = "your_client_id"
certificate_path = "path_to_certificate.pfx"
certificate_password = "your_certificate_password"

context = AuthenticationContext(site_url)
context.acquire_token_for_app_using_cert(client_id, tenant_id, certificate_path, certificate_password)
context = ClientContext(site_url, context)
Summary of Authentication Methods:
Authentication Method	Use Case	How to Implement
Basic Authentication	Quick, internal apps, testing.	with_credentials(username, password)
OAuth (Client ID & Secret)	Production apps, secure cloud-based apps.	Use AuthenticationContext with client credentials.
Interactive Authentication	User-driven apps that require manual login.	Use InteractiveBrowser to open a browser window for login.
Bearer Token (Azure AD Token)	Apps needing secure access without user context.	Get token using client credentials and use it in the Authorization header.
App-Only Authentication	Background services accessing SharePoint resources.	Use app credentials (client ID/secret) for access.
Certificate-Based Authentication	High-security apps requiring a certificate.	Use certificate with Azure AD or SharePoint for authentication.

"""