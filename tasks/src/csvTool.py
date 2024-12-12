"""CSV tools to get information"""
import os
from enum import Enum


class TypeValidate(Enum):
    """Enum of type validation"""
    INT = 1


def fix_csv_remove_character(
        folder: str,
        target_csv: str,
        fixed_file: str = "fixed.csv",
        overwrite: bool = True,
        character_to_delete: str = "\t"
) -> None:
    """Remove character from csv files

    Args:
        folder (str): folder to search
        target_csv (str): csv file to remove
        fixed_file (str, optional): name of file. Defaults to "fixed.csv".
        overwrite (bool, optional): overwrite file. Defaults to True.
        character_to_delete (str, optional): character to delete. Defaults to "\t".
    """
    source_file = os.path.join(folder, target_csv)
    target_file = os.path.join(folder, fixed_file)
    if os.path.exists(target_file):
        os.remove(target_file)
    count = 0
    data_fixed = []
    with os.open(source_file, 'r') as source_csv:
        lines = source_csv.readlines()
        for line in lines:
            count += 1
            if count == 1:
                data_fixed.append(line)
            elif count >= 2:
                array_line = line.split(character_to_delete)
                if count > 12590 and count < 12890:
                    print(line)
                if validate_type(array_line[5], TypeValidate.INT):
                    data_fixed.append(line)
                else:
                    index_start = 2
                    start_index = line.find(
                        array_line[index_start]) + len(array_line[index_start]) + 1
                    index_end = find_agronomic_year(
                        array_line=array_line, start_position=3)
                    if index_end != -1:
                        end_index = line.find(
                            array_line[index_end-1]) - 1
                        new_line = line.replace(
                            line[start_index:end_index],
                            line[start_index:end_index].replace(
                                character_to_delete, "")
                        )
                        data_fixed.append(new_line)
    with open(target_file, 'wb') as target_csv:
        for data in data_fixed:
            target_csv.write(bytes(data, 'utf-8'))
    if overwrite:
        if os.path.exists(source_file):
            os.remove(source_file)
        os.rename(src=target_file, dst=source_file)


def fix_csv_remove_comma(
        folder: str,
        target_csv: str,
        fixed_file: str = "fixed.csv",
        overwrite: bool = True
) -> None:
    """Remove coma from csv file

    Args:
        folder (str): folder to search file
        target_csv (str): file to remove coma
        fixed_file (str, optional): New name of file. Defaults to "fixed.csv".
        overwrite (bool, optional): Overwrite file. Defaults to True.
    """
    source_file = os.path.join(folder, target_csv)
    target_file = os.path.join(folder, fixed_file)
    if os.path.exists(target_file):
        os.remove(target_file)
    with os.open(source_file, 'br') as source_csv, os.open(target_file, 'wb') as target_open_csv:
        lines = source_csv.readlines()
        for line in lines:
            new_line = line.decode('latin-1')
            target_open_csv.write(bytes(new_line.replace(",", ""), 'utf-8'))
    if overwrite:
        if os.path.exists(source_file):
            os.remove(source_file)
        os.rename(src=target_file, dst=source_file)


def find_agronomic_year(array_line: list, start_position: int) -> int:
    """Find agronomic year

    Args:
        array_line (_type_): list of lines to search year
        start_position (int): character position to search

    Returns:
        int: position of year
    """
    for index in range(start_position, len(array_line)):
        if validate_type(array_line[index], TypeValidate.INT):
            return index
    return -1


def validate_type(value: str, type_validate: TypeValidate) -> bool:
    """Validate type 

    Args:
        value (str): value to validate
        type (_type_): _description_

    Returns:
        bool: _description_
    """
    try:
        if type_validate == TypeValidate.INT:
            int(value)
            return True
    except ValueError:
        return False
