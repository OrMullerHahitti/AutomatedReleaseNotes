
from backend.app.services.storage_services import SharePointStorageService
import asyncio


# https://ts.accenture.com/sites/CoreTeam-SoftwareEngineering/Shared%20Documents/General/ARN
# https://xx.abcde.com/sites/Engineering/Shared%20Documents/General/ARN
# https://ts.accenture.com/sites/CoreTeam-SoftwareEngineering/Shared%20Documents/General
# https://ts.accenture.com/sites/CoreTeam-SoftwareEngineering/Shared%20Documents/General

def test():
    # Secrets
    secrets = {
        "username": "",
        "password": ""
    }
    site_url = "https://ts.accenture.com/sites/CoreTeam-SoftwareEngineering"
    folder_path = "/sites/CoreTeam-SoftwareEngineering/Shared Documents/General/"
    platform = SharePointStorageService(site_url, folder_path, secrets)
    platform.save_file("test", "test")


test()


# Good documentation here!!!!! https://pypi.org/project/Office365-REST-Python-Client/
# Consider Interactive login for the testing
