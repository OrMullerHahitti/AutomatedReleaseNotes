import json

from langchain.chains.llm import LLMChain

from backend.app.models.models import TopicStructured


def return_structured_json(input:str,llm,template,structure) -> json:
    """
    Given the following text:
    {input}

    Tag the data into structured categories. Provide the output as a JSON object with keys as categories and values as the relevant information.
    """
    structured = llm.with_structured_output(structure)
    tagging_chain = LLMChain(llm=llm, prompt=template, output_key="tags")
    return tagging_chain.invoke({"input":input}).json()

