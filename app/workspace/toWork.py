import requests

from .compressFile import extract_all_gz, unzip_file
from .pathDirectory import PathDirectory
from .xlsToDatabase import (
    get_genotypes,
    get_locations,
    get_raw_collections,
    get_trait_details,
    get_environments,
)


class WorkSpace:
    def __init__(self, path):
        self.path_directory = PathDirectory(home=path)
        self.url_base = "http://localhost:8000"

    def clean_workspace(self):
        self.path_directory.clean_work_directory()

    def prepare_folder_files(self, file_name):
        source_file = self.path_directory.get_file_from_file_directory(
            file=file_name)
        destiny_folder = self.path_directory.get_work_directory()
        unzip_file(source_file=source_file, destiny_folder=destiny_folder)
        extract_all_gz(destiny_folder)

    def work_with_all_zips(self):
        for file in self.path_directory.get_all_files_zip():
            self.clean_workspace()
            self.prepare_folder_files(file_name=file)
            list_csv_files = self.path_directory.get_all_file_csv()
            self.storage_on_database(list_csv_files=list_csv_files)
            self.path_directory.remove_file(file)

    def storage_on_database(self, list_csv_files):
        self.store_location(locations=get_locations(
            path=self.path_directory.get_work_directory(),
            list_csv_files=list_csv_files,
        ))
        self.store_genotype(genotypes=get_genotypes(
            path=self.path_directory.get_work_directory(),
            list_csv_files=list_csv_files,
        ))
        self.store_environments(environments=get_environments(
            path=self.path_directory.get_work_directory(),
            list_csv_files=list_csv_files
        ))
        self.store_raw_collection(raw_collections=get_raw_collections(
            path=self.path_directory.get_work_directory(),
            list_csv_files=list_csv_files,
        ))
        self.store_trait_detail(trait_details=get_trait_details(
            path=self.path_directory.get_work_directory(),
            list_csv_files=list_csv_files,
        ))

    def store_location(self, locations):
        for location in locations:
            url = "{}/locations".format(self.url_base)
            response = requests.post(
                url=url,
                headers={"Accept": "application/json"},
                json=location,
            )
            if not response.ok:
                raise ConnectionError(response.text())

    def store_genotype(self, genotypes):
        for genotype in genotypes:
            response = requests.post(
                url="{}/genotypes".format(self.url_base),
                headers={"Accept": "application/json"},
                json=genotype,
            )
            if not response.ok:
                raise ConnectionError(response.text())

    def store_environments(self, environments):
        for environment in environments:
            response = requests.post(
                url="{}/field_collection_environments/xls".format(
                    self.url_base),
                headers={"Accept": "application/json"},
                json=environment,
            )
            if not response.ok:
                raise ConnectionError(response.text())

    def store_raw_collection(self, raw_collections):
        for raw_collection in raw_collections:
            raw_collection["hash_raw"] = str(raw_collection.pop("hash"))
            response = requests.post(
                url="{}/raw_collections/xls".format(self.url_base),
                headers={"Accept": "application/json"},
                json=raw_collection,
            )
            if not response.ok:
                raise ConnectionError(response.text())

    def store_trait_detail(self, trait_details):
        for trait_detail in trait_details:
            if "variable_ontologies" in trait_detail:
                variable_ontologies = trait_detail.pop("variable_ontologies")
                crop_ontologies = trait_detail.pop("crop_ontologies")
                response = requests.post(
                    url="{}/crop_ontologies/".format(self.url_base),
                    headers={"Accept": "application/json"},
                    json=crop_ontologies,
                )
                if not response.ok:
                    raise ConnectionError(response.text())
                trait_ontologies = trait_detail.pop("trait_ontologies")
                trait_ontologies["crop_ontology_id"] = response.json()["id"]
                response = requests.post(
                    url="{}/trait_ontologies/".format(self.url_base),
                    headers={"Accept": "application/json"},
                    json=trait_ontologies,
                )
                if not response.ok:
                    raise ConnectionError(response.text())
                variable_ontologies["trait_ontology_id"] = response.json()[
                    "id"]
                traits = trait_detail.pop("traits")
                response = requests.get(
                    url="{}/traits/".format(self.url_base),
                    headers={"Accept": "application/json"},
                    params={"name": traits["name"]},
                )
                if not response.ok:
                    response = requests.post(
                        url="{}/traits/".format(self.url_base),
                        headers={"Accept": "application/json"},
                        json={
                            "name": traits["name"],
                            "number": "0",
                            "description": "",
                            "co_trait_name": traits["name"],
                            "variable_name": traits["variable_name"],
                            "co_id": traits["co_id"],
                        }
                    )
                    if not response.ok:
                        raise ConnectionError(response.text())
                id = response.json()["id"]
                traits["description"] = ""
                traits["number"] = ""
                response = requests.put(
                    url="{}/traits/{}".format(self.url_base, id),
                    headers={"Accept": "application/json"},
                    json=traits,
                )
                if not response.ok:
                    raise ConnectionError(response.text())
                variable_ontologies["trait_id"] = response.json()["id"]
                method_ontologies = trait_detail.pop("method_ontologies")
                if method_ontologies["formula"] is None:
                    method_ontologies["formula"] = ""
                response = requests.post(
                    url="{}/method_ontologies/".format(self.url_base),
                    headers={"Accept": "application/json"},
                    json=method_ontologies,
                )
                if not response.ok:
                    raise ConnectionError(response.text())
                variable_ontologies["method_ontology_id"] = response.json()[
                    "id"]

                scale_ontologies = trait_detail.pop("scale_ontologies")
                response = requests.post(
                    url="{}/scale_ontologies/".format(self.url_base),
                    headers={"Accept": "application/json"},
                    json=scale_ontologies,
                )
                if not response.ok:
                    raise ConnectionError(response.text())
                variable_ontologies["scale_ontology_id"] = response.json()[
                    "id"]

                response = requests.post(
                    url="{}/variable_ontologies/".format(self.url_base),
                    headers={"Accept": "application/json"},
                    json=variable_ontologies,
                )
                if not response.ok:
                    raise ConnectionError(response.text())
