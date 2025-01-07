
from typing import List
from azure_authentication_client import authenticate_openai
from fastapi import FastAPI, HTTPException
from langchain.chat_models import AzureChatOpenAI
from pydantic import BaseModel, Field
from langchain.llms import OpenAI, HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from backend.app.models.models import WorkItem
from backend.app.utils.getters import get_llm
#from backend.app.utils.config import summarize_prompt_text, format_prompt_text, release_notes_prompt_text



async def generate_doc(work_items: List[WorkItem]):
    '''Generate release notes based on the provided work items
    Args:
        work_items (List[WorkItem]): List of work items to generate release notes from'''

    try:
        # Convert list of Workitems into nested dictionary
        # Example: {'item1' : {'id' : 123 , 'title': "test" ,'description' = 'test', 'type': 'user story' , 'state': "Closed"}}
        work_items_nested_dict = {
            f"item{index}": {'id': item.id, 'title': item.title, 'description': item.description, 'type': item.type,
                             'state': item.state} for index, item in enumerate(work_items)}

        summarize_prompt = PromptTemplate(
            input_variables=["work_items"],
            template=summarize_prompt_text
        )



        # Combine chains into a sequential chain with manual input for the second step
        work_items_text = "\n".join(
            f"- {item['title']}: {item.get('description', 'No description')} (Type: {item.get('type', 'N/A')})"
            for item in work_items_nested_dict  # Changed to work_items_nested_dict here
        )

        summarize_chain = LLMChain(llm=llm, prompt=summarize_prompt)
        summary = summarize_chain.run(work_items=work_items_text)



        # Step 2: Format Release Notes with a Given Format
        format_prompt = PromptTemplate(
            input_variables=["summary", "format"],
            template=summarize_prompt_text
        )
        format_chain = LLMChain(llm=llm, prompt=format_prompt)


        release_notes = format_chain.run(summary=summary, format=release_notes_prompt_text)

        return release_notes

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


