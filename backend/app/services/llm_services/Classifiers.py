import asyncio
from abc import ABC, abstractmethod

from langchain.chains.llm import LLMChain
from langchain.output_parsers import StructuredOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

#from backend.app.routers.LLM import work_items
from backend.app.services.azure_devops_services import AzureDevOpsService
from backend.app.services.llm_services.llm_plugs.prompts import prompt_templates
from langchain_core.prompts import PromptTemplate
from backend.app.services.llm_services.llm_plugs.prompts import *

from backend.app.models.models import TopicStructured
from backend.app.utils.useful_functions import get_azure_llm, format_work_items


class Classifier(ABC):
    def __init__(self,llm,text:str,template:PromptTemplate=prompt_templates.tagging_base_prompt):
        '''

        :param llm: a valid llm pointer
        :param text: list of parsed work items
        :param template: PromptTemplate object from langchain_core.prompts
        '''
        self.llm=llm
        self.text=text
        self. template=template

    @abstractmethod
    def classify(self) -> TopicStructured:
        pass


class BaseClassifer(Classifier):
    def __init__(self, llm, text: str, template: PromptTemplate = prompt_templates.tagging_base_prompt):
        super().__init__(llm, text, template)

    async def classify(self):
        """
        Given the following text:
        {input}

        Tag the data into structured categories. Provide the output as a JSON object with keys as categories and values as the relevant information.
        """
        # Create a parser for TopicStructured
        llm_structured = self.llm.with_structured_output(TopicStructured)


        # chain = (
        #         {"input": RunnablePassthrough()}
        #         | self.template
        #         | llm_structured
        #TODO prompy_templates.tagging_base_prompt is in the llm plugs you can change it there and just run the module
        return await llm_structured.ainvoke(f'{prompt_templates.tagging_base_prompt} use this text :{self.text}')




        # Run the chain
if __name__ == "__main__":
    async def test_classifier():
        llm=get_azure_llm()
        platform = AzureDevOpsService()
        work_items =await platform.fetch_work_items_for_multiple_sprints(["Sprint 30", "Sprint 31"])
        work_items_str = format_work_items(work_items)
        classifier=BaseClassifer(llm,work_items_str)
        text = await classifier.classify()
        print(text)
    asyncio.run(test_classifier())
