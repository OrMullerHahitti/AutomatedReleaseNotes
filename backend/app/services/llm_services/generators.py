from backend.app.models.base_service import BaseGenerator


class DefaultGenerator(BaseGenerator):
    async def generate_release_notes(self, llm, work_items):
        """
        Generate release notes from a list of WorkItems using the provided LLM.
        """
        return llm.generate_response(work_items)
