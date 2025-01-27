
import asyncio
import io
from backend.app.utils.useful_functions import make_request, convert_docx_to_text, convert_text_to_docx
from backend.app.models.models import *
from backend.app.utils.config import *
from fastapi import HTTPException #TODO: is this import needed???
from backend.app.models.base_service import BaseStorage
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from docx import Document


#TODO: tell Or - it is better LLM will return text and here will be the DOCX formation, for consistency and abstract

class SharePoint_Storage_Service(BaseStorage):
    def __init__(self, site_url: str , folder_url: str, secrets: dict):
        super().__init__(secrets)
        self.site_url = site_url # sharepoint url , i.e. https://yourdomain.sharepoint.com/sites/yoursite
        self.folder_url = folder_url # "/sites/yoursite/Shared Documents/Folder"
        self.context = ClientContext(site_url).with_credentials(secrets['username'], secrets['password']) #Conncetion object, "Client"
        self.folder = self.context.web.get_folder_by_server_relative_url(folder_url)
        print("success")


    async def save_file(self, content: str , title: str) -> bool:
        """
                Convert the text to docx format and upload to SharePoint.

                Args:
                - doc (str): Text content of the document.
                - file_name (str): The name of the file to be saved (e.g., "document.docx").
        """
        try:

            # convert to a Document Object (docx)
            doc = convert_text_to_docx(title,content)

            # Save the document to an in-memory binary stream
            doc_stream = io.BytesIO()
            doc.save(doc_stream) # Save the document to the in-memory stream
            doc_stream.seek(0)  # Rewind the stream to the beginning

            # Prepare the file name (e.g., "document.docx")
            file_name = f"{title}.docx"

            # Upload the file to SharePoint (using the in-memory stream)
            file = self.folder.files.add(file_name, doc_stream)
            await self.context.execute_query()  # Execute the request to upload the file

            # Check if the file object exists and has a valid ID to confirm successful upload
            if file and file.properties.get("Id"):
                print("File uploaded successfully")
                return True
            else:
                print("File upload failed")
                return False

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file into DB: {str(e)}")



    async def fetch_file(self , signature: str) -> str:
        """
        Given a file name signature,
        this function returns the contents of an existing file.
        """
        try:
            # Get the file from SharePoint
            file = self.folder.files.get_by_url(f"{signature}")
            await self.context.load(file)
            await self.context.execute_query()

            # Download the file content as bytes
            file_content = file.content  # This is a byte stream

            # Convert the byte content to a docx Document object
            doc = Document(io.BytesIO(file_content))

            output = convert_docx_to_text(doc)
            return output

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch file from DB: {str(e)}")







