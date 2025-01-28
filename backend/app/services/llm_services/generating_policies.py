import asyncio
from typing import List

from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SimpleSequentialChain, SequentialChain
from langchain.memory import ConversationBufferMemory

from backend.app.models.base_service import BaseGenerator
from backend.app.models.models import WorkItem, TopicStructured
from backend.app.services.llm_services.Classifiers import BaseClassifer
from backend.app.services.llm_services.llm_plugs.prompts import *
from backend.app.services.llm_services.llm_plugs import *
from backend.app.models.base_service import BaseGenerator
from backend.app.services.llm_services.llm_utils import generate_release_notes_paragraphs
from backend.app.utils.useful_functions import format_work_items
from backend.app.services.llm_services.llm_plugs.prompts import paragraph_examples as example_outputs


class DefaultGenerator(BaseGenerator):
    async def generate_release_notes(self, llm, work_items):
        """
        Generate release notes from a list of WorkItems using the provided LLM.
        """
        return llm.generate_response(work_items)
class BasicGenerator(BaseGenerator):
    ''' Default generator for release notes.
     This generator uses LangChain to generate release notes based on a list of work items.
     The release notes are generated using a structured JSON output that includes the title, doc name, and content.
    '''
    def __init__(self,llm):
        super().__init__(llm)


    async def generate_release_notes(self,llm, work_items: str) :
        """
           Creates a DOCX release note using LangChain and OpenAI.
           Automatically generates the title, doc name, and release note content from structured JSON output.

           :param system_instructions: Instructions or system prompt to guide the LLM.
           :param prompt_format: The format of the prompt to provide structured JSON output.
           :param work_items: A long string containing the list of work items.
           """
        classifier = BaseClassifer(llm, work_items)
        topics = await classifier.classify()
        rn_content = await generate_release_notes_paragraphs(llm,topic_data=topics,system_instructions=[system_insturctions.system_two],example_outputs=example_outputs)
        return rn_content


class LabelingGeneratorWithPredefinedClasses(BaseGenerator):
    ''' Default generator for release notes.
     This generator uses LangChain to generate release notes based on a list of work items.
     The release notes are generated using a structured JSON output that includes the title, doc name, and content.
    '''
    def __init__(self,llm,system_instructions:str,labeling_format:str):
        super().__init__(llm)
        self.system_instructions=system_instructions
        self.labeling_format=labeling_format
        # Create a prompt template that specifies the output should be in JSON format
        self.init_prompt_labeling = prompt_templates.tagging_prompt


    async def generate_release_notes(self,llm, work_items: List[WorkItem]) :
        """
           Creates a DOCX release note using LangChain and OpenAI.
           Automatically generates the title, doc name, and release note content from structured JSON output.

           :param system_instructions: Instructions or system prompt to guide the LLM.
           :param prompt_format: The format of the prompt to provide structured JSON output.
           :param work_items: A long string containing the list of work items.
           """

        memory = ConversationBufferMemory(memory_key="history", input_key="text")

        # Step 1: Tag the data
        tagging_prompt = prompt_templates.tagging_prompt
        tagging_chain = LLMChain(llm=llm, prompt=tagging_prompt, output_key="tags")

        # Step 2: Summarize the data using the categories
        summarization_prompt = PromptTemplate(
            input_variables=["tags"],
            template="Given the following categorized data:\n{tags}\n\nSummarize the information into a concise paragraph."
        )
        summarization_chain = LLMChain(llm=llm, prompt=summarization_prompt, output_key="summary")

        # Step 3: Create release notes based on the summary
        release_notes_prompt = PromptTemplate(
            input_variables=["summary"],
            template="Create release notes in the following format based on this summary:\n{summary}\n\n"
                     "Format:\n- Title:\n- Key Updates:\n- Additional Notes:"
        )
        release_notes_chain = LLMChain(llm=llm, prompt=release_notes_prompt, output_key="release_notes")

        chain = SequentialChain(
            memory=memory,
            chains=[tagging_chain, summarization_chain, release_notes_chain],
            input_variables=["text"],
            output_variables=["release_notes"],  # Final output
            verbose=True  # To see intermediate steps
        )
        formatted = chain.invoke({"input": f'{work_items}'})
        return formatted



#TODO for next models, classification of work items and generation of release notes, more complex logic will be added



if __name__ == "__main__":
    from azure_authentication_client import authenticate_openai
    from langchain_openai import AzureChatOpenAI
    from langchain.prompts import PromptTemplate
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
        work_items = await test_service.fetch_work_items_for_multiple_sprints(["Sprint 30", "Sprint 31"])
        gen = BasicGenerator(llm1)
        response = await gen.generate(work_items)
        print(response)
    asyncio.run(testing_one_two(llm1))
    print("hold")




