"""Main function to work with zip file

    Raises:
        ConnectionError: _description_
        ConnectionError: _description_
        ConnectionError: _description_
        ConnectionError: _description_
        ConnectionError: _description_
        ConnectionError: _description_
        ConnectionError: _description_
        ConnectionError: _description_
        ConnectionError: _description_
        ConnectionError: _description_
        ConnectionError: _description_
    """
import requests

from src.compressFile import extract_all_gz, unzip_file
from src.pathDirectory import PathDirectory
from src.xlsToDatabase import (
    get_genotypes,
    get_locations,
    get_raw_collections,
    get_trait_details,
    get_environments,
)


class WorkSpace:
    """Start to work with space or folder
    """

    def __init__(self, path: str, api_storage: str):
        self.path_directory = PathDirectory(home=path)
        self.url_base = api_storage

    def clean_workspace(self):
        """Clean work directory
        """
        self.path_directory.clean_work_directory()

    def prepare_folder_files(self, file_name: str):
        """Create all folder to work with it

        Args:
            file_name (_type_): file the name to work with it
        """
        source_file = self.path_directory.get_file_from_file_directory(
            file=file_name)
        destiny_folder = self.path_directory.work_directory()
        unzip_file(source_file=source_file, destiny_folder=destiny_folder)
        extract_all_gz(destiny_folder)

    def work_with_all_zips(self):
        """Method to work with a zip file
        """
        for file in self.path_directory.all_files_zip():
            print(f"File to work {file}")
            self.clean_workspace()
            self.prepare_folder_files(file_name=file)
            list_csv_files = self.path_directory.all_file_csv()
            print(f"List of files {list_csv_files}")
            self.storage_on_database(list_csv_files=list_csv_files)
            self.path_directory.remove_file(file)

    def storage_on_database(self, list_csv_files: list):
        """Save on API rest database

        Args:
            list_csv_files (_type_): list the files to store on API rest database
        """
        self.store_location(locations=get_locations(
            path=self.path_directory.work_directory(),
            list_csv_files=list_csv_files,
        ))
        self.store_genotype(genotypes=get_genotypes(
            path=self.path_directory.work_directory(),
            list_csv_files=list_csv_files,
        ))
        self.store_environments(environments=get_environments(
            path=self.path_directory.work_directory(),
            list_csv_files=list_csv_files
        ))
        self.store_raw_collection(raw_collections=get_raw_collections(
            path=self.path_directory.work_directory(),
            list_csv_files=list_csv_files,
        ))
        self.store_trait_detail(trait_details=get_trait_details(
            path=self.path_directory.work_directory(),
            list_csv_files=list_csv_files,
        ))

    def store_location(self, locations: list):
        """Store locations

        Args:
            locations (list): List of location

        Raises:
            ConnectionError: Return error if can't connect to API rest
        """
        print(f"Url to save => {self.url_base}/locations")
        for location in locations:
            url = f"{self.url_base}/locations"
            response = requests.post(
                url=url,
                headers={"Accept": "application/json"},
                json=location,
                timeout=5000,
            )
            if not response.ok:
                raise ConnectionError(response.text())

    def store_genotype(self, genotypes: list):
        """Save genotypes list to API rest

        Args:
            genotypes (list): list of genotype to stores

        Raises:
            ConnectionError: Return error if can't connect to API rest
        """
        for genotype in genotypes:
            response = requests.post(
                url=f"{self.url_base}/genotypes",
                headers={"Accept": "application/json"},
                json=genotype,
                timeout=5000,
            )
            if not response.ok:
                raise ConnectionError(response.text())

    def store_environments(self, environments: list):
        """Save environment variables

        Args:
            environments (list): list of environment to save

        Raises:
            ConnectionError: Return error if can't connect to API rest
        """
        for environment in environments:
            response = requests.post(
                url=f"{self.url_base}/field_collection_environments/xls",
                headers={"Accept": "application/json"},
                json=environment,
                timeout=5000,
            )
            if not response.ok:
                raise ConnectionError(response.text())

    def store_raw_collection(self, raw_collections: list):
        """Save list of raw data, data equal to csv and xls process

        Args:
            raw_collections (list): list of raw to store

        Raises:
            ConnectionError: Return error if can't connect to API rest
        """
        for raw_collection in raw_collections:
            raw_collection["hash_raw"] = str(raw_collection.pop("hash"))
            response = requests.post(
                url=f"{self.url_base}/raw_collections/xls",
                headers={"Accept": "application/json"},
                json=raw_collection,
                timeout=5000,
            )
            if not response.ok:
                raise ConnectionError(response.text())

    def store_trait_detail(self, trait_details: list):
        """Save list of trait with other information

        Args:
            trait_details (list): list of trait to store

        Raises:
            ConnectionError: Return error if can't connect to API rest
            ConnectionError: Return error if can't connect to API rest
            ConnectionError: Return error if can't connect to API rest
            ConnectionError: Return error if can't connect to API rest
            ConnectionError: Return error if can't connect to API rest
            ConnectionError: Return error if can't connect to API rest
            ConnectionError: Return error if can't connect to API rest
        """
        for trait_detail in trait_details:
            if "variable_ontologies" in trait_detail:
                variable_ontologies = trait_detail.pop("variable_ontologies")
                crop_ontologies = trait_detail.pop("crop_ontologies")
                response = requests.post(
                    url=f"{self.url_base}/crop_ontologies/",
                    headers={"Accept": "application/json"},
                    json=crop_ontologies,
                    timeout=5000,
                )
                if not response.ok:
                    raise ConnectionError(response.text())
                trait_ontologies = trait_detail.pop("trait_ontologies")
                trait_ontologies["crop_ontology_id"] = response.json()["id"]
                response = requests.post(
                    url=f"{self.url_base}/trait_ontologies/",
                    headers={"Accept": "application/json"},
                    json=trait_ontologies,
                    timeout=5000,
                )
                if not response.ok:
                    raise ConnectionError(response.text())
                variable_ontologies["trait_ontology_id"] = response.json()[
                    "id"]
                traits = trait_detail.pop("traits")
                response = requests.get(
                    url=f"{self.url_base}/traits/",
                    headers={"Accept": "application/json"},
                    params={"name": traits["name"]},
                    timeout=5000,
                )
                if not response.ok:
                    response = requests.post(
                        url=f"{self.url_base}/traits/",
                        headers={"Accept": "application/json"},
                        json={
                            "name": traits["name"],
                            "number": "0",
                            "description": "",
                            "co_trait_name": traits["name"],
                            "variable_name": traits["variable_name"],
                            "co_id": traits["co_id"],
                        },
                        timeout=5000,
                    )
                    if not response.ok:
                        raise ConnectionError(response.text())
                id_trait = response.json()["id"]
                traits["description"] = ""
                traits["number"] = ""
                response = requests.put(
                    url=f"{self.url_base}/traits/{id_trait}",
                    headers={"Accept": "application/json"},
                    json=traits,
                    timeout=5000,
                )
                if not response.ok:
                    raise ConnectionError(response.text())
                variable_ontologies["trait_id"] = response.json()["id"]
                method_ontologies = trait_detail.pop("method_ontologies")
                if method_ontologies["formula"] is None:
                    method_ontologies["formula"] = ""
                response = requests.post(
                    url=f"{self.url_base}/method_ontologies/",
                    headers={"Accept": "application/json"},
                    json=method_ontologies,
                    timeout=5000,
                )
                if not response.ok:
                    raise ConnectionError(response.text())
                variable_ontologies["method_ontology_id"] = response.json()[
                    "id"]

                scale_ontologies = trait_detail.pop("scale_ontologies")
                response = requests.post(
                    url=f"{self.url_base}/scale_ontologies/",
                    headers={"Accept": "application/json"},
                    json=scale_ontologies,
                    timeout=5000,
                )
                if not response.ok:
                    raise ConnectionError(response.text())
                variable_ontologies["scale_ontology_id"] = response.json()[
                    "id"]

                response = requests.post(
                    url=f"{self.url_base}/variable_ontologies/",
                    headers={"Accept": "application/json"},
                    json=variable_ontologies,
                    timeout=5000,
                )
                if not response.ok:
                    raise ConnectionError(response.text())
