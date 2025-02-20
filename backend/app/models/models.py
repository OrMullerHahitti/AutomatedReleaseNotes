
import datetime

from pydantic import BaseModel,Field
import datetime as dt
from typing import Optional, Annotated, List


class DateRange(BaseModel):
    start_date: datetime.date
    end_date: datetime.date

class Commit(BaseModel):
    id: str
    date: datetime.date = Field(..., alias="datetime", example="2021-24-01")
    message: str
    status: str

class WorkItem(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    type: str
    state: str
    # assigned_to: str

class LLMResponse(BaseModel):
    ''''Document to be made from the list of work items'''


    doc_name:str=Field(..., alias="doc_name",description="name of document to be displayed",example="version_1.0.docx")
    title: str = Field(..., alias="title",description="title of document")
    content: str = Field(..., alias="content",description="the release notes content")

class Sprint(BaseModel):
    id: str | None = Field(None, alias="id")
    name: str = Field(..., alias="name")
    start_date: datetime.date = Field(..., alias="start_date", example="2021-24-01")
    finish_date: datetime.date =Field(..., alias="finish_date", example="2021-24-01")

class LLMconfig(BaseModel):
    deployment_name: str
    temperature: float
    api_key: str
    endpoint: str|None=None

#TODO: insert the correct description rules.
class TopicStructured(BaseModel):
    new_feature: List[str] = Field(default=None, alias="new_feature",description="any new feautre")
    improvement: List[str] = Field(default=None, alias="improvement",description="improvements in the existing product")
    bug_fixes: List[str] = Field(default=None, alias="bug_fixes" , description="anything related to bugs")
    test: List[str] = Field(default=None, alias="test" , description="anything related to tests")
    n_a: List[str] = Field(default=None, alias="n_a", description = "all other options + internal things")




