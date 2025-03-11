# Introduction 
This is an E2E system to generate release notes for SMESH.

## Description
Automated Release Notes is a Python and JS based tool designed to automate the generation of release notes for projects. 


## Setup Environment Variables

This project requires 2 `.env` file to work correctly - AutomatedReleaseNotes/backend/.env and AutomatedReleaseNotes/frontend/.env
The files contain sensitive information and configuration settings such as API keys, database credentials, and other settings.

```
AutomatedReleaseNotes/backend/.env

AZURE_DEVOPS_ORG: The Azure DevOps organization name.
AZURE_DEVOPS_PROJECT: The name of the Azure DevOps project.
AZURE_DEVOPS_TEAM: The name of the Azure DevOps team.
AZURE_DEVOPS_REPO: The name of the Azure DevOps repository.
AZURE_DEVOPS_ITERATION_TEAM: The name of the iteration team in Azure DevOps.
AZURE_DEVOPS_PAT: Your Personal Access Token (PAT) for authenticating with Azure DevOps. This is encoded and used for API requests.

Logging Configuration:
LOGGING_LEVEL: The level of logging (e.g., INFO, DEBUG, ERROR).

Azure OpenAI Configuration:
AZURE_OPENAI_ENDPOINT: The endpoint URL for Azure OpenAI services.

Azure App Configuration:
AZURE_APP_TENANT_ID: The Tenant ID for Azure Active Directory (Azure AD).
AZURE_APP_CLIENT_SECRET: The client secret used for authenticating with Azure AD.
AZURE_APP_CLIENT_ID: The client ID of the registered Azure application.
AZURE_APP_SCOPE: The scope of the access granted for the Azure application.

Blob Storage Configuration:
BLOB_STORAGE_ACCOUNT_URL: The URL for the Azure Blob Storage account.
BLOB_STORAGE_CONTAINER_NAME: The name of the container in the Blob Storage account.

CORS Configuration:
ALLOWED_ORIGINS_DEV: The allowed origins for development environment (used for CORS settings).
ALLOWED_ORIGINS_PROD: The allowed origins for production environment (used for CORS settings).
```

``` 
AutomatedReleaseNotes/frontend/.env

REACT_APP_BASE_URL: The base URL for your API or backend service. This should be the URL where your server is hosted (e.g., http://localhost:5000 for local development or the production server URL).
REACT_APP_NOTIFICATION_TIMEOUT: The timeout duration (in milliseconds) for notifications to automatically disappear. For example, setting this to 5000 will make notifications disappear after 5 seconds.
REACT_APP_API_TIMEOUT: The timeout duration (in milliseconds) for API requests. If the backend takes longer than this value to respond, the request will be aborted. For example, 10000 means the timeout is set to 10 seconds.
REACT_APP_CONFETTI_PARTICLE_COUNT: The number of particles to display in the confetti effect. A higher value will produce more confetti particles. For example, 200 would display 200 confetti particles.
REACT_APP_CONFETTI_SPREAD: The spread of the confetti particles (in degrees). A higher value results in a wider spread. For example, 90 would spread the confetti particles over a 90-degree angle.
```

## How to Install
1. Clone the repository:
    ```sh
    git clone https://labsTLV@dev.azure.com/labsTLV/Labs_TelAviv/_git/AutomatedReleaseNotes
    cd AutomatedReleaseNotes
    git checkout fullstack-branch
    ```
2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ``` 
3. Install uvicorn:
   ```sh
    pip install uvicorn
    ```
4. Install npm (nodejs) - go to https://nodejs.org/en and follow the instructions.

5. Make sure the .env files are set up correctly.

## How to Use (locally)
1. open 2 terminals and navigate to the root directory - "AutomatedReleaseNotes" 
2. run the backend - ```uvicorn backend.app.main:app --reload --log-level debug ```
3. run the frontend - ```npm run --prefix ./frontend start```
4. Enjoy! :)

    

