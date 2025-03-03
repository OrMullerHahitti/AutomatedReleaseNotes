# import msal
# from urllib.parse import urlparse, parse_qs
# from backend.app.utils.config import azure_openai_endpoint, azure_app_tenant_id, azure_app_client_secret, azure_app_client_id, azure_app_scope
# from backend.app.utils.useful_functions import TokenResponse
# import jwt  # PyJWT for decoding JWT tokens
#
#
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
#
#
#
# get_token_delegated()