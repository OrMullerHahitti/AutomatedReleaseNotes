from typing import List

from backend.app.models.models import LLMResponse

#TODO create the configs class that'll have the base configs for llm and for the base platform
def generate_doc(sprints: List[str],base:Configs = baseConfig) -> LLMResponse:
    """
    Generate release notes for the given sprint names.
    """
    # Get the work items for the selected sprints
    work_items = base.platform.fetch_work_items_for_multiple_sprints(sprints)

    # Generate the release notes
    release_notes = base.generator.generate_response(work_items)

    return release_notes