from langchain_core.prompts import ChatPromptTemplate, PromptTemplate


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
#TODO: amit needs to complete the examples
class examples:
    example_one:str = "this is an example of a release note: 'Fixed a bug where the user could not log in'"
    example_two:str = "this is an example of a release note: 'Fixed a bug where the user could not log in'"
    example_three:str = "this is an example of a release note: 'Fixed a bug where the user could not log in'"


class prompt_templates:
    tagging_base_prompt :str = "Tag the data into structured categories. Provide the output as tjhe structure probided with values as the relevant work items."
