from copy_files_to_onedrive import copy_file, split_path, get_one_files, get_project_files
import time
import os

def main():
    import json

    start_time = time.time()

    settings_dict = {}

    with open("settings.json", "r") as f:
        settings_dict = json.load(f)

    PROJECT_DIRECTORY = settings_dict['PROJECT_DIRECTORY']
    ONE_DRIVE_DIRECTORY = settings_dict['ONE_DRIVE_DIRECTORY']

    count_new_files = 0
    count_files_updated = 0
    count_files_uptodate = 0
    count_files_removed = 0

    project_files = get_project_files(PROJECT_DIRECTORY)
    project_name = split_path(PROJECT_DIRECTORY)[-1]
    one_files = get_one_files(os.path.join(ONE_DRIVE_DIRECTORY, project_name))

    choice = 'u'
    
    for one_file in one_files:
        exists = False
        one_file_path = os.path.join(os.path.join(ONE_DRIVE_DIRECTORY, project_name, one_file))
        for project_file in project_files:
            if one_file == project_file:
                exists = True
                one_file_mtime = os.path.getmtime(one_file_path)
                project_file_mtime = os.path.getmtime(os.path.join(PROJECT_DIRECTORY, project_file))
                dest_dir = os.path.join(PROJECT_DIRECTORY, split_path(project_file)[-1])
                if one_file_mtime > project_file_mtime:
                    print(f"Replacing {one_file} in {dest_dir}. {' ':100}", end='\r')
                    copy_file(one_file_path, dest_dir)
                    count_files_updated += 1
                elif one_file_mtime < project_file_mtime:
                    if choice == 'y' or choice == 'n' or choice == 'u':
                        print(f"There is already a newer version of {one_file} present in {dest_dir}.")
                        choice = str.lower(input("Do you want to overwrite it? (y = Yes, n = No, a = Yes to all, anything else to ignore all): "))

                        if choice == 'y' or choice == 'a':
                            print(f"Replacing {one_file}. On user request.{' ':200}", end='\r')
                            copy_file(one_file_path, dest_dir)
                            count_files_updated += 1
                        else: 
                            print(f"Skipping {one_file}. On user request.{' ':200}", end='\r')
                            count_files_uptodate += 1
                            
                    elif choice == "a":
                        print(f"Replacing {one_file}. On user request. (Replace all){' ':200}", end='\r')
                        copy_file(one_file_path, dest_dir)
                        count_files_updated += 1
                    else:
                        print(f"Skipping {one_file}. On user request. (Skip all){' ':200}", end='\r')
                        count_files_uptodate += 1
                else:
                    print(f"This is the newest version of {one_file}. Skipping.{' ':100}", end='\r')
                    count_files_uptodate += 1
        if not exists:
            dest_dir = os.path.join(PROJECT_DIRECTORY, one_file)
            print(f"Copying {one_file} to {dest_dir}. {' ':100}", end='\r')
            copy_file(one_file_path, dest_dir)
            count_new_files += 1
    
    choice = "u"

    for project_file in project_files:
        exists = False
        for one_file in one_files:
            if project_file == one_file:
                exists = True
        if not exists:
            if choice == 'u' or choice == 'k' or choice == 'r':
                print(f"File {project_file} appears in the project directory but not on the remote.{' ':100}")
                choice = str.lower(input("What do you want to do with it? (k = Keep it, r = Remove it, a = Remove all, anything else to keep all): "))
                
                if choice == 'r' or choice == 'a':
                    print(f"Removing {project_file} from {PROJECT_DIRECTORY}{' ':100}", end='\r')
                    count_files_removed += 1
                    os.remove(os.path.join(PROJECT_DIRECTORY, project_file))
                else:
                    print(f"Keeping {project_file}{' ':100}", end='\r')

            elif choice == 'a':
                print(f"Removing all [{project_file}] from {PROJECT_DIRECTORY}{' ':100}", end='\r')
                count_files_removed += 1
                os.remove(os.path.join(PROJECT_DIRECTORY, project_file))
            else: 
                print(f"Keeping all [{project_file}]{' ':100}", end='\r')

    
    end_time = time.time()

    print(f"{' ':400}", end='\r')
    print("Project update finished.")
    print(f"Amount of files: \n\t- Added: {count_new_files} \n\t- Updated: {count_files_updated} \n\t- Up-to-date: {count_files_uptodate} \n\t- Removed: {count_files_removed}")
    print(f"Time elapsed: {end_time-start_time} seconds")
    print()

if __name__ == "__main__":
    main()