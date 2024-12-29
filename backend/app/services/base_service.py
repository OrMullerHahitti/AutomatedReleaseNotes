# app/services/base_service.py
from abc import ABC, abstractmethod
from typing import List
from app.models.models import *


class BasePlatform(ABC):
    def __init__(self,auth_headers):
        self.auth_headers=auth_headers

    # @abstractmethod
    # async def fetch_commits(self, start_date: str, finish_date: str) -> List[Commit]:
    #     pass

    @abstractmethod
    async def fetch_work_items(self, sprint_name: str) -> List[WorkItem]:
        pass
    @abstractmethod
    async def fetch_sprints(self) -> List[Sprint]:
        pass

from abc import ABC, abstractmethod

class BaseLLMService(ABC):
    @abstractmethod
    async def generate_response(self, work_items: list[WorkItem]) -> str:
        pass