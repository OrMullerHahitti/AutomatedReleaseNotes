
from io import BytesIO
from backend.app.utils.useful_functions import make_request, convert_docx_to_text, convert_text_to_docx
from fastapi import HTTPException
from backend.app.models.base_service import BaseStorage
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
from docx import Document


#TODO: tell Or - it is better LLM will return text and here will be the DOCX formation, for consistency and abstract

class SharePointStorageService(BaseStorage):

    def __init__(self, site_url: str , folder_path: str, secrets: dict):
        super().__init__(secrets)
        self.site_url = site_url
        self.folder_path = folder_path
        self.userCredentials = user_credentials = UserCredential(f'{secrets["username"]}',f'{secrets["password"]}')
        self.context = ClientContext(site_url).with_credentials(self.userCredentials) #Conncetion object, "Client"
        self.folder = self.context.web.get_folder_by_server_relative_url(folder_path)


    def save_file(self, file_name: str,title: str,  content: str) -> bool:
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



    def fetch_file(self , signature: str) -> str:
        """
            Given a unique file name , a.k.a "signature",
            this function returns the contents of an existing file.
        """
        try:
            # Get the file from SharePoint
            file = self.folder.files.get_by_url(f"{signature}")
            self.context.load(file)
            self.context.execute_query()

            # Download the file content as bytes using open_binary
            file_content = file.read()

            # Convert the byte content to a docx Document object
            byte_stream = BytesIO(file_content)
            byte_stream.seek(0)

            doc = Document(byte_stream)

            output = convert_docx_to_text(doc)
            print("Output is: " + output)
            return output

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch file from DB: {str(e)}")



