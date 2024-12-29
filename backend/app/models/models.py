
import datetime
from pydantic import BaseModel,Field
import datetime as dt
from typing import Optional


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

class Document(BaseModel):
    title: str = Field(..., alias="title",description="title of document")
    content: str = Field(..., alias="content",description="content of document")

class Sprint(BaseModel):
    id: str | None = Field(None, alias="id")
    name: str = Field(..., alias="name")
    start_date: datetime.date = Field(..., alias="start_date", example="2021-24-01")
    finish_date: datetime.date =Field(..., alias="finish_date", example="2021-24-01")



