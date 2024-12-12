"""Tools to work with folder and files"""
import os


class PathDirectory:
    """Main class to work with all files 
    """

    def __init__(self, home):
        self.parent_dir = home
        self.path_work = os.path.join(self.parent_dir, 'work_file')
        self.path_files = os.path.join(self.parent_dir, 'files')
        print("Paths")
        print(self.path_work)
        print(self.path_files)
        self.list_files_zip = os.listdir(self.path_files)
        if not os.path.exists(self.path_files):
            os.mkdir(self.path_files)
        if not os.path.isdir(self.path_work):
            os.mkdir(self.path_work)
        os.chmod(self.path_work, 0o0777)

    @property
    def work_directory(self):
        """Get work directory

        Returns:
            _type_: Work directory
        """
        return self.path_work

    @property
    def all_files_zip(self) -> list:
        """Get a list of files

        Returns:
            list: files on zip
        """
        return self.list_files_zip

    @property
    def all_file_csv(self):
        """Get a list of files csv

        Returns:
            _type_: list files csv
        """
        return os.listdir(self.path_work)

    def remove_file(self, file: str) -> None:
        """Remove some file

        Args:
            file (str): file to remove
        """
        file_to_remove = os.path.join(self.path_files, file)
        os.remove(file_to_remove)

    def get_file_from_file_directory(self, file: str) -> str:
        """Get file from work directory

        Args:
            file (_type_): file to get

        Raises:
            FileNotFoundError: File not found

        Returns:
            str: file with all path
        """
        file_exist = os.path.join(self.path_files, file)
        if os.path.exists(file_exist):
            return file_exist
        raise FileNotFoundError(f"Do not exist this file {
                                file} on file directory")

    def get_one_files_from_directory(self, file: str) -> str:
        """Get one file without validation 

        Args:
            file (str): file to search

        Returns:
            str: get file with path
        """
        return os.path.join(self.path_files, file)

    def clean_work_directory(self):
        """Clean work directory from all files

        Raises:
            FileNotFoundError: Some file can't delete
        """
        try:
            files = os.listdir(self.path_work)
            for file in files:
                file_path = os.path.join(self.path_work, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except OSError as error:
            print(f"Error to tray to clean files {error}")
            raise FileNotFoundError(
                "Error occurred while deleting files.") from error
