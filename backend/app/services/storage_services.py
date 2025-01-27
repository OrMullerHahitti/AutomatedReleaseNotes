
import asyncio

from backend.app.utils.useful_functions import make_request
from backend.app.models.models import *
from backend.app.utils.config import *
from fastapi import HTTPException #TODO: is this import needed???
from backend.app.models.base_service import BaseStorage
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File


#TODO: tell Or - it is better LLM will return text and here will be the DOCX formation, for consistency and abstract

class SharePoint_Storage_Service(BaseStorage):
    def __init__(self, site_url: str , folder_url: str, secrets: dict):
        super().__init__(secrets)
        self.site_url = site_url # sharepoint url , i.e. https://yourdomain.sharepoint.com/sites/yoursite
        self.folder_url = folder_url # "/sites/yoursite/Shared Documents/Folder"
        self.context = ClientContext(site_url).with_credentials(secrets) #Conncetion object, "Client"
        self.folder = self.context.web.get_folder_by_server_relative_url(folder_url)


    async def save_file(self, doc: str):
        pass



    async def fetch_file(self , signature: str) -> str:
        """
        Given a file name signature,
        this function returns the contents of an existing file.
        """
        try:
            file = self.folder.files.get_by_url(f"{signature}")
            self.context.load(file)
            self.context.execute_query()
            return file

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch file from DB: {str(e)}")







