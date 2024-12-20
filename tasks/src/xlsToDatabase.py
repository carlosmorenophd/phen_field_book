"""Tool to work with some xls files"""
import os
import re

import pandas as pd
import requests

from src.csvTool import fix_csv_remove_comma


def get_locations(path: str, list_csv_files: list) -> dict:
    """Get location into dictionary

    Args:
        path (_type_): work directory
        list_csv_files (_type_): list of files 

    Raises:
        FileNotFoundError: Not found file

    Returns:
        dict: dict with location
    """
    source = search_file_by_regex(
        list_files=list_csv_files,
        end_with="Loc_data.xls",
    )
    file_name = rename_file_csv(
        path=path, source=source,
        destiny='location.csv',
    )
    if os.path.isfile(file_name):
        csv_data = pd.read_csv(
            file_name,
            delimiter='\t',
            engine='python',
            header=None,
        )
        csv_dictionary = csv_data.to_dict('index')
        head = csv_dictionary.pop(0)
        return get_dictionary_by_entity(
            entity='locations',
            head=head,
            csv_dictionary=csv_dictionary
        )
    raise FileNotFoundError('Filing to save file or not exist it')


def search_file_by_regex(
    list_files: list,
    end_with: str,
    end_with_double: str = ""
):
    """Return file that have regex equal

    Args:
        list_files (list): list of files
        end_with (str): regex end with
        end_with_double (str, optional): regex double end. Defaults to "".

    Raises:
        FileNotFoundError: Not have this files 

    Returns:
        _type_: file name
    """

    for file in list_files:
        x = re.search(f"{end_with}$", file)
        if x:
            return file
        if end_with_double != "":
            x = re.search(f"{end_with_double}$", file)
            if x:
                return file
    raise FileNotFoundError(
        f"Can not find the file to work - {end_with}")


def get_genotypes(path: str, list_csv_files: list) -> dict:
    """get genotype

    Args:
        path (str): path to folder
        list_csv_files (list): list of csv files

    Raises:
        FileNotFoundError: Not found the file

    Returns:
        dict: Dictionary of genotype
    """
    source = search_file_by_regex(
        list_files=list_csv_files, end_with="Genotypes_Data.xls")
    file_name = rename_file_csv(
        path=path, source=source, destiny='genotypes.csv')
    if os.path.isfile(file_name):
        csv_data = pd.read_csv(
            file_name, delimiter='\t',
            engine='python',
            header=None,
            encoding='ISO-8859-1'
        )
        csv_dictionary = csv_data.to_dict('index')
        head = csv_dictionary.pop(0)
        return get_dictionary_by_entity(
            entity='genotypes',
            head=head,
            csv_dictionary=csv_dictionary
        )
    raise FileNotFoundError(f"Filing to save {file_name} or not exist it")


def get_environments(path: str, list_csv_files: list) -> dict:
    """Get environment variable

    Args:
        path (str): path to folder
        list_csv_files (list): list of csv files

    Raises:
        FileNotFoundError: Not found file

    Returns:
        dict: Dictionary of environment
    """
    source = search_file_by_regex(
        list_files=list_csv_files, end_with="_EnvData.xls")
    web_file = source.replace("_EnvData.xls", "").replace(" ", "")
    file_name = rename_file_csv(
        path=path, source=source, destiny='env_data.csv')
    if os.path.isfile(file_name):
        csv_data = pd.read_csv(
            file_name, delimiter='\t',
            engine='python',
            header=None,
            encoding='ISO-8859-1'
        )
        csv_dictionary = csv_data.to_dict('index')
        head = csv_dictionary.pop(0)
        return get_dictionary_by_entity(
            entity='env_data',
            head=head,
            csv_dictionary=csv_dictionary,
            static_row={"web_file_name": web_file},
        )
    raise FileNotFoundError(
        f"Filing - EnvData to save {file_name} or not exist it")


def get_raw_collections(path: str, list_csv_files: list) -> dict:
    """Get all raw data from csv

    Args:
        path (str): path to folder
        list_csv_files (list): list of csv files

    Raises:
        FileNotFoundError: File not found

    Returns:
        dict: Dictionary of raw data
    """
    source = search_file_by_regex(
        list_files=list_csv_files,
        end_with="_RawData.xls"
    )
    web_file = source.replace("_RawData.xls", "").replace(" ", "")
    file_name = rename_file_csv(path=path, source=source, destiny='raw.csv')
    fix_csv_remove_comma(folder=path, target_csv='raw.csv')
    if os.path.isfile(file_name):
        csv_data = pd.read_csv(
            file_name, delimiter='\t',
            engine='python',
            header=None,
            encoding='ISO-8859-1'
        )
        csv_dictionary = csv_data.to_dict('index')
        head = csv_dictionary.pop(0)
        return get_dictionary_by_entity(
            entity='raw_collections',
            head=head,
            csv_dictionary=csv_dictionary,
            add_hash=True,
            static_row={"web_file_name": web_file},
        )
    raise FileNotFoundError(f"Filing to save {file_name} or not exist it")


def get_trait_details(path: str, list_csv_files: list) -> None:
    """_summary_

    Args:
        path (str): path to folder
        list_csv_files (list): list of csv files

    Raises:
        FileNotFoundError: File don't found

    Returns:
        _type_: Dictionary of traits
    """
    print("Start to search trait details")
    source = search_file_by_regex(
        list_files=list_csv_files, end_with="IDYN.xls", end_with_double="IDYN.xlsx")
    print(source)
    file_name = os.path.join(path, source)
    if os.path.isfile(file_name):
        csv_data = pd.read_excel(file_name, sheet_name=None)
        entities = []
        for key in csv_data:
            dic_general = {}
            dic_trait = {}
            index_column = 3
            if pd.isnull(csv_data[key].iloc[2, 3]):
                index_column = 4
            if ':' in csv_data[key].iloc[2, index_column]:
                str_temp = csv_data[key].iloc[2, index_column].split(':')[1]
                if '  ' in str_temp:
                    dic_trait['name'] = str_temp.split('  ')[0].strip()
                else:
                    dic_trait['name'] = str_temp.strip()
            if ':' in csv_data[key].iloc[3, index_column]:
                dic_trait['co_trait_name'] = csv_data[key].iloc[3, index_column].split(':')[
                    1].strip()
            if ':' in csv_data[key].iloc[4, index_column]:
                dic_trait['variable_name'] = csv_data[key].iloc[4, index_column].split(':')[
                    1].strip()
            if ' : ' in csv_data[key].iloc[5, index_column]:
                dic_trait['co_id'] = csv_data[key].iloc[5, index_column].split(' : ')[
                    1].strip()
            dic_general["traits"] = dic_trait
            if 'co_id' in dic_trait and dic_trait['co_id'] != '':
                url = f"https://cropontology.org/brapi/v1/variables/{
                    dic_trait['co_id']}"
                request = requests.get(
                    url=url,
                    headers={'Accept': 'application/json'},
                    timeout=5000,
                )
                if request.ok:
                    dic_general['crop_ontologies'] = {
                        'ontology_db_id': request.json()['result']['ontologyDbId'],
                        "name": request.json()['result']['ontologyName']
                    }
                    dic_general['trait_ontologies'] = {
                        'trait_db_id': request.json()['result']['trait']['traitDbId'],
                        "name": request.json()['result']['trait']['name'],
                        "class_family": request.json()['result']['trait']['class'],
                        "description": request.json()['result']['trait']['description']}
                    dic_general['method_ontologies'] = {
                        'method_db_id': request.json()['result']['method']['methodDbId'],
                        "name": request.json()['result']['method']['name'],
                        "class_family": request.json()['result']['method']['class'],
                        "description": request.json()['result']['method']['description'],
                        "formula": request.json()['result']['method']['formula']}
                    dic_general['scale_ontologies'] = {
                        'scale_db_id': request.json()['result']['scale']['scaleDbId'],
                        "name": request.json()['result']['scale']['name'],
                        "data_type": request.json()['result']['scale']['dataType'],
                        "valid_values": str(request.json()['result']['scale']['validValues'])}
                    dic_general['variable_ontologies'] = {
                        'observation_variable_db_id': request.json()['result']['observationVariableDbId'],
                        "name": request.json()['result']['name'],
                        "synonyms": request.json()['result']['synonyms'],
                        "growth_stage": request.json()['result']['growthStage']}
            entities.append(dic_general)
        return entities
    raise FileNotFoundError('Filing to save {file_name} or not exist it')


def get_dictionary_by_entity(
    entity: str,
    head: str,
    csv_dictionary: dict,
    add_hash: bool = False,
    static_row: dict = None,
) -> list:
    """Convert a dictionary in some dictionary with correct type and name of attributes from database

    Args:
        entity (str): name fo entity
        head (str): column of csv to cast by attribute
        csv_dictionary (dict): dict to cast
        add_hash (bool, optional): adding the hash of row. Defaults to False.
        static_row (dict, optional): row static for save. Defaults to None.

    Returns:
        _type_: list of data with name of attributes and correct type to store on database
    """
    array_dictionary = []
    for key in csv_dictionary:
        dictionary_to_save = {}
        for head_key in head:
            column = convert_head_csv_to_column(
                entity, head_csv=head[head_key],
                value=csv_dictionary[key][head_key]
            )
            if column['name'] != 'None':
                dictionary_to_save[column['name']] = column['value']
        if add_hash:
            create_hash = hash(frozenset(csv_dictionary[key].items()))
            dictionary_to_save['hash'] = create_hash
        if static_row:
            for key in static_row:
                dictionary_to_save[key] = static_row[key]
        array_dictionary.append(dictionary_to_save)
    return array_dictionary


def rename_file_csv(path: str, source: str, destiny: str) -> str:
    """Rename some file

    Args:
        path (str): folder of file
        source (str): old name
        destiny (str): new name

    Returns:
        str: new name with path
    """
    os.rename(os.path.join(path, source), os.path.join(path, destiny))
    return os.path.join(path, destiny)


def convert(value: str, to: str, default):
    """cast some value

    Args:
        value (str): value to cast
        to (str): type of cast
        default (_type_): default value

    Returns:
        _type_: return the value casted
    """
    if to == "int":
        try:
            return int(value)
        except ValueError:
            return default


def convert_head_csv_to_column(entity: str, head_csv: str, value: str) -> dict:
    """take entity and head_csv to cast values

    Args:
        entity (str): entity from db
        head_csv (str): name of column on csv
        value (str): value to cast

    Returns:
        dict: dict with value casted
    """
    if entity == 'locations':
        if head_csv == 'Loc_no':
            return {'name': 'number', 'value': int(value)}
        if head_csv == 'Country':
            return {'name': 'country', 'value': str(value)}
        if head_csv == 'Loc. Description':
            return {'name': 'description', 'value': str(value)}
        if head_csv == 'Institute Name':
            return {'name': 'institute_name', 'value': str(value)}
        if head_csv == 'Cooperator':
            return {'name': 'cooperator', 'value': str(value)}
        if head_csv == 'Latitud':
            return {'name': 'latitude', 'value': str(value)}
        if head_csv == 'Lat_degress':
            return {
                'name': 'latitude_degrees',
                'value': convert(value=value, to="int", default=-500),
            }
        if head_csv == 'Lat_minutes':
            return {
                'name': 'latitude_minutes',
                'value': convert(value=value, to="int", default=-500),
            }
        if head_csv == 'Longitude':
            return {'name': 'longitude', 'value': str(value)}
        if head_csv == 'Long_degress':
            return {
                'name': 'longitude_degrees',
                'value': convert(value=value, to="int", default=-500),
            }
        if head_csv == 'Long_minutes':
            return {
                'name': 'longitude_minutes',
                'value': convert(value=value, to="int", default=-500),
            }
        if head_csv == 'Altitude':
            return {'name': 'altitude', 'value': convert(value=value, to="int", default=-500)}
        return {'name': 'None', 'value': 'None'}
    if entity == 'genotypes':
        if head_csv == 'Cid':
            return {'name': 'c_id', 'value': int(value)}
        if head_csv == 'Sid':
            return {'name': 's_id', 'value': int(value)}
        if head_csv == 'Cross Name':
            return {'name': 'cross_name', 'value': str(value)}
        if head_csv == 'Selection History':
            return {'name': 'history_name', 'value': str(value)}
        return {'name': 'None', 'value': 'None'}
    if entity == 'raw_collections':
        return head_csv_raw_collection(head_csv, value)
    if entity == 'env_data':
        return head_csv_env_data(head_csv, value)
    return {'name': 'None', 'value': 'None'}


def head_csv_env_data(head_csv: str, value: str) -> dict:
    """cast value with column name csv from env

    Args:
        head_csv (str): column name
        value (str): value to cast

    Returns:
        dict: dict with values casted
    """
    if head_csv == 'Trial name':
        return {"name": "trial_name", "value": str(value)}
    if head_csv == "Occ":
        return {"name": "occurrence", "value": int(value)}
    if head_csv == "Loc_no":
        return {"name": "location_number", "value": int(value)}
    if head_csv == "Country":
        return {"name": "location_country", "value": str(value)}
    if head_csv == "Loc_desc":
        return {"name": "description", "value": str(value)}
    if head_csv == "Cycle":
        return {"name": "agricultural_cycle", "value": str(value)}
    if head_csv == "Trait No":
        return {"name": "trait_number", "value": str(value)}
    if head_csv == "Trait name":
        return {"name": "trait_name", "value": str(value)}
    if head_csv == "Value":
        return {"name": "value_data", "value": str(value)}
    if head_csv == "Unit":
        return {"name": "unit_name", "value": str(value)}
    return {'name': 'None', 'value': 'None'}


def head_csv_raw_collection(head_csv: str, value: str) -> dict:
    """Convert some value from raw collection to correct type

    Args:
        head_csv (str): column name
        value (str): value to cast

    Returns:
        dict: dict with value casted
    """
    if head_csv == 'Trial name':
        return {'name': 'trial_name', 'value': str(value)}
    if head_csv == 'Occ':
        return {'name': 'field_occurrence', 'value': int(value)}
    if head_csv == 'Loc_no':
        return {'name': 'location_number', 'value': int(value)}
    if head_csv == 'Country':
        return {'name': 'location_country', 'value': str(value)}
    if head_csv == 'Loc_desc':
        return {'name': 'field_description', 'value': str(value)}
    if head_csv == 'Cycle':
        return {'name': 'field_agricultural_cycle', 'value': str(value)}
    if head_csv == 'Cid':
        return {'name': 'genotype_c_id', 'value': int(value)}
    if head_csv == 'Sid':
        return {'name': 'genotype_s_id', 'value': int(value)}
    if head_csv == 'Gen_name':
        return {'name': 'genotype_name', 'value': str(value)}
    if head_csv == 'Trait No':
        return {'name': 'trait_number', 'value': str(value)}
    if head_csv == 'Trait name':
        return {'name': 'trait_name', 'value': str(value)}
    if head_csv == 'Gen_no':
        return {'name': 'genotype_number', 'value': int(value)}
    if head_csv == 'Rep':
        return {'name': 'repetition', 'value': int(value)}
    if head_csv == 'Sub_block':
        return {'name': 'sub_block', 'value': int(value)}
    if head_csv == 'Plot':
        return {'name': 'plot', 'value': int(value)}
    if head_csv == 'Value':
        return {'name': 'value_data', 'value': str(value)}
    if head_csv == 'Unit':
        return {'name': 'unit_name', 'value': str(value)}
    return {'name': 'None', 'value': 'None'}
