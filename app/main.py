from workspace.toWork import WorkSpace
from os import getenv
from dotenv import load_dotenv
import time

load_dotenv()


def run_project():
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
