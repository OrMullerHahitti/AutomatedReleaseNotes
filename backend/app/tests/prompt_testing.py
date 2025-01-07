from fastapi import APIRouter, HTTPException
from langchain.chains.llm import LLMChain
from langchain_community.chat_models import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate

from backend.app.models.models import Document
import logging
from azure_authentication_client import authenticate_openai


api_key = authenticate_openai().api_key

llm =AzureChatOpenAI(deployment_name= "gpt-4o-deployment",
                               temperature=0.7,
                               api_key=api_key,
                               azure_endpoint='https://function-app-open-ai-prod-apim.azure-api.net/proxy-api/')
summarize_prompt = PromptTemplate(
            input_variables=["work_items"],
            template="""
            Here is a list of work items:
            {work_items}

            Summarize them into short, categorized notes for release:
            """
        )
summarize_chain = LLMChain(llm=llm, prompt=summarize_prompt)

# Step 2: Format Release Notes with a Given Format
format_prompt = PromptTemplate(
    input_variables=["summary", "format"],
    template="""
    Use the following format to structure the summary into release notes:

    Format:
    {format}

    Summary:
    {summary}
    """
)
format_chain = LLMChain(llm=llm, prompt=format_prompt)

# # Combine chains into a sequential chain with manual input for the second step
# work_items_text = "\n".join(
#     f"- {item['title']}: {item.get('description', 'No description')} (Type: {item.get('type', 'N/A')})"
#     for item in work_items
# )

# Step 1: Summarize the work items

summary = summarize_chain.run(work_items=work_items_text)

# Step 2: Use the summary with the custom format
release_note_format = """
Release Notes:

- **{category}**:
  {details}

Best regards,
Your Development Team
"""
release_notes = format_chain.run(summary=summary, format=release_note_format)


