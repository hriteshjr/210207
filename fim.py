import os
import shutil
import hashlib
import time

directory_to_watch = '/Users/hritesh/Documents/fim/folder'
log_file_path = '/Users/hritesh/Documents/fim/test/logfile.txt'
source_directory = '/Users/hritesh/Documents/fim/folder'
destination_directory = '/Users/hritesh/Documents/fim/test'
tim = {}

# Normal Mode
def normal():
    try:
        while True:
            files_in_directory = os.listdir(directory_to_watch)
            for file in files_in_directory:
                tim[file] = os.path.getmtime(os.path.join(directory_to_watch, file))

            time.sleep(60)
            print("60 Seconds Elapsed...")

            current_files_in_directory = os.listdir(directory_to_watch)

            # check for new files
            new_files = set(current_files_in_directory) - set(files_in_directory)
            for file in new_files:
                print(f'New file added: {file}')
                with open(log_file_path, 'a') as log_file:
                    log_file.write(f'New file added: {file}\n')

            # check for deleted files
            deleted_files = set(files_in_directory) - set(current_files_in_directory)
            for file in deleted_files:
                print(f'File deleted: {file}')
                with open(log_file_path, 'a') as log_file:
                    log_file.write(f'File deleted: {file}\n')

            # check for modified files
            modified_files = set()
            for file in current_files_in_directory:
                if file in files_in_directory:
                    if os.path.getmtime(os.path.join(directory_to_watch, file)) > tim[file]:
                        modified_files.add(file)
            for file in modified_files:
                print(f'File modified: {file}')
                with open(log_file_path, 'a') as log_file:
                    log_file.write(f'File modified: {file}\n')

    except KeyboardInterrupt:
        print("Program stopped by user.")

# Aggressive Mode
def get_file_md5(file_path):
    """
    Returns the MD5 hash of the specified file.
    """
    with open(file_path, 'rb') as f:
        hash_md5 = hashlib.md5()
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def mirror_directory(source, destination):
    """
    Mirrors a directory hierarchy from the source directory to the destination directory,
    renaming files with the content md5 of the original file data.
    """
    for root, dirs, files in os.walk(source):
        destination_dir = root.replace(source, destination)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        for file in files:
            source_file = os.path.join(root, file)
            destination_file = os.path.join(destination_dir, get_file_md5(source_file))
            shutil.copy2(source_file, destination_file)

def aggressive():
    try:
        while True:
            files_in_directory = os.listdir(directory_to_watch)
            for file in files_in_directory:
                tim[file] = os.path.getmtime(os.path.join(directory_to_watch, file))

            mirror_directory(source_directory, destination_directory)

            print("60 Seconds Elapsed...Updating Mirror Directory")
            time.sleep(60)

    except KeyboardInterrupt:
        print("Program stopped by user.")

# Main
print("1- Normal Mode \n2- Aggressive Mode")
choice = int(input("Enter Choice: "))

if choice == 1:
    normal()
elif choice == 2:
    aggressive()
