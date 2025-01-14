from typing import List
from azure_authentication_client import authenticate_openai
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import AzureChatOpenAI
import asyncio
from backend.app.services.azure_devops_services import AzureDevOpsService
from backend.app.utils.useful_functions import format_work_items

# 9.11.2023: Sprint 28-31 // 9.1.2024: Sprint 32-33, // February 2024: Sprint 34,35

#TODO: add example input (as work items text) and example output (as the document)
#TODO: have the fetch_work_items support multiple sprints as parameter?


# Setup the LLM interaction
api_key=authenticate_openai().api_key
llm = AzureChatOpenAI(deployment_name="gpt-4o-deployment", temperature=0,api_key=api_key,azure_endpoint='https://function-app-open-ai-prod-apim.azure-api.net/proxy-api/')
test_prompt = PromptTemplate(
    input_variables=["work_items"],
    template="""
            Act as a Technical writer. I want you to produce documentation for the work items completed in a sprint.
            The target audience wont be highly technical, some might be security professionals, but mostly business people.
            so we want the features to talk to the business people and avoid technical terms
            
            Here is the data you should use:
            {work_items}
            
            Example output:
            
            Happy to announce the first SMESH release of FY25 with new capabilities and improved performance to support your security engagements and work!


Exciting projects are ahead of us this year, concentrating on SIEM, threat modelling, threat detection, advanced search capabilities and more!


We will be organizing a hands-on session towards the end of Q1. Let us know what you would like to hear more among these topics!


What’s new in version (v.0.11.0)


New Capabilities:


SiemBERT: Automate the classification of SIEM detection queries and descriptions, mapping them to MITRE ATT&CK techniques. The objective is to help organizations achieve more comprehensive threat coverage. (demo movie)


Advance Search: Retrieve the most relevant mitigation techniques by simply entering vulnerability description input. The tools indexes specific data sources such as Accenture policy, OWASP, web or other predefined data sources.


New Features:

· Concrete Countermeasures:

o Select between different attack frameworks – D3FEND or MITRE.

o Mark guide text to provide feedback or suggest correction.


· Reporting Engine:

o Attack Path Filtering: Enable the system to provide more relevant attack techniques and patterns given a certain CVE, through smart filtering functionality in the backend that leverages LLMs.

o See confidence level for the text to CWE result o Export and import adversarial scenario

o Expand/collapse adversarial scenario graph nodes



Performance Improvement and System Updates:

· Implemented Bron as a service, operating as a data service providing up to date cyber security data from MITRE, DEFEND, CWE, CVE etc.

· Security improvements o Cipher was strengthened.

o Log level was tuned.

o robots.txt added.

o Logout functionality added.

o Legal notice added.



Stay tuned for the upcoming features (just in few weeks' time):


o Security Advisor:

§ Enable users to choose from grounding documents based on security area

o Reporting engine:

§ Enable users to provide feedback on the query results (CWE, Pattern, technique)



We are continuously working on improving SMESH to provide value to your security engagements. As always, we appreciate your feedback to help us grow SMESH!
            
            """
)


test_chain = LLMChain(llm=llm, prompt=test_prompt)



async def get_workitems(sprint_name: str):
    azure_test = AzureDevOpsService()
    work_items = await azure_test.fetch_work_items(sprint_name)
    return work_items




# Main function that runs the chain and handles the work items
async def generate_release_notes(sprint_name: str):
    # Get work items (await because it's an async function)
    work_items = await get_workitems(sprint_name)

    # Format the work items to match the prompt template
    formatted_work_items = format_work_items(work_items)

    # Run the LLM chain with the formatted work items
    release_notes = test_chain.run(work_items=formatted_work_items)

    return release_notes


# Example usage of the function (use asyncio to run the async function)
sprint_name = "Sprint 56"
release_notes = asyncio.run(generate_release_notes(sprint_name))

print(release_notes)


examples = [
    {
        "work_items": "Who lived longer, Muhammad Ali or Alan Turing?",
        "output" : """

""",
    }

]