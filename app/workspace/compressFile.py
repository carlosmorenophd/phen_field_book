import gzip
import os
import shutil
from zipfile import ZipFile


def unzip_file(source_file, destiny_folder):
    with ZipFile(source_file, 'r') as zObject:
        zObject.extractall(destiny_folder)
    zObject.close()


def extract_all_gz(directory):
    for file in os.listdir(directory):
        if file.endswith(".gz"):
            gz_path = os.path.join(directory, file)
            print(file)
            extract_path = os.path.join(directory, file.replace(".gz", ""))
            with gzip.open(gz_path, "rb") as inFile, open(
                    extract_path, "wb"
            ) as outfile:
                shutil.copyfileobj(inFile, outfile)

