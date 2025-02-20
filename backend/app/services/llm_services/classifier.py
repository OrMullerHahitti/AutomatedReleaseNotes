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

        :param llm: a valid llm pointer can be anything as long as it can be invoked
        :param text: list of parsed work items :: has to be a string of work items i.e.
        :param template: a prompt template text OR a prompt template object that will be used to classify the work items given pydantic output object
        '''
        self.llm=llm
        self.text=text
        self. template=template

    @abstractmethod
    def classify(self) -> TopicStructured:
        ''' requirements for the classify method:
        1. The method should return a TopicStructured or another if wanted object that is a pydantic object'''
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

        from langchain.output_parsers import PydanticOutputParser
        from langchain_core.prompts import PromptTemplate
        parser = PydanticOutputParser(pydantic_object=TopicStructured)

        prompt_template = PromptTemplate(
            template="""
            You are an AI that classifies work items.

            Classify the following work items into one of the categories each: new_feature, improvement,bug_fixes,test,n_a

            Format the response strictly as JSON using this schema:
           {format_instructions}

            Work Item:
            {work_items}

            Respond only with JSON.
                        """,
            input_variables=["work_items"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )

        from langchain_core.pydantic_v1 import BaseModel, Field, validator
        chain = prompt_template|self.llm|parser

        #TODO prompy_templates.tagging_base_prompt is in the llm plugs you can change it there and just run the module
        return await chain.ainvoke({"work_items": self.text})




        # Run the chain
# if __name__ == "__main__":
#     async def test_classifier():
#         llm=get_azure_llm()
#         platform = AzureDevOpsService()
#         work_items =await platform.fetch_work_items_for_multiple_sprints(["Sprint 30", "Sprint 31"])
#         work_items_str = format_work_items(work_items)
#         classifier=BaseClassifer(llm,work_items_str)
#         text = await classifier.classify()
#         print(text)
#     asyncio.run(test_classifier())
