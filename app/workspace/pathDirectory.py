import os


class PathDirectory:
    def __init__(self, home):
        self.parent_dir = home
        self.path_work = os.path.join(self.parent_dir, 'work_file')
        self.path_files = os.path.join(self.parent_dir, 'files')
        self.list_files_zip = os.listdir(self.path_files)
        if not os.path.isdir(self.path_work):
            os.mkdir(self.path_work)

    def get_work_directory(self):
        return self.path_work

    def get_all_files_zip(self):
        return self.list_files_zip

    def get_all_file_csv(self):
        return os.listdir(self.path_work)

    def remove_file(self, file):
        file_to_remove = os.path.join(self.path_files, file)
        os.remove(file_to_remove)

    def get_file_from_file_directory(self, file):
        file_exist = os.path.join(self.path_files, file)
        if os.path.exists(file_exist):
            return file_exist
        else:
            raise FileNotFoundError('Do not exist this file on file directory')

    def get_one_files_from_directory(self, file):
        return os.path.join(self.path_files, file)

    def clean_work_directory(self):
        try:
            files = os.listdir(self.path_work)
            for file in files:
                file_path = os.path.join(self.path_work, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except OSError:
            raise FileNotFoundError("Error occurred while deleting files.")
