from typing import List

from backend.app.models.models import WorkItem


def format_work_items(work_items:List[WorkItem]):
    return "\n".join(f"- {item.title}: {item.description} (Type: {item.type}, State: {item.state} , {item.id})"
                     for item in work_items)