# app/services/base_service.py
from abc import ABC, abstractmethod
from typing import List

from app.models.models import WorkItem


class BasePlatform(ABC):
    @abstractmethod
    async def fetch_commits(self, start_date: str, end_date: str) -> List[Commit]:
        pass

    @abstractmethod
    async def fetch_work_items(self) -> List[dict]:
        pass
    @abstractmethod
    async def fetch_sprints(self) -> List[Sprint]:
        pass

from abc import ABC, abstractmethod

class BaseLLMService(ABC):
    @abstractmethod
    async def generate_response(self, work_items: list[WorkItem]) -> str:
        pass