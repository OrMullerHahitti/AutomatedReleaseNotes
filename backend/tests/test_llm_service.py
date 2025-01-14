from typing import List
from azure_authentication_client import authenticate_openai
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import AzureChatOpenAI
import asyncio
from app.services.azure_devops_services import AzureDevOpsService
from app.utils.useful_functions import format_work_items


# 9.11.2023: Sprint 28-31 // 9.1.2024: Sprint 32-33, // February 2024: Sprint 34,35

#TODO: add example input (as work items text) and example output (as the document)
#TODO: add few-shots learning , read about strategies , make the test easier


# Setup the LLM interaction
api_key=authenticate_openai().api_key
llm = AzureChatOpenAI(deployment_name="gpt-4o-deployment", temperature=0.5,api_key=api_key,azure_endpoint='https://function-app-open-ai-prod-apim.azure-api.net/proxy-api/')
template = """
            Act as a Technical writer. I want you to produce documentation for the work items completed in the sprints.
            The target audience wont be highly technical, some might be security professionals, but mostly business people.
            so we want the features to talk to the business people and avoid technical terms.
            
            
            
            Here is the data you should use:
            {work_items}
            
            
            Example Output:
            
            Very happy to see the increasing interest in SMESH and excitement about new capabilities!

With that said, SMESH latest release is out with new features and improved performance to support your security engagements and work!



What’s new in version 0.8.2?



New functionalities:

· Attack flow functionality is now available under Reporting Engine tab:

The feature enables automatic extraction of Attack Flow graphs from free text incident and finding reports. SMESH takes a textual description of a cyberattack scenario and autonomously generates a graphical, interoperable representation of the attack (based on the attack flow model by MITRE center of threat informed defense). View the demo here.



Periodic performance improvement and system updates:

· Improved accuracy in the Reporting Engine ‘potential attack techniques’ results, also achieved thanks to system alignment with the latest MITRE ATT&CK version – v14.



Stay tuned for the upcoming features (just in few weeks' time):


New features:

o Reporting Engine – Attack Path Filtering: Enable the system to provide more relevant attack techniques and patterns given a certain CVE, through smart filtering functionality in the backend that leverages LLMs.

o Concrete Countermeasures – User Feedback: Enable the user to mark text to provide feedback or suggest correction, which will help to improve the AI model in the backend.

o Concrete Countermeasures – CWE Mitigation Framework component: Enable user to select between different attack frameworks – D3FEND or MITRE.


We are continuously working on improving SMESH to provide value to your security engagements. As always, we appreciate your feedback to help us grow SMESH!


Stay tuned for the hands-on session, where we will provide a walkthrough of the new feature
            
            """

with open("../logs/prompt.txt" , 'w', encoding='utf-8') as prompt:
    prompt.write(template)


test_prompt = PromptTemplate(
    input_variables=["work_items"],
    template= template
)


test_chain = LLMChain(llm=llm, prompt=test_prompt)



async def get_workitems(sprint_names: List[str]):
    azure_test = AzureDevOpsService()
    work_items = await azure_test.fetch_work_items_for_multiple_sprints(sprint_names)
    return work_items




# Main function that runs the chain and handles the work items
async def generate_release_notes(sprint_list: List[str]):
    # Get work items (await because it's an async function)
    work_items = await get_workitems(sprint_list)

    # Format the work items to match the prompt template
    formatted_work_items = format_work_items(work_items)
    with open("../logs/WorkItems_text", 'w', encoding='utf-8') as WorkItems_text:
        WorkItems_text.write(formatted_work_items)

    # Run the LLM chain with the formatted work items
    release_notes = test_chain.run(work_items=formatted_work_items)

    return release_notes


# Example usage of the function (use asyncio to run the async function)
sprint_names = ["Sprint 30"]
release_notes = asyncio.run(generate_release_notes(sprint_names))

with open("../logs/AI_response.txt" , 'w', encoding='utf-8') as AI_response:
    AI_response.write(release_notes)



print("Completed.")
from backend.app.services.generating_policies import DefaultGenerator

deff = DefaultGenerator(llm)



