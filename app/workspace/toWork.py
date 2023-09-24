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
        self.url_base = "http://localhost:8000"

    def clean_workspace(self):
        self.path_directory.clean_work_directory()

    def prepare_folder_files(self, file_name):
        source_file = self.path_directory.get_file_from_file_directory(file=file_name)
        destiny_folder = self.path_directory.get_work_directory()
        unzip_file(source_file=source_file, destiny_folder=destiny_folder)
        extract_all_gz(destiny_folder)

    def storage_on_database(self):
        for location in get_locations(self.path_directory.get_work_directory()):
            url = "http://localhost:8000/locations"
            response = requests.post(
                url=url,
                headers={"Accept": "application/json"},
                json=location,
            )
            if not response.ok:
                print(response.text())
        for genotype in get_genotypes(self.path_directory.get_work_directory()):
            response = requests.post(
                url="http://localhost:8000/genotypes",
                headers={"Accept": "application/json"},
                json=genotype,
            )
            if not response.ok:
                print(response.text())
        for raw_collections in get_raw_collections(
            self.path_directory.get_work_directory()
        ):
            trail = dict()
            trail["name"] = raw_collections.pop("trails.name")
            response = requests.post(
                url="http://localhost:8000/trails/",
                headers={"Accept": "application/json"},
                json=trail,
            )
            if not response.ok:
                print(response.text())
            raw_collections["trail_id"] = response.json()["id"]
            number = raw_collections.pop("locations.number")
            raw_collections.pop("locations.country")
            raw_collections.pop("locations.description")
            response = requests.get(
                url="http://localhost:8000/locations/",
                headers={"Accept": "application/json"},
                params={"number": int(number)},
            )
            if not response.ok:
                print(response.text())
            raw_collections["location_id"] = response.json()["id"]
            ids = {
                "c_id": raw_collections.pop("genotypes.c_id"),
                "s_id": raw_collections.pop("genotypes.s_id"),
            }
            raw_collections.pop("genotypes.cross_name")
            response = requests.get(
                url="http://localhost:8000/genotypes/",
                headers={"Accept": "application/json"},
                params=ids,
            )
            if not response.ok:
                print(response.text())
            raw_collections["genotype_id"] = response.json()["id"]
            trait = {
                "name": raw_collections.pop("traits.name"),
                "number": raw_collections.pop("traits.trait_number"),
                "description": "",
                "co_trait_name": "",
                "variable_name": "",
                "co_id": "",
            }
            response = requests.post(
                url="http://localhost:8000/traits/",
                headers={"Accept": "application/json"},
                json=trait,
            )
            if not response.ok:
                print(response.text())
            raw_collections["trait_id"] = response.json()["id"]

            response = requests.post(
                url="http://localhost:8000/units/",
                headers={"Accept": "application/json"},
                json={"name": raw_collections.pop("units.name")},
            )
            if not response.ok:
                print(response.text())
            raw_collections["unit_id"] = response.json()["id"]

            raw_collections["hash_raw"] = str(raw_collections.pop("hash"))
            response = requests.post(
                url="http://localhost:8000/raw_collections/",
                headers={"Accept": "application/json"},
                json=raw_collections,
            )
            if not response.ok:
                print(response.text())
        for trait_detail in get_trait_details(self.path_directory.get_work_directory()):
            print(trait_detail)
            if "variable_ontologies" in trait_detail:
                variable_ontologies = trait_detail.pop("variable_ontologies")
                crop_ontologies = trait_detail.pop("crop_ontologies")
                response = requests.post(
                    url="{}/crop_ontologies/".format(self.url_base),
                    headers={"Accept": "application/json"},
                    json=crop_ontologies,
                )
                if not response.ok:
                    print(response.text())
                trait_ontologies = trait_detail.pop("trait_ontologies")
                trait_ontologies["crop_ontology_id"] = response.json()["id"]
                response = requests.post(
                    url="{}/trait_ontologies/".format(self.url_base),
                    headers={"Accept": "application/json"},
                    json=trait_ontologies,
                )
                if not response.ok:
                    print(response.text())
                variable_ontologies["trait_ontology_id"] = response.json()["id"]
                traits = trait_detail.pop("traits")
                response = requests.get(
                    url="{}/traits/".format(self.url_base),
                    headers={"Accept": "application/json"},
                    params={"name": traits["name"]},
                )
                if not response.ok:
                    print(response.text())
                id = response.json()["id"]
                traits["description"] = ""
                traits["number"] = ""
                response = requests.put(
                    url="{}/traits/{}".format(self.url_base, id),
                    headers={"Accept": "application/json"},
                    json=traits,
                )
                if not response.ok:
                    print(response.text())
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
                    print(response.text())
                variable_ontologies["method_ontology_id"] = response.json()["id"]

                scale_ontologies = trait_detail.pop("scale_ontologies")
                response = requests.post(
                    url="{}/scale_ontologies/".format(self.url_base),
                    headers={"Accept": "application/json"},
                    json=scale_ontologies,
                )
                if not response.ok:
                    print(response.text())
                variable_ontologies["scale_ontology_id"] = response.json()["id"]

                response = requests.post(
                    url="{}/variable_ontologies/".format(self.url_base),
                    headers={"Accept": "application/json"},
                    json=variable_ontologies,
                )
                if not response.ok:
                    print(response.text())
