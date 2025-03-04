
from io import BytesIO
from typing import Optional
import logging
from backend.app.utils.config import azure_app_tenant_id, azure_app_client_id , azure_app_client_secret
from backend.app.utils.useful_functions import convert_text_to_docx
from backend.app.models.base_service import BaseStorage
from azure.storage.blob import BlobServiceClient
from azure.identity import ClientSecretCredential  # Use ClientSecretCredential directly
from docx import Document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BlobStorageService(BaseStorage):
    """
    A service to interact with Azure Blob Storage for storing and retrieving Word documents.
    This class allows saving text as a .docx file and fetching the content of an existing .docx file from Blob Storage.
    """

    def __init__(self, account_url: str, container_name: str):
        """
        Initializes the BlobStorageService with Azure Storage account URL and container name.

        Args:
            account_url (str): The URL of the Azure Blob Storage account.
            container_name (str): The container where the files are stored.
        """
        super().__init__(secrets={})  # Assuming no credentials needed, or you can handle via environment variables.

        # Use the credentials from config.py
        credential = ClientSecretCredential(
            tenant_id=azure_app_tenant_id,
            client_id=azure_app_client_id,
            client_secret=azure_app_client_secret
        )

        # Initialize the BlobServiceClient with the provided credentials
        logger.info(f"Initializing the BlobStorageObject with parameters {account_url} , {container_name}")
        self.blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)
        self.container_client = self.blob_service_client.get_container_client(container_name)

    def save_file(self, file_name: str, title: str, content: str) -> bool:
        """
        Converts the text content to a .docx file and uploads it to Azure Blob Storage.

        Args:
            file_name (str): The desired name of the file (without extension).
            title (str): The title to be used in the document.
            content (str): The text content to be converted to a .docx file.

        Returns:
            bool: True iff the file was successfully uploaded
        """
        try:
            # Convert to a Document Object (docx)
            doc = convert_text_to_docx(title, content)

            # Save the document to an in-memory binary stream
            doc_stream = BytesIO()
            doc.save(doc_stream)  # Save the document to the in-memory stream
            doc_stream.seek(0)  # Rewind the stream to the beginning

            # Prepare the blob name (e.g., "document.docx")
            file_name = f"{file_name}.docx"

            # Upload the file to Azure Blob Storage
            logger.info(f"Starting to upload {file_name} to {self.container_client.url}...")
            blob_client = self.container_client.get_blob_client(file_name)
            blob_client.upload_blob(doc_stream, overwrite=True)
            logger.info(f"Successfully uploaded {file_name} to {self.container_client.url}")

            return True

        except Exception as e:
            logger.error(f"Failed to save file to Blob Storage: {str(e)}")
            return False

    def fetch_file(self, signature: str) -> Optional[Document]:
        """
        Retrieves a file from Azure Blob Storage based on its signature (file name).

        Args:
            signature (str): The unique file name (signature) to identify the file on Blob Storage.

        Returns:
            Document: A docx Document object containing the file's content.
        """
        try:
            # Get the blob from Azure Blob Storage
            blob_client = self.container_client.get_blob_client(signature)
            download_stream = blob_client.download_blob()

            # Download the file content as bytes
            file_content = download_stream.readall()

            # Convert the byte content to a docx Document object
            byte_stream = BytesIO(file_content)  # convert bytes to byte_stream
            byte_stream.seek(0)  # Rewind the stream to the beginning
            doc = Document(byte_stream)  # build the .docx object
            return doc

        except Exception as e:
            logger.error(f"Failed to fetch file from Blob Storage: {str(e)}")
            return None


# from office365.sharepoint.client_context import ClientContext
# from office365.runtime.auth.user_credential import UserCredential
# from office365.runtime.auth.authentication_context import AuthenticationContext


# class SharePointStorageService(BaseStorage):
#     """
#     A service to interact with SharePoint for storing and retrieving Word documents.
#     This class allows saving text as a .docx file and fetching the content of an existing .docx file from SharePoint.
#     """
#
#     def __init__(self, site_url: str , folder_path: str, secrets: dict):
#         """
#         Initializes the SharePointStorageService with site URL, folder path, and credentials.
#
#         Args:
#             site_url (str): The SharePoint site URL. example: "https://<tenant-id>/sites/<site-name>"
#             folder_path (str): The folder path relative to the site where the files are stored. example: "/sites/<site-name>/Shared Documents/<folder-name>"
#             secrets (dict): Dictionary containing user credentials (username and password in plain text).
#         """
#         # TODO: use scalable & secure authentication - Lior
#         super().__init__(secrets)
#         self.site_url = site_url
#         self.folder_path = folder_path
#         # self.auth_context = AuthenticationContext(self.site_url)
#         # self.userCredentials = UserCredential(secrets["username"],secrets["password"])
#         # self.context = ClientContext(site_url).with_credentials(self.userCredentials) #Conncetion object, "Client"
#
#         # self.context = ClientContext(self.site_url).with_access_token(get_token_as_jsontoken)
#         self.context = ClientContext(self.site_url).with_access_token(get_token_delegated)
#         self.folder = self.context.web.get_folder_by_server_relative_url(folder_path)
#
#
#     def save_file(self, file_name: str,title: str,  content: str) -> bool:
#         """
#        Converts the text content to a .docx file and uploads it to SharePoint.
#
#        Args:
#            file_name (str): The desired name of the file (without extension).
#            title (str): The title to be used in the document.
#            content (str): The text content to be converted to a .docx file.
#
#        Returns:
#            bool: True iff the file was successfully uploaded
#         """
#         try:
#
#             # convert to a Document Object (docx)
#             doc = convert_text_to_docx(title,content)
#
#             # Save the document to an in-memory binary stream
#             doc_stream = BytesIO()
#             doc.save(doc_stream) # Save the document to the in-memory stream
#             doc_stream.seek(0)  # Rewind the stream to the beginning
#
#             # Prepare the file name (e.g., "document.docx")
#             file_name = f"{file_name}.docx"
#
#             # Upload the file to SharePoint (using the in-memory stream)
#             file = self.folder.files.add(file_name, doc_stream)
#             self.context.execute_query()  # Execute the request to upload the file
#             return True
#
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Failed to save file into DB: {str(e)}")
#
#
#     #TODO: determine a file name schema to ensure its unique - Or
#     def fetch_file(self , signature: str) -> Document:
#         """
#         Retrieves a file from SharePoint based on its signature (file name).
#         for example: "test123.docx".
#
#         Args:
#             signature (str): The unique file name (signature) to identify the file on SharePoint.
#
#         Returns:
#             Document: A docx Document object containing the file's content.
#         """
#         try:
#             # Get the file from SharePoint
#             file = self.folder.files.get_by_url(f"{signature}")
#             self.context.load(file)
#             self.context.execute_query()
#
#             # Download the file content as bytes using open_binary
#             file_content = file.read()
#
#             # Convert the byte content to a docx Document object
#             byte_stream = BytesIO(file_content) # convert bytes to byte_stream
#             byte_stream.seek(0) # Rewind the stream to the beginning
#             doc = Document(byte_stream) # build the .docx object
#
#             return doc
#
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Failed to fetch file from DB: {str(e)}")





