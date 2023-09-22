import os


class PathDirectory:
    def __init__(self, home):
        self.parent_dir = home
        self.work_directory = os.path.join(self.parent_dir, 'work_file')
        self.files_directory = os.path.join(self.parent_dir, 'files')
        if not os.path.isdir(self.work_directory):
            os.mkdir(self.work_directory)

    def get_work_directory(self):
        return self.work_directory

    def get_file_from_file_directory(self, file):
        file_exist = os.path.join(self.files_directory, file)
        if os.path.exists(file_exist):
            return file_exist
        else:
            raise FileNotFoundError('Do not exist this file on file directory')

    def get_one_files_from_directory(self, file):
        return os.path.join(self.files_directory, file)

    def clean_work_directory(self):
        try:
            files = os.listdir(self.work_directory)
            for file in files:
                file_path = os.path.join(self.work_directory, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except OSError:
            raise FileNotFoundError("Error occurred while deleting files.")
