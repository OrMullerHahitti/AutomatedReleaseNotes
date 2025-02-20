import asyncio
import json
from typing import List
from urllib import response

from langchain.chains.llm import LLMChain

from backend.app.models.models import TopicStructured, WorkItem, LLMResponse
from backend.app.services.llm_services.llm_plugs.prompts import paragraphGeneration, FinalAssembly, paragraph_examples
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage




def return_structured_json(input_:str,llm,template,structure) -> json:
    """
    Given the following text:
    {input}

    Tag the data into structured categories. Provide the output as a JSON object with keys as categories and values as the relevant information.
    """
    structured = llm.with_structured_output(structure)
    tagging_chain = LLMChain(llm=llm, prompt=template, output_key="tags")
    return tagging_chain.invoke({"input":input_}).json()

def build_paragraph_chain(llm_pointer, use_memory: bool = False) -> LLMChain:
    """
    Builds a chain that generates a single paragraph for a specific topic.
    """
    prompt_template = PromptTemplate(
        template=paragraphGeneration.prompt_one,
        input_variables=["work_items", "topic_name"],
    )

    memory = ConversationBufferMemory(
        # By default, it expects just one input key.
        # You can specify which input key to focus on, for example:
        input_key="work_items",  # or "topic_name"
        return_messages=True
    ) if use_memory else None
    llm_chain = LLMChain(
        llm=llm_pointer,
        prompt=prompt_template,
        verbose=True,
        memory=memory
    )

    return llm_chain
def build_final_assembly_chain(llm_pointer,example_final_doc,use_memory: bool = False) -> LLMChain:
    """
    Builds a chain that assembles all paragraphs into a final release notes JSON.
    """
    prompt_str = FinalAssembly.prompt_one.replace("{example_final_docs}", example_final_doc)

    prompt_template = PromptTemplate(
        template=prompt_str,
        input_variables=["paragraphs", "system_instructions"],
    )

    memory = ConversationBufferMemory(
        # By default, it expects just one input key.
        # You can specify which input key to focus on, for example:
        input_key="paragraphs",  # or "topic_name"
        return_messages=True
    ) if use_memory else None

    final_chain = LLMChain(
        llm=llm_pointer,
        prompt=prompt_template,
        verbose=True,
        memory=memory
    )

    return final_chain

async def generate_release_notes_paragraphs(
        llm,
    topic_data: TopicStructured,
    example_outputs: List[str],
    system_instructions: List[str],
    use_memory: bool = False
) -> LLMResponse:
    """
    Generates the final LLMResponse (release notes) using a multi-step approach. given a list of work items in a topic structure.
    """

    # Convert the list of work items into a string (for example)
    paragraphs_promises = []

    # Build chains
    for key,value in topic_data.model_dump().items():
        paragraph_chain = build_paragraph_chain(llm, use_memory=True)
        paragraphs_promises.append(paragraph_chain.ainvoke(input={"work_items" : str(value), "topic_name" : key}))


    paragraphs = await asyncio.gather(*paragraphs_promises)

    # paragraphs will be a list of strings once all calls have completed
    paragraph_examples_str = "\n".join([f"Example Paragraph {i+1}: {ex}" for i, ex in enumerate(example_outputs)])

    # Step 6: Assemble final doc
    final_chain = build_final_assembly_chain(llm,paragraph_examples_str, use_memory)

    # Combine system instructions into a single string
    system_instructions_str = "\n".join(system_instructions)

    paragraphs_str = "\n".join(paragraphs['text'] for paragraphs in paragraphs)

    final_response = await final_chain.ainvoke(input={
        "paragraphs":paragraphs_str,
        "system_instructions":system_instructions_str
    }
    )
    return final_response
# if __name__ == "__main__":


