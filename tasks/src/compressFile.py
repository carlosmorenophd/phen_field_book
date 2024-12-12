"""Unzip files"""
import os

import gzip
import shutil
from zipfile import ZipFile
from pyunpack import Archive


def unzip_file(source_file: str, destiny_folder: str)-> None:
    """Unzip some file

    Args:
        source_file (str): source file to unzip
        destiny_folder (str): folder to unziped
    """

    with ZipFile(source_file, 'r') as zObject:
        zObject.extractall(destiny_folder)
    zObject.close()


def extract_all_gz(directory: str) -> None:
    """Unzip all files in one folder

    Args:
        directory (str): folder to unzip all files
    """
    for file in os.listdir(directory):
        if file.endswith(".gz"):
            gz_path = os.path.join(directory, file)
            print(file)
            extract_path = os.path.join(directory, file.replace(".gz", ""))
            with gzip.open(gz_path, "rb") as inFile, open(
                    extract_path, "wb"
            ) as outfile:
                shutil.copyfileobj(inFile, outfile)
        if file.endswith(".7z"):
            z_path = os.path.join(directory, file)
            Archive(z_path).extractall(directory)
