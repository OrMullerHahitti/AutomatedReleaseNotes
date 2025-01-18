import asyncio
from typing import Any, List

from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SimpleSequentialChain

from backend.app.models.base_service import BaseGenerator
from backend.app.models.models import LLMResponse, WorkItem
from backend.app.models.llm_plugs.prompts import *
from docx import Document
from backend.app.utils.prompts.prompts import default_prompt_format
from backend.app.utils.useful_functions import get_azure_llm

class SummarizeGenerator(BaseGenerator):
    ''' Default generator for release notes.
     This generator uses LangChain to generate release notes based on a list of work items.
     The release notes are generated using a structured JSON output that includes the title, doc name, and content.
    '''
    def __init__(self,llm,system_instructions:str,summarize_format:str):
        super().__init__(llm)
        self.system_instructions=system_instructions
        self.summarize_prompt=summarize_format
        # Create a prompt template that specifies the output should be in JSON format
        self.init_prompt_summary = PromptTemplate(
            input_variables=["input"],
            template=(

                "here is what you should use: List of work items:\n{work_items}\n"
                "create a summary of the items that will later be used for release note genereation"
            )
        )


    async def generate_release_notes(self,llm, work_items: List[WorkItem]) :
        """
           Creates a DOCX release note using LangChain and OpenAI.
           Automatically generates the title, doc name, and release note content from structured JSON output.

           :param system_instructions: Instructions or system prompt to guide the LLM.
           :param prompt_format: The format of the prompt to provide structured JSON output.
           :param work_items: A long string containing the list of work items.
           """
        release_note_prompt = PromptTemplate(
            input_variables=["summary"],
            template="Write a release Notes for this summary: {summary}",
        )

        summary_chain = LLMChain(llm=self.llm, prompt=self.init_prompt_summary)

        release_note_chain = LLMChain(llm=self.llm, prompt=release_note_prompt)

        overall_chain = SimpleSequentialChain(chains=[summary_chain, release_note_chain])

        release_notes_before_structure =  overall_chain.invoke({"input":f'{self.system_instructions}\n{self.summarize_prompt}\n{work_items}'})

        formatted_from_example = llm.invoke(f'{release_notes_before_structure["output"]} this is your input. format it to match this example :{default_prompt_format}')

        return formatted_from_example





#TODO for next models, classification of work items and generation of release notes, more complex logic will be added



if __name__ == "__main__":
    from azure_authentication_client import authenticate_openai
    from langchain_openai import AzureChatOpenAI
    from langchain.prompts import PromptTemplate
    from backend.app.utils.useful_functions import format_work_items
    from backend.app.models.base_service import BaseGenerator
    from backend.app.services.azure_devops_services import AzureDevOpsService

    import os

    api_key = authenticate_openai().api_key
    if not os.environ.get("AZURE_OPENAI_API_KEY"):
        os.environ["AZURE_OPENAI_API_KEY"] = api_key

    # from backend.app.utils.config import summarize_prompt_text, format_prompt_text, release_notes_prompt_text

    api_key = authenticate_openai().api_key

    llm1 = AzureChatOpenAI(deployment_name="gpt-4o-deployment",
                          temperature=0.7,
                          azure_endpoint='https://function-app-open-ai-prod-apim.azure-api.net/proxy-api/')
    async def testing_one_two(language):
        test_service = AzureDevOpsService()
        work_items = await test_service.fetch_work_items_for_multiple_sprints(["sprint 30"])
        gen = SummarizeGenerator(language,system_instructions=system_insturctions.system_two,summarize_format=summarize_format.format_one)
        response = await gen.generate(work_items)
    asyncio.run(testing_one_two(llm1))




