from typing import List
from azure_authentication_client import authenticate_openai
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import AzureChatOpenAI
import asyncio
from backend.app.services.azure_devops_services import AzureDevOpsService
from backend.app.utils.useful_functions import format_work_items
import csv



# Setup the LLM interaction
api_key = authenticate_openai().api_key
llm = AzureChatOpenAI(deployment_name="gpt-4o-deployment", temperature=0, api_key=api_key,
                      azure_endpoint='https://function-app-open-ai-prod-apim.azure-api.net/proxy-api/')

test_prompt = PromptTemplate(
    input_variables=["work_items"],
    template="""
            For each of the lines of text in DATA sections, classify it into one of the CATEGORIES.
            Each line of text corresponds to a task, and you need to determine the most appropriate category based on its content.
            Output format is <line>@<category>
            
            ### CATEGORIES ###
            
            #### Improvement
This category encompasses tasks aimed at enhancing existing systems, processes, or features. Key aspects include:
- Adding new functionalities or features to improve user experience or system performance.
- Refining and updating existing components to ensure consistency and efficiency.
- Implementing solutions to automate processes and reduce manual intervention.
- Enhancing the design and usability of user interfaces.
- Improving infrastructure for better deployment and resource management.
 
#### Test
This category involves tasks focused on verifying the correctness and reliability of systems and features. Key aspects include:
- Creating and executing tests to ensure the accuracy and functionality of new or existing features.
- Developing comprehensive test cases to cover various scenarios and edge cases.
- Automating tests to streamline the validation process and ensure continuous integration.
- Ensuring that intermediary steps in processes are valid and meet expected outcomes.
 
#### Bug fix
This category addresses tasks aimed at identifying, troubleshooting, and resolving issues or errors in the system. Key aspects include:
- Fixing inconsistencies and errors in user interfaces to enhance user experience.
- Resolving bugs that interfere with the functionality and performance of features.
- Ensuring that error messages and system feedback are clear and informative.
- Troubleshooting deployment issues and ensuring smooth operation of services.
 
#### New Feature
This category includes tasks focused on developing and implementing new functionalities that were not previously available. Key aspects include:
- Adding new capabilities to systems to meet user needs and requirements.
- Enabling users to perform new actions or access new data through the system.
- Enhancing the system's ability to provide feedback and improve based on user input.
- Implementing new visual components and analysis tools to aid in data interpretation and decision-making.
 
#### nan
This category includes tasks that do not fit into the other predefined categories. These tasks may involve:
- Administrative or preparatory activities, such as attending exams or preparing reviews.
- Collaborative efforts and communication with stakeholders or other teams.
- Research and exploration activities to gather information or refine content.
- Miscellaneous tasks that support overall project goals but do not directly involve system improvements, testing, bug fixing, or new feature development.

            
            ### DATA ###
            {work_items}

            """
)

test_chain = LLMChain(llm=llm, prompt=test_prompt)

test = """
As a developer, I would like to get to know all new SMESH features and cover them in SMESH tests
As a DevOps I want to pull complete billing of our resources
As a frontend developer, I would like to be able to update Reporting Engine UI to ensure great UX
As a dev, I'd like to add tests for covering correctness of the created graph
As a researcher I would like to explore the ChatGPT using ontology research (publication) so I could list this KPI as done
As a dev, I'd like to add tests along different steps in the graph creation pipeline to make sure intermediaries are valid
As a dev, I'd like to automatically verify that built graph contains the latest CVEs, CWEs and other entities
As a developer I would like to design an API so clients will be able to upload an external knowledge base to our vector data base
As a dev, I'd like to create a training pipeline for SiemBert so that it can run automatically and periodically
As a dev, I'd like to only update the parts that were changed in the BRON graph, so that I won't need to re-create the whole graph on every run
As a developer I would like to attend the certification exam
As a researcher I would like to review and refine the blog post
As a developer I would like to prepare for my azure developer associate certificate
As a frontend developer, I would like to update SMESH with the new typography elements from ui-common-design to ensure consistent design
As a DevOps I want to discuss automatic propagation of BRON to SMESH PROD
As a DevOps I'd like to further report on SMESH/Azure pricing
As a frontend developer, I want to fix inconsistencies in SMESH UI to ensure great UX
As a frontend developer I would like to see the error messages better explained from the E2E test runs
As a frontend developer, I would like to update SMESH with the new typography elements from ui-common-design to ensure consistent design
As a DevOps engineer I would like to present the E2E test to stakeholder, to increase their confidence in the system
As a developer, I'd like to implement an evaluation solution for FireX
As a DevOps I'd like to copy app registrations secrets to a KeyVault so other services and resources can access it from there
As a DevOps I want to continue work on SMESH infra for faster deployment
As a DevOps I want to understand how much time is needed to deploy and configure various parts of SMESH infra
Create a demo from inputs that Hodaya will share
As a developer, I would like to cover "act as Azure Cloud Expert" in SMESH tests
As a DevOps I'd like to know whether to keep ITE resources
As Data Analyst I would like to apply the aggregation logic to other data sources
As a designer I would like to clean up Figma file for smesh 
as a devops i'd like to use these new health endpoints for kubernetes probes
"""

async def get_workitems(sprint_name: str):
    azure_test = AzureDevOpsService()
    work_items = await azure_test.fetch_work_items(sprint_name)
    return work_items


# Main function that runs the chain and handles the work items
async def generate_release_notes(sprint_name: str):
    # Get work items (await because it's an async function)
    # work_items =  test # await get_workitems(sprint_name)

    # Format the work items to match the prompt template
    # formatted_work_items = format_work_items(work_items)

    # Run the LLM chain with the formatted work items
    release_notes = test_chain.run(work_items=test)

    return release_notes


# Example usage of the function (use asyncio to run the async function)
sprint_name = "Sprint 56"
release_notes = asyncio.run(generate_release_notes(sprint_name))

# Split the data into lines
lines = release_notes.strip().split("\n")



# Open a CSV file for writing
with open('work_items.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    # Write the header
    writer.writerow(['WorkItem', 'Category'])

    # Write each line of data
    for line in lines:
        print(line)
        work_item, category = line.split('@')
        writer.writerow([work_item, category])


# Function to read CSV file and return data as a dictionary
def read_csv(file_name):
    data = {}
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            work_item, category = row
            data[work_item] = category
    return data


# Read data from both CSV files
file1_data = read_csv('test.csv')
file2_data = read_csv('work_items.csv')

# Initialize counters
identical_count = 0
different_count = 0

# Compare the categories for each WorkItem
for work_item in file1_data:
    if work_item in file2_data:
        if file1_data[work_item] == file2_data[work_item]:
            identical_count += 1
        else:
            different_count += 1

# Output the results
print(f"Identical lines: {identical_count}")
print(f"Different lines: {different_count}")
print (f"Percentage of accuracy: {identical_count}")
