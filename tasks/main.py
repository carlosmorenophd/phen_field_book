"""Main function"""
import time
from os import getenv

from dotenv import load_dotenv

from src.toWork import WorkSpace


load_dotenv()


def run_project():
    """Main function to waiting to new zip file to work with it
    """
    if getenv("MODE_DAEMON"):
        while True:
            print("Working ----- ")
            try:
                work_space = WorkSpace(
                    path=getenv("FOLDER_DATA"),
                    api_storage=getenv("URL_DATA_WAREHOUSE"),
                )
                work_space.work_with_all_zips()
            except FileNotFoundError as error:
                print("Error to work: ", error)
            time.sleep(600)
    else:
        work_space = WorkSpace(
            path=getenv("FOLDER_DATA"),
            api_storage=getenv("URL_DATA_WAREHOUSE"),
        )
        work_space.work_with_all_zips()


if __name__ == "__main__":
    run_project()
