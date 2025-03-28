# File: backend/tests/demo.py
import os
import sys
import streamlit as st
import asyncio


from azure_authentication_client import authenticate_openai
from backend.app.utils.config import (authentication_headers_azure, azure_devops_org, azure_devops_project,
                                      azure_devops_team, azure_devops_iteration_team)
from backend.app.utils.config import sharepoint_site, sharepoint_folder, sharepoint_password, sharepoint_username

from langchain_openai import AzureChatOpenAI
from backend.app.services.storage_services import SharePointStorageService

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, repo_root)

from backend.app.services.llm_services.generate import BasicGenerator
from backend.app.services.azure_devops_services import AzureDevOpsService


def get_azure_llm():
    api_key = authenticate_openai().api_key
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = api_key
    return AzureChatOpenAI(
        deployment_name="gpt-4o-deployment",
        temperature=0.7,
        azure_endpoint="https://function-app-open-ai-prod-apim.azure-api.net/proxy-api/"
    )
llm = get_azure_llm()
async def main():
    st.title("Automated Release Notes Demo")
    test_service = AzureDevOpsService(auth_headers=authentication_headers_azure,azure_devops_project=azure_devops_project,
                                      azure_devops_org=azure_devops_org,azure_devops_team=azure_devops_team,
                                      azure_devops_iteration_team=azure_devops_iteration_team)
    # test_database = SharePointStorageService(sharepoint_site, sharepoint_folder,
    #                                          {"username": sharepoint_username, "password": sharepoint_password})

    # Await the async get_azure_llm function

    if llm:
        st.success(f"LLM pointer was set correctly. This is what we got: {llm}")
    else:
        st.error("LLM pointer is not set. Please check your configuration.")

    gen = BasicGenerator(llm)
    all_sprints = await test_service.fetch_sprints()
    sprint_names = [sprint.name for sprint in all_sprints]
    st.write("Available Sprints:")
    selected_sprints = st.multiselect("Select Sprints", sprint_names)

    if st.button("Generate"):
        if selected_sprints:
            work_items = await test_service.fetch_work_items_for_multiple_sprints(selected_sprints)
            st.write("Fetched Work Items:", work_items)
            st.write(type(work_items[0]))

            response = await gen.generate(work_items)
            st.write("Response:")
            st.write(response)
        else:
            st.warning("Please select at least one sprint before generating.")

if __name__ == "__main__":


    asyncio.run(main())