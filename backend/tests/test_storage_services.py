

from backend.app.services.storage_services import BlobStorageService
from backend.app.utils.config import blob_storage_account_url, blob_storage_container_name


def test():
    platform = BlobStorageService(blob_storage_account_url, blob_storage_container_name)
    # is_saved = platform.save_file("test_amit","test_amit test_amit","test_amit @ test_amit @ test_amit 123")
    # print(f"is_saved? {is_saved}")
    doc_test = platform.fetch_file("test.docx")
    print(f"Doc test is: {doc_test}")
    # if not doc_test:
    #     print("the file doesn't exist")
        # # Iterate through each paragraph and print its text
        # for paragraph in doc_test.paragraphs:
        #     print(paragraph.text)

test()


# from backend.app.services.storage_services import SharePointStorageService
# from backend.app.utils.config import sharepoint_site, sharepoint_folder, sharepoint_username, sharepoint_password
#
#
#
# def test():
#     platform = SharePointStorageService(sharepoint_site, sharepoint_folder,
#     {"username" : sharepoint_username, "password" : sharepoint_password})
#     platform.save_file("test_amit","test_amit test_amit","test_amit @ test_amit @ test_amit 123")
#     doc_test = platform.fetch_file("test_amit.docx")
#     # Iterate through each paragraph and print its text
#     for paragraph in doc_test.paragraphs:
#         print(paragraph.text)
#
# test()


# from office365.sharepoint.client_context import ClientContext
# from office365.runtime.auth.authentication_context import AuthenticationContext
#
# context = AuthenticationContext(url)
#
# if context.acquire_token_for_user(username=sharepoint_username, password=sharepoint_password):
#     context = ClientContext(url, context)
#     print(context)
