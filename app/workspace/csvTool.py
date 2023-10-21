from enum import Enum
from os import path, remove, rename


def fix_csv_remove_commodim(folder: str, target_csv: str, fixed_file: str = "fixed.csv", overwrite: bool = True, commodin: str = "\t"):
    source_file = path.join(folder, target_csv)
    target_file = path.join(folder, fixed_file)
    if path.exists(target_file):
        remove(target_file)
    count = 0
    data_fixed = []
    with open(source_file, 'r') as source_csv:
        lines = source_csv.readlines()
        for line in lines:
            count += 1
            if count == 1:
                data_fixed.append(line)
            elif count >= 2:
                array_line = line.split(commodin)
                if count > 12590 and count < 12890:
                    print(line)
                if validate_type(array_line[5], Type_Validate.INT):
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
                        newLine = line.replace(
                            line[start_index:end_index], line[start_index:end_index].replace(commodin, ""))
                        data_fixed.append(newLine)
    with open(target_file, 'wb') as target_csv:
        for data in data_fixed:
            target_csv.write(bytes(data, 'utf-8'))
    if overwrite:
        if path.exists(source_file):
            remove(source_file)
        rename(src=target_file, dst=source_file)


def fix_csv_remove_comma(folder: str, target_csv: str, fixed_file: str = "fixed.csv", overwrite: bool = True):
    source_file = path.join(folder, target_csv)
    target_file = path.join(folder, fixed_file)
    if path.exists(target_file):
        remove(target_file)
    with open(source_file, 'r') as source_csv, open(target_file, 'wb') as target_csv:
        lines = source_csv.readlines()
        for line in lines:
            target_csv.write(bytes(line.replace(",",""), 'utf-8'))
    if overwrite:
        if path.exists(source_file):
            remove(source_file)
        rename(src=target_file, dst=source_file)


def find_agronomic_year(array_line, start_position: int) -> int:
    for index in range(start_position, len(array_line)):
        if validate_type(array_line[index], Type_Validate.INT):
            return index
    return -1


def validate_type(value: str, type) -> bool:
    try:
        if type == Type_Validate.INT:
            int(value)
            return True
    except ValueError:
        return False


class Type_Validate(Enum):
    INT = 1


if __name__ == "__main__":
    fix_csv_remove_comma(folder="/home/yeiden/Documents/wirk",
                         target_csv="raw.csv", overwrite=False)
