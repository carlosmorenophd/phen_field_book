import requests

from .compressFile import extract_all_gz, unzip_file
from .pathDirectory import PathDirectory
from .xlsToDatabase import (
    get_genotypes,
    get_locations,
    get_raw_collections,
    get_trait_details,
)


class WorkSpace:
    def __init__(self, path):
        self.path_directory = PathDirectory(home=path)

    def clean_workspace(self):
        self.path_directory.clean_work_directory()

    def prepare_folder_files(self, file_name):
        source_file = self.path_directory.get_file_from_file_directory(file=file_name)
        destiny_folder = self.path_directory.get_work_directory()
        unzip_file(source_file=source_file, destiny_folder=destiny_folder)
        extract_all_gz(destiny_folder)

    def storage_on_database(self):
        for location in get_locations(self.path_directory.get_work_directory()):
            url = "http://localhost/locations"
            r = requests.post(
                url=url,
                headers={"Accept": "application/json"},
                json=location,
            )
        for genotype in get_genotypes(self.path_directory.get_work_directory()):
            url = "http://localhost/genotypes"
            r = requests.post(
                url=url,
                headers={"Accept": "application/json"},
                json=genotype,
            )
        for raw_collections in get_raw_collections(self.path_directory.get_work_directory()):
            print(raw_collections)
            url = "http://localhost/raw_collections/"
            r = requests.post(
                url=url,
                headers={"Accept": "application/json"},
                json=genotype,
            )
        var = get_trait_details(self.path_directory.get_work_directory())
