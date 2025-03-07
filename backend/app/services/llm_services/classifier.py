from abc import ABC, abstractmethod

from backend.app.services.llm_services.prompts import *
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from backend.app.models.models import TopicStructured


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


        parser = PydanticOutputParser(pydantic_object=TopicStructured)

        prompt_template = PromptTemplate(
            template=classifiy_prompt,
            input_variables=["work_items"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )
        chain = prompt_template|self.llm|parser
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
