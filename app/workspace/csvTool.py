from enum import Enum
from os import path, remove, rename


def fix_csv_remove_comma(folder: str, target_csv: str, fixed_file: str = "fixed.csv", overwrite: bool = True, commodin: str = "\t"):
    source_file = path.join(folder, target_csv)
    target_file = path.join(folder, fixed_file)
    if path.exists(target_file):
        remove(target_file)
    count = 0
    with open(target_file, 'wb') as target_csv, open(source_file, 'r') as source_csv:
        lines = source_csv.readlines()
        for line in lines:
            count += 1
            print(count)
            if count == 1:
                target_csv.write(bytes(line, 'utf-8'))
            elif count >= 2:
                array_line = line.split(commodin)
                if len(array_line) > 15:
                    if validate_type(array_line[5], Type_Validate.INT):
                        target_csv.write(bytes(line, 'utf-8'))
                    else:
                        # Find the agronomic year
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
                            target_csv.write(bytes(newLine, 'utf-8'))
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
                         target_csv="test.csv", overwrite=False)
