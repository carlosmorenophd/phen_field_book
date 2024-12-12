from workspace.toWork import WorkSpace
from os import getenv
from dotenv import load_dotenv
import time

load_dotenv()

<<<<<<< HEAD
=======
def run_project():
    work_space = WorkSpace("/home/Yeiden/Documents/wirk/")
    work_space.work_with_all_zips()
    # work_space.clean_workspace()
    # work_space.prepare_folder_files("dataverse_files.zip")
    # work_space.storage_on_database()
>>>>>>> hotfix/23.10.21

def run_project():
    if getenv("DEBUG"):
        work_space = WorkSpace(path=getenv(
            "PATH_TO_SCRAPPING"), api_storage=getenv("URL_DATA_WAREHOUSE"))
        work_space.work_with_all_zips()
    else:
        while True:
            print("Working ----- ")
            try:
                work_space = WorkSpace(path=getenv(
                    "PATH_TO_SCRAPPING"), api_storage=getenv("URL_DATA_WAREHOUSE"))
                work_space.work_with_all_zips()
            except Exception as error:
                print("Error to work: ", error)
            time.sleep(60)

if __name__ == "__main__":
    run_project()
