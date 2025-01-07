from azure_authentication_client import authenticate_openai
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import AzureChatOpenAI
api_key=authenticate_openai().api_key
from openai import OpenAI, azure_endpoint

print(api_key)
#'https://function-app-open-ai-prod-apim.azure-api.net/proxy-api/',
llm = AzureChatOpenAI(deployment_name="gpt-4o-deployment", temperature=0,api_key=api_key,azure_endpoint='https://function-app-open-ai-prod-apim.azure-api.net/proxy-api/')

test_prompt = PromptTemplate(
    input_variables=["work_items"],
    template="""
                -prompt here-
                """
)

release_notes = format_chain.run(summary=summary, format=release_note_format)

