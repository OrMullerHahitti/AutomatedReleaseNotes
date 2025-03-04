# app/services/base_service.py
from abc import ABC, abstractmethod
from docx import Document
from backend.app.models.models import *
from backend.app.utils.useful_functions import format_work_items
from backend.app.models.models import Sprint, WorkItem
import typing


class BasePlatform(ABC):
    def __init__(self,auth_headers):
        self.auth_headers=auth_headers

    @abstractmethod
    async def fetch_work_items(self, sprint_name: str) -> List[WorkItem]:
        pass
    @abstractmethod
    async def fetch_sprints(self) -> List[Sprint]:
        pass
    @abstractmethod
    async def fetch_work_items_for_multiple_sprints(self, sprint_names: List[str]) -> List[WorkItem]:
        pass



class BaseLLMService(ABC):
    @abstractmethod
    async def generate_response(self, work_items: list[WorkItem]) -> str:
        pass




#TODO: Advise with OR: is it generic enough?
#TODO: what will be stored - txt or docx?
#TODO: what will be the correct parameters for the functions , and return types?

class BaseStorage(ABC):

    def __init__(self,secrets):
        self.secrets = secrets # password for auth

    @abstractmethod
    async def save_file(self, doc: Document, file_name: str) -> bool:
        """
        Convert LLM response to structured text (????)
        Save the given Document object into the database or storage system.
        returns true iff file upload succeeded
        """
        pass

    @abstractmethod
    async def fetch_file(self , signature: str) -> Optional[Document]:
        """
        Fetch a file (Document object) from the storage system.
        signature = file name string to look for
        returns the Document itself or None
        """
        pass

