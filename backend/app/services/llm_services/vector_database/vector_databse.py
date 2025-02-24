import os

from azure_authentication_client import authenticate_openai
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.embeddings import embeddings
from langchain_huggingface import HuggingFaceEmbeddings

api_key = authenticate_openai().api_key
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = api_key

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = api_key
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = InMemoryVectorStore(embedding=embeddings)
document_1 = Document(
    page_content='''SMESH latest release is out with new features and improved performance to support your security engagements and work!



What’s new in version 0.8.2?


New features:

o Concrete Countermeasures – User Feedback: Enable the user to mark text and provide feedback or suggest correction, which will improve the AI model in the backend and improve accuracy. View the demo here.


Periodic performance improvement and system updates:

· TBD


Stay tuned for the upcoming features (just in few weeks' time):


Upcoming features:

o Reporting Engine – Attack Path Filtering: Enable the system to provide more relevant attack techniques and patterns given a certain CVE, through smart filtering functionality in the backend that leverages LLMs.

o Concrete Countermeasures – CWE Mitigation Framework component: Enable user to select between different attack frameworks – D3FEND or MITRE.


We are continuously working on improving SMESH to provide value to your security engagements. As always, we appreciate your feedback to help us grow SMESH!''',
    metadata={"source": "Febuary.2024"},
)

document_2 = Document(
    page_content='''SMESH latest release is out with many new functionalities and improved performance to support your security engagements and work!

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

o System alignment with the latest MITRE ATT&CK version – v14.''',
    metadata={"source": "sprints 28,29,30,31,32"},
)
document_3 = Document(
   page_content='''Very happy to see the increasing interest in SMESH and excitement about new capabilities!

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


Stay tuned for the hands-on session, where we will provide a walkthrough of the new features''',
    metadata={"source": "09/01/2024"},
)
document_4 = Document(
    page_content='''Happy to announce the first SMESH release of FY25 with new capabilities and improved performance to support your security engagements and work!


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



We are continuously working on improving SMESH to provide value to your security engagements. As always, we appreciate your feedback to help us grow SMESH!''',
    metadata={"source": "september_2024"},
)
documents = [document_1, document_2,document_3,document_4]

vector_store.add_documents(documents=documents, ids=["doc1", "doc2","doc3","doc4"])
print("hi")