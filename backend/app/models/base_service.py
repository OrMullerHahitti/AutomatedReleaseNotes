# app/services/base_service.py
from abc import ABC, abstractmethod
from typing import List

from docx import Document

from backend.app.models.models import *
from backend.app.utils.useful_functions import format_work_items
from backend.app.models.models import Sprint, WorkItem


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

class BaseGenerator(ABC):
    """
    Abstract base class defining the 'generate_release_notes' interface.
    All concrete policies must implement this method.
    """
    def __init__(self,llm):
        self.llm=llm
    async def generate(self, work_items: List[WorkItem]) -> LLMResponse:
        """
        Generate release notes from a list of WorkItems using the provided LLM.
        """
        work_items= format_work_items(work_items)
        docs= await self.generate_release_notes(llm=self.llm,work_items=work_items)
        structured_llm_response = self.llm.with_structured_output(LLMResponse)

        release_notes = structured_llm_response.invoke(f'{docs} --- structure'
                                                       f'the following release note to match the structured out put to have Title, Doc name and content')

        doc = Document()

        # Add the title
        doc.add_heading(release_notes.title, level=1)

        # Add the generated release note content
        doc.add_paragraph(release_notes.content)

        # Save the document
        doc.save(f'{release_notes.doc_name}.docx' if release_notes.doc_name else "release_notes.docx")
        print(f"Release note saved to {release_notes.doc_name}")
        return release_notes

    @abstractmethod
    async def generate_release_notes(self,llm,  work_items: str) -> LLMResponse:
        """
        Generate release notes from a list of WorkItems using the provided LLM.
        """
        pass




#TODO: Advise with OR: is it generic enough?
#TODO: what will be stored - txt or docx?
#TODO: what will be the correct parameters for the functions , and return types?

class BaseStorage(ABC):

    def __init__(self,secrets):
        self.secrets = secrets # password for auth

    @abstractmethod
    async def save_file(self, file_name: str, title: str,  content: str) -> bool:
        """
        Convert LLM response to structured text (????)
        Save the given Document object into the database or storage system.
        """
        pass

    @abstractmethod
    async def fetch_file(self , signature: str) -> Document:
        """
        Fetch a file (Document object) from the storage system.
        signature = file name string to look for
        """
        pass

