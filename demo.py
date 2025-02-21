import streamlit as st
import asyncio

from backend.app.services.azure_devops_services import AzureDevOpsService
from backend.app.services.llm_services.generating_policies import BasicGenerator
from backend.app.utils.useful_functions import get_azure_llm


# Placeholder for AzureDevOpsService and BasicGenerator
# Replace with your actual implementation


async def main():
    st.title("Automated Release Notes Demo")

    # Initialize AzureDevOpsService and BasicGenerator
    test_service = AzureDevOpsService()
    llm = get_azure_llm()
    gen = BasicGenerator(llm)

    # Fetch and display all sprints
    all_sprints = await test_service.fetch_sprints()
    sprint_names = [sprint.name for sprint in all_sprints]
    st.write("Available Sprints:")
    selected_sprints = st.multiselect("Select Sprints", sprint_names)

    if st.button("Generate"):  # Add a generate button
        if selected_sprints:
            # Fetch work items for selected sprints
            selected_sprints_list = selected_sprints #No need to convert, already a list
            work_items = await test_service.fetch_work_items_for_multiple_sprints(selected_sprints_list)
            st.write("Fetched Work Items:",work_items)
            st.write(type(work_items[0]))

            # Generate response
            response = await gen.generate(work_items)

            # Show the response as output
            #st.write("Generated Response:")
           # st.write(response)
        else:
            st.warning("Please select at least one sprint before generating.")

if __name__ == "__main__":
    asyncio.run(main())