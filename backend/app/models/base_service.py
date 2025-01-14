# app/services/base_service.py
from abc import ABC, abstractmethod
from typing import List
from backend.app.models.models import *

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
    '''
    Base class for generating release notes
    '''
    def __init__(self):
        pass
    @abstractmethod
    async def generate_doc(self,prompt:str|List[str], work_items: str,system_instructions: str|None="",amount_of_invokes=1,save_memory=False)->LLMResponse:
        pass



