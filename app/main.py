from workspace.toWork import WorkSpace


def run_project():
    work_space = WorkSpace("/home/Yeiden/Documents/wirk/")
    work_space.work_with_all_zips()
    # work_space.clean_workspace()
    # work_space.prepare_folder_files("dataverse_files.zip")
    # work_space.storage_on_database()


if __name__ == "__main__":
    run_project()
