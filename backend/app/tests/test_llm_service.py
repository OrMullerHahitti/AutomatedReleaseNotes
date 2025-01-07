from azure_authentication_client import authenticate_openai
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import AzureChatOpenAI
api_key=authenticate_openai().api_key
from openai import OpenAI, azure_endpoint

print(api_key)
#'https://function-app-open-ai-prod-apim.azure-api.net/proxy-api/',
llm = AzureChatOpenAI(deployment_name="gpt-4o-deployment", temperature=0,api_key=api_key,azure_endpoint='https://function-app-open-ai-prod-apim.azure-api.net/proxy-api/')
summarize_prompt = PromptTemplate(
    input_variables=["work_items"],
    template="""
                Here is a list of work items:
                {work_items}

                Summarize them into short, categorized notes for release:
                """
)

# TODO: how do we get the workItems here? shouldn't it be added to the QueryRequest model?

# Convert list of Workitems into nested dictionary

work_items = {
    'id': 123,
    'title': "this is a very important test",
    'description': 'the biggest test that was done',
    'type': 'user story',
    'state': "Closed"
}



# work_items_nested_dict = {
#     f"item{index}": {'id': item.id, 'title': item.title, 'description': item.description, 'type': item.type,
#                      'state': item.state} for index, item in enumerate(work_items)}

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

# TODO: fix this implementation as following work_items_nested_dict

# Combine chains into a sequential chain with manual i
work_items_text = '\n'.join([f"{key}: {value}" for key, value in work_items.items()])


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



print("jello")