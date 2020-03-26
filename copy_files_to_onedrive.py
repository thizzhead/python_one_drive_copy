import os
import shutil
import errno
import time



def split_path(path):
    files = []
    while 1:
        path, f = os.path.split(path)
        if f != "":
            files.append(f)
        else:
            if path != "":
                files.append(path)
            break

    files.reverse()
    
    return files

def copy_file(filepath, destination_path):
    try:
        print(f"Copying new file to {destination_path:200}", end='\r')
        shutil.copy2(filepath, destination_path)
    except IOError as e:
        # ENOENT(2): file does not exist, raised also on missing dest parent dir
        if e.errno != errno.ENOENT:
            raise
        # try creating parent directories
        print(f"Directory {os.path.dirname(destination_path):171} doesn't exist creating one.", end='\r')
        os.makedirs(os.path.dirname(destination_path))
        # copy the file once the directory exists
        print(f"Copying new file to {destination_path:200}", end='\r')
        shutil.copy2(filepath, destination_path)

def get_one_files(one_drive_project_directory):

    one_files = []

    for root, dirs, files in os.walk(one_drive_project_directory):
        for file in files:
            file_relative = os.path.relpath(os.path.join(root, file), one_drive_project_directory)
            one_files.append(file_relative)
    return one_files

def get_project_files(project_directory):
    project_files = []

    for root, dirs, files in os.walk(project_directory):
        for file in files:
            if file.endswith(".uasset"):
                file_relative = os.path.relpath(os.path.join(root, file), project_directory)
                project_files.append(file_relative)
    return project_files

def main():
    import json

    start_time = time.time()

    settings_dict = {}

    with open("settings.json", "r") as f:
        settings_dict = json.load(f)

    PROJECT_DIRECTORY = settings_dict['PROJECT_DIRECTORY']
    ONE_DRIVE_DIRECTORY = settings_dict['ONE_DRIVE_DIRECTORY']

    count_new_files = 0
    count_changes = 0
    count_files_removed = 0
                
    one_files = get_one_files(os.path.join(ONE_DRIVE_DIRECTORY, split_path(PROJECT_DIRECTORY)[-1]))
    project_files = get_project_files(PROJECT_DIRECTORY)

    # Remove files
    for one_file in one_files:
        exists = False
        for file in project_files:
            if file == one_file:
                exists = True
        if not exists:
            os.remove(os.path.join(ONE_DRIVE_DIRECTORY, split_path(PROJECT_DIRECTORY)[-1], one_file))
            count_files_removed += 1

    for file in project_files:
        match = None
        for one_file in one_files:
            if file == one_file:
                match = one_file

        if match:
            if os.path.getmtime(os.path.join(PROJECT_DIRECTORY, file)) > os.path.getmtime(os.path.join(ONE_DRIVE_DIRECTORY, split_path(PROJECT_DIRECTORY)[-1], match)):
                copy_file(os.path.join(PROJECT_DIRECTORY, file), os.path.join(ONE_DRIVE_DIRECTORY, split_path(PROJECT_DIRECTORY)[-1], match))
                count_changes += 1
        else:
            copy_file(os.path.join(PROJECT_DIRECTORY, file), os.path.join(ONE_DRIVE_DIRECTORY, split_path(PROJECT_DIRECTORY)[-1], file))
            count_new_files += 1

    print(f"{' ':300}", end='\r')

    end_time = time.time()
    
    print(f"Added {count_new_files} new files, {count_changes} files have been modified, {count_files_removed} files have been removed")
    print(f"Time elapsed: {end_time-start_time} seconds")


if __name__ == "__main__":
    main()