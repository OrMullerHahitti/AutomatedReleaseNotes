
from io import BytesIO
from backend.app.utils.useful_functions import make_request, convert_docx_to_text, convert_text_to_docx
from fastapi import HTTPException
from backend.app.models.base_service import BaseStorage
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
from docx import Document


class SharePointStorageService(BaseStorage):
    """
    A service to interact with SharePoint for storing and retrieving Word documents.
    This class allows saving text as a .docx file and fetching the content of an existing .docx file from SharePoint.
    """

    def __init__(self, site_url: str , folder_path: str, secrets: dict):
        """
        Initializes the SharePointStorageService with site URL, folder path, and credentials.

        Args:
            site_url (str): The SharePoint site URL. example: "https://<tenant-id>/sites/<site-name>"
            folder_path (str): The folder path relative to the site where the files are stored. example: "/sites/<site-name>/Shared Documents/<folder-name>"
            secrets (dict): Dictionary containing user credentials (username and password in plain text).
        """
        # TODO: use scalable & secure authentication - Lior
        super().__init__(secrets)
        self.site_url = site_url
        self.folder_path = folder_path
        self.userCredentials = UserCredential(secrets["username"],secrets["password"])
        self.context = ClientContext(site_url).with_credentials(self.userCredentials) #Conncetion object, "Client"
        self.folder = self.context.web.get_folder_by_server_relative_url(folder_path)


    def save_file(self, file_name: str,title: str,  content: str) -> bool:
        """
       Converts the text content to a .docx file and uploads it to SharePoint.

       Args:
           file_name (str): The desired name of the file (without extension).
           title (str): The title to be used in the document.
           content (str): The text content to be converted to a .docx file.

       Returns:
           bool: True iff the file was successfully uploaded
        """
        try:

            # convert to a Document Object (docx)
            doc = convert_text_to_docx(title,content)

            # Save the document to an in-memory binary stream
            doc_stream = BytesIO()
            doc.save(doc_stream) # Save the document to the in-memory stream
            doc_stream.seek(0)  # Rewind the stream to the beginning

            # Prepare the file name (e.g., "document.docx")
            file_name = f"{file_name}.docx"

            # Upload the file to SharePoint (using the in-memory stream)
            file = self.folder.files.add(file_name, doc_stream)
            self.context.execute_query()  # Execute the request to upload the file
            return True

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file into DB: {str(e)}")


    #TODO: determine a file name schema to ensure its unique - Or
    def fetch_file(self , signature: str) -> Document:
        """
        Retrieves a file from SharePoint based on its signature (file name).
        for example: "test123.docx".

        Args:
            signature (str): The unique file name (signature) to identify the file on SharePoint.

        Returns:
            Document: A docx Document object containing the file's content.
        """
        try:
            # Get the file from SharePoint
            file = self.folder.files.get_by_url(f"{signature}")
            self.context.load(file)
            self.context.execute_query()

            # Download the file content as bytes using open_binary
            file_content = file.read()

            # Convert the byte content to a docx Document object
            byte_stream = BytesIO(file_content) # convert bytes to byte_stream
            byte_stream.seek(0) # Rewind the stream to the beginning
            doc = Document(byte_stream) # build the .docx object

            return doc

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch file from DB: {str(e)}")



