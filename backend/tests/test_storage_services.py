
from backend.app.services.storage_services import SharePointStorageService
from backend.app.utils.config import sharepoint_site, sharepoint_folder, sharepoint_username, sharepoint_password

# "https://ts.accenture.com/sites/CoreTeam-SoftwareEngineering/Shared Documents/General/ARN/"


def test():
    platform = SharePointStorageService(sharepoint_site, sharepoint_folder,
    {"username" : sharepoint_username, "password" : sharepoint_password})
    platform.save_file("test_amit","test_amit test_amit","test_amit @ test_amit @ test_amit 123")
    doc_test = platform.fetch_file("test_amit.docx")
    # Iterate through each paragraph and print its text
    for paragraph in doc_test.paragraphs:
        print(paragraph.text)

test()
