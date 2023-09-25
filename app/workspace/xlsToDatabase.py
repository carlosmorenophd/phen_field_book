import os
import pandas as pd
import requests
import re


def get_locations(path, list_csv_files):
    source = search_file_by_regex(list_files=list_csv_files, end_with="Loc_data.xls")
    file_name = rename_file_csv(path=path, source=source, destiny='location.csv')
    if os.path.isfile(file_name):
        csv_data = pd.read_csv(file_name, delimiter='\t', engine='python', header=None, )
        csv_dictionary = csv_data.to_dict('index')
        head = csv_dictionary.pop(0)
        return get_dictionary_by_entity(entity='locations', head=head, csv_dictionary=csv_dictionary)
    else:
        raise FileNotFoundError('Filing to save file or not exist it')


def search_file_by_regex(list_files, end_with, end_with_double: str = ""):
    for file in list_files:
        x = re.search("{}$".format(end_with), file)
        if x:
            return file
        if end_with_double != "":
            x = re.search("{}$".format(end_with_double), file)
            if x:
                return file
    raise FileNotFoundError("Can not find the file to work - {}".format(end_with))


def get_genotypes(path, list_csv_files):
    source = search_file_by_regex(list_files=list_csv_files, end_with="Genotypes_Data.xls")
    file_name = rename_file_csv(path=path, source=source, destiny='genotypes.csv')
    if os.path.isfile(file_name):
        csv_data = pd.read_csv(file_name, delimiter='\t', engine='python', header=None, encoding='ISO-8859-1')
        csv_dictionary = csv_data.to_dict('index')
        head = csv_dictionary.pop(0)
        return get_dictionary_by_entity(entity='genotypes', head=head, csv_dictionary=csv_dictionary)
    else:
        raise FileNotFoundError('Filing to save file or not exist it')


def get_raw_collections(path, list_csv_files):
    source = search_file_by_regex(list_files=list_csv_files, end_with="RawData.xls")
    file_name = rename_file_csv(path=path, source=source, destiny='raw.csv')
    if os.path.isfile(file_name):
        csv_data = pd.read_csv(file_name, delimiter='\t', engine='python', header=None, encoding='ISO-8859-1')
        csv_dictionary = csv_data.to_dict('index')
        head = csv_dictionary.pop(0)
        return get_dictionary_by_entity(entity='raw_collections', head=head, csv_dictionary=csv_dictionary, add_hash=True)
    else:
        raise FileNotFoundError('Filing to save file or not exist it')


def get_trait_details(path, list_csv_files):
    source = search_file_by_regex(list_files=list_csv_files, end_with="IDYN.xls", end_with_double="IDYN.xlsx")
    print(source)
    file_name = os.path.join(path, source)
    if os.path.isfile(file_name):
        csv_data = pd.read_excel(file_name, sheet_name=None)
        entities = []
        for key in csv_data:
            dic_general = {}
            dic_trait = {}
            if ':' in csv_data[key].iloc[2, 3]:
                str_temp = csv_data[key].iloc[2, 3].split(':')[1]
                if '  ' in str_temp:
                    dic_trait['name'] = str_temp.split('  ')[0].strip()
                else:
                    dic_trait['name'] = str_temp.strip()
            if ':' in csv_data[key].iloc[3, 3]:
                dic_trait['co_trait_name'] = csv_data[key].iloc[3, 3].split(':')[1].strip()
            if ':' in csv_data[key].iloc[4, 3]:
                dic_trait['variable_name'] = csv_data[key].iloc[4, 3].split(':')[1].strip()
            if ' : ' in csv_data[key].iloc[5, 3]:
                dic_trait['co_id'] = csv_data[key].iloc[5, 3].split(' : ')[1].strip()
            dic_general["traits"] = dic_trait
            if 'co_id' in dic_trait and dic_trait['co_id'] != '':
                url = 'https://cropontology.org/brapi/v1/variables/%s' % dic_trait['co_id']
                r = requests.get(url=url, headers={'Accept': 'application/json'})
                dic_general['crop_ontologies'] = {'ontology_db_id': r.json()['result']['ontologyDbId'],
                                                  "name": r.json()['result']['ontologyName']}
                dic_general['trait_ontologies'] = {'trait_db_id': r.json()['result']['trait']['traitDbId'],
                                                   "name": r.json()['result']['trait']['name'],
                                                   "class_family": r.json()['result']['trait']['class'],
                                                   "description": r.json()['result']['trait']['description']}
                dic_general['method_ontologies'] = {'method_db_id': r.json()['result']['method']['methodDbId'],
                                                    "name": r.json()['result']['method']['name'],
                                                    "class_family": r.json()['result']['method']['class'],
                                                    "description": r.json()['result']['method']['description'],
                                                    "formula": r.json()['result']['method']['formula']}
                dic_general['scale_ontologies'] = {'scale_db_id': r.json()['result']['scale']['scaleDbId'],
                                                   "name": r.json()['result']['scale']['name'],
                                                   "data_type": r.json()['result']['scale']['dataType'],
                                                   "valid_values": str(r.json()['result']['scale']['validValues'])}
                dic_general['variable_ontologies'] = {
                    'observation_variable_db_id': r.json()['result']['observationVariableDbId'],
                    "name": r.json()['result']['name'],
                    "synonyms": r.json()['result']['synonyms'],
                    "growth_stage": r.json()['result']['growthStage']}
            entities.append(dic_general)
        return entities
    else:
        raise FileNotFoundError('Filing to save file or not exist it')


def get_dictionary_by_entity(entity, head, csv_dictionary, add_hash: bool = False ):
    array_dictionary = []
    for key in csv_dictionary:
        dictionary_to_save = {}
        for head_key in head:
            column = convert_head_csv_to_column(entity, head_csv=head[head_key],
                                                value=csv_dictionary[key][head_key])
            if column['name'] != 'None':
                dictionary_to_save[column['name']] = column['value']
        if add_hash:
            create_hash = hash(frozenset(csv_dictionary[key].items()))
            # print (create_hash.items())
            # print(hash(frozenset(create_hash.items())))
            dictionary_to_save['hash'] = create_hash
        array_dictionary.append(dictionary_to_save)
    return array_dictionary


def rename_file_csv(path, source, destiny):
    os.rename(os.path.join(path, source), os.path.join(path, destiny))
    return os.path.join(path, destiny)


def convert_head_csv_to_column(entity, head_csv, value):
    if entity == 'locations':
        if head_csv == 'Loc_no':
            return {'name': 'number', 'value': int(value)}
        elif head_csv == 'Country':
            return {'name': 'country', 'value': str(value)}
        elif head_csv == 'Loc. Description':
            return {'name': 'description', 'value': str(value)}
        elif head_csv == 'Institute Name':
            return {'name': 'institute_name', 'value': str(value)}
        elif head_csv == 'Cooperator':
            return {'name': 'cooperator', 'value': str(value)}
        elif head_csv == 'Latitud':
            return {'name': 'latitude', 'value': str(value)}
        elif head_csv == 'Lat_degress':
            return {'name': 'latitude_degrees', 'value': int(value)}
        elif head_csv == 'Lat_minutes':
            return {'name': 'latitude_minutes', 'value': int(value)}
        elif head_csv == 'Longitude':
            return {'name': 'longitude', 'value': str(value)}
        elif head_csv == 'Long_degress':
            return {'name': 'longitude_degrees', 'value': int(value)}
        elif head_csv == 'Long_minutes':
            return {'name': 'longitude_minutes', 'value': int(value)}
        elif head_csv == 'Altitude':
            return {'name': 'altitude', 'value': int(value)}
        else:
            return {'name': 'None', 'value': 'None'}
    elif entity == 'genotypes':
        if head_csv == 'Cid':
            return {'name': 'c_id', 'value': int(value)}
        elif head_csv == 'Sid':
            return {'name': 's_id', 'value': int(value)}
        elif head_csv == 'Cross Name':
            return {'name': 'cross_name', 'value': str(value)}
        elif head_csv == 'Selection History':
            return {'name': 'history_name', 'value': str(value)}
        else:
            return {'name': 'None', 'value': 'None'}
    elif entity == 'raw_collections':
        if head_csv == 'Trial name':
            return {'name': 'trails.name', 'value': str(value)}
        elif head_csv == 'Occ':
            return {'name': 'occurrence', 'value': int(value)}
        elif head_csv == 'Loc_no':
            return {'name': 'locations.number', 'value': int(value)}
        elif head_csv == 'Country':
            return {'name': 'locations.country', 'value': str(value)}
        elif head_csv == 'Loc_desc':
            return {'name': 'locations.description', 'value': str(value)}
        elif head_csv == 'Cycle':
            return {'name': 'cycle', 'value': str(value)}
        elif head_csv == 'Cid':
            return {'name': 'genotypes.c_id', 'value': str(value)}
        elif head_csv == 'Sid':
            return {'name': 'genotypes.s_id', 'value': str(value)}
        elif head_csv == 'Gen_name':
            return {'name': 'genotypes.cross_name', 'value': str(value)}
        elif head_csv == 'Trait No':
            return {'name': 'traits.trait_number', 'value': str(value)}
        elif head_csv == 'Trait name':
            return {'name': 'traits.name', 'value': str(value)}
        elif head_csv == 'Gen_no':
            return {'name': 'gen_number', 'value': int(value)}
        elif head_csv == 'Rep':
            return {'name': 'repetition', 'value': int(value)}
        elif head_csv == 'Sub_block':
            return {'name': 'sub_block', 'value': int(value)}
        elif head_csv == 'Plot':
            return {'name': 'plot', 'value': int(value)}
        elif head_csv == 'Value':
            return {'name': 'value_data', 'value': str(value)}
        elif head_csv == 'Unit':
            return {'name': 'units.name', 'value': str(value)}
        else:
            return {'name': 'None', 'value': 'None'}
    else:
        return {'name': 'None', 'value': 'None'}
