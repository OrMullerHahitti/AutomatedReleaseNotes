from typing import List, Any, Dict

from langchain_core.prompts import PromptTemplate
from sqlalchemy.sql.schema import DefaultGenerator


from app.models.base_service import BaseGenerator
from app.models.models import WorkItem


class DefaultGenerator(BaseGenerator):
    '''Default policy for generating release notes'''
    def __init__(self, format_text: PromptTemplate):
        super().__init__(format_text)


