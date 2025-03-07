from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
class PromptBuilder:
    def __init__(self):
        self.role = ""
        self.task_description = ""
        self.input_specifications = ""
        self.output_requirements = ""
        self.constraints = ""
        self.edge_cases = ""
        self.example_prompt = ""

    def set_role(self, role: str):
        """Define the role of the AI."""
        self.role = f"You are {role}."
        return self

    def set_task_description(self, description: str):
        """Describe the specific task the AI needs to perform."""
        self.task_description = description
        return self

    def set_input_specifications(self, input_spec: str):
        """Define the expected input format or details."""
        self.input_specifications = f"Input Format: {input_spec}."
        return self

    def set_output_requirements(self, output_req: str):
        """Specify the format and structure of the output."""
        self.output_requirements = f"Output Format: {output_req}."
        return self

    def set_constraints(self, constraints: str):
        """Define strict rules and limitations for the AI's response."""
        self.constraints = f"Rules: {constraints}."
        return self

    def set_edge_cases(self, edge_cases: str):
        """Specify how to handle ambiguous cases."""
        self.edge_cases = f"Edge Cases: {edge_cases}."
        return self

    def set_example_prompt(self, example: str):
        """Provide an example of a well-structured prompt."""
        self.example_prompt = f"Example: {example}"
        return self

    def build(self):
        """Constructs and returns the final prompt as a formatted string."""
        return "\n".join(filter(None, [
            self.role,
            self.task_description,
            self.input_specifications,
            self.output_requirements,
            self.constraints,
            self.edge_cases,
            self.example_prompt
        ]))
'''example usage for prompt builder'''
'''prompt = (PromptBuilder()
          .set_role("an AI that classifies work items")
          .set_task_description("Classify the following work items into predefined categories.")
          .set_input_specifications("A list of work item descriptions")
          .set_output_requirements("Strict JSON format with a list of classified work items")
          .set_constraints("Each work item must belong to one category; respond only in JSON format")
          .set_edge_cases("If an item does not match any category, classify it as 'n_a'")
          .set_example_prompt("Work Items: {work_items}\nRespond only with JSON.")
          .build())'''


classifiy_prompt=(PromptBuilder().set_role("You are an AI that classifies work items.")
                               .set_task_description("Classify the following work items into predefined categories.")
                               .set_input_specifications("A list of work items. ")
                               .set_output_requirements("""Format the response strictly as JSON using this schema:
           {format_instructions}""").set_edge_cases("If an item does not match any category, classify it as 'n_a' althgough try to avoid that")
                               .set_constraints("Each work item must belong to one category; respond only in JSON format")
                                 .set_example_prompt("Work Items: {work_items}\nRespond only with JSON.").build())














class classifying_prompt:
    classification_one:str = """
            You are an AI that classifies work items.

            Classify the following work items into one of the categories each: new_feature, improvement,bug_fixes,test,n_a

            Format the response strictly as JSON using this schema:
           {format_instructions}

            Work Items:
            {work_items}

            Respond only with JSON.
                        """
class system_insturctions:
    system_one :str = "you are a proffessional releasse note expert with highly skilled in writing release notes"
    system_two:str = '''Act as a technical writer. you will write release notes for the input data below.'
                        your audience is business people with limited technical knowledge.
                        you will write the release notes in a way that is easy to understand for business people.'''
    system_three:str = f'Act as a technical writer. you will write release notes for the input data below.'

class summarize_format:
    format_one:str = "summarize the input data below"
    format_two:str = "summarize the input data below in a way that is easy to understand for business people"
    format_three:str = "summarize the input data below in a way that is easy to understand for business people"

class examples:
    example_one:str = "this is an example of a release note: 'Fixed a bug where the user could not log in'"
    example_two:str = "this is an example of a release note: 'Fixed a bug where the user could not log in'"
    example_three:str = "this is an example of a release note: 'Fixed a bug where the user could not log in'"


class prompt_templates:
    tagging_base_prompt :str = "Tag the data into structured categories. Provide the output as tjhe structure probided with values as the relevant work items."
    prompt_two:str = "you can write another prompt here and try it out"
class paragraphGeneration:
    prompt_one:str = """
You are given a list of work items and a topic structure (new features, improvements, bug fixes, tests, etc.).
Your task is to generate one paragraph of the release notes focusing specifically on {topic_name}.

Here is the data:
{work_items}

Follow these instructions:
1. Summarize relevant details for {topic_name}.
2. Be concise but informative.
3. Maintain a professional release note style.

Output:
A single paragraph describing the {topic_name}.
"""
class FinalAssembly:
    prompt_one:str = """ you are an helpful assistant who is specializing in creating a release note documents concerning both technological and business aspects.
We have these paragraphs from previous steps:
{paragraphs}, each paragraph focusing on a specific topic.

Below are some example final documents (in JSON format) demonstrating the output style:
{example_final_docs}
do not overfit to the examples! but use them as general guidelines

Now assemble them into a cohesive release notes document.

System instructions:
{system_instructions}

Output must be a JSON with keys doc_name, title, and content. Title is a short summary, doc_name is the version doc name, and content is the actual text.
Use the following format:
{{"doc_name": "<string>", "title": "<string>", "content": "<string>"}}


"""

paragraph_examples = [
    '''SMESH latest release is out with new features and improved performance to support your security engagements and work!



What’s new in version 0.8.2?


New features:

o Concrete Countermeasures – User Feedback: Enable the user to mark text and provide feedback or suggest correction, which will improve the AI model in the backend and improve accuracy. View the demo here.


Periodic performance improvement and system updates:

· TBD


Stay tuned for the upcoming features (just in few weeks' time):


Upcoming features:

o Reporting Engine – Attack Path Filtering: Enable the system to provide more relevant attack techniques and patterns given a certain CVE, through smart filtering functionality in the backend that leverages LLMs.

o Concrete Countermeasures – CWE Mitigation Framework component: Enable user to select between different attack frameworks – D3FEND or MITRE.


We are continuously working on improving SMESH to provide value to your security engagements. As always, we appreciate your feedback to help us grow SMESH!'''
    ,
'''We can add GIFS, please find the suggested ones here: https://ts.accenture.com/:f:/r/sites/SMESH/Shared%20Documents/Engagement%20Materials/Release%20Updates?csf=1&web=1&e=WGvG37

SMESH latest release is out with many new functionalities and improved performance to support your security engagements and work!

What’s new in version 0.7.0?


New functionalities:

o Export and Import functionalities are now available for Reporting Engine, Security Advisor and Concrete Countermeasures:

o Export*: Ability to export security findings (Reporting Engine), chats (Security Advisor) and countermeasures (Concrete Countermeasures) to JSON or CSV format to enable reviewing, sharing, and reporting the security insights in an editable format.

o Import: Ability to upload previously exported security findings, chats, and countermeasures in JSON format to enable collaborative investigation over SMESH or handover current investigation to a team member.

* Users should assume full responsibility for data security of the exported data.

o Cyware integration for existing and future capabilities: Connect SMESH with Accenture’s Cyware to support selected analysis in Reporting Engine such as exploitation and severity analysis. Cyware will provide SMESH with Accenture internal security insights such as providing Common Product Enumeration, severity assessment and mitigation information related to a documented vulnerability.

Periodic performance improvement and system updates:

o Concrete countermeasures response time improved by 70%




Stay tuned for the upcoming features (just in few weeks' time):


New features:

o Reporting Engine – Attack Flow: Enable users to create a graph representation of the attacker’s possible movements in the system to exploit a vulnerability according to MITRE ATT&CK Flow framework, by simply entering a free text description of an adversarial scenario.


New functionalities:

o Reporting Engine – Attack Path Filtering: Enable the system to provide more relevant attack techniques and patterns given a certain CVE, through smart filtering functionality in the backend that leverages LLMs.


We are continuously working on improving SMESH to provide value to your security engagements. As always, we appreciate your feedback to help us grow SMESH!


[end of announcement]


[content for next announcement]

Periodic performance improvement and system updates:

o System alignment with the latest MITRE ATT&CK version – v14''']
