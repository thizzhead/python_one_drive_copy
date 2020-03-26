This simple script copies files (currently only .uasset) from one directory to another doing a simple version control based on modification time in a somewhat user friendly environment.

## How to use?
- Open settings.json.
- Fill in the PROJECT_DIRECTORY and ONE_DRIVE_DIRECTORY.
- Run copy_files_to_onedrive.py to copy files from a project to the remote directory (OneDrive) (commit/push?) or copy_files_to_project.py to fetch files from OneDrive to project directory.