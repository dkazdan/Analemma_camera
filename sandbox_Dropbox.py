import dropbox
import os
import psutil
# import shutil
from datetime import datetime

# globals:
Pi_analemma_directory = '/home/DK/Pictures/analemma_to_be_uploaded/'
Pi_analemma_storage_directory = '/home/DK/Pictures/analemma_uploaded/'
# get list of filenames
Pi_uploads = os.listdir(Pi_analemma_directory)

# token stored in file points to NFC_Upload
with open('/home/DK/Documents/analemma_python_code/DBX_token.txt') as f:
    DBX_token = f.read()
#create Dropbox object for the upload
dbx = dropbox.Dropbox(DBX_token)

def upload_new_files_to_dropbox():
    print('starting upload')
    filecount=0
    tock=datetime.now()
    # upload all the files listed
    for filename in Pi_uploads:
        with open(Pi_analemma_directory+filename, "rb") as f:
            dbx.files_upload(f.read(), '/Analemma/'+filename)
        filecount += 1
    tick=datetime.now()
    print('upload complete, ', filecount, 'files transferred')
    print('upload time: ', tick-tock)

def move_files(source, destination):
    tock=datetime.now()
    allfiles = os.listdir(source)
    for f in allfiles:
        src_path=os.path.join(source, f)
        dst_path=os.path.join(destination, f)
        os.rename(src_path, dst_path)
    tick=datetime.now()
    print('transfer time: ', tick-tock)
        
def get_disk_space(): # finds available disk space
    disk = psutil.disk_usage('/')
    total_space = disk.total / (1024 ** 3)  # Convert to GB
    used_space = disk.used / (1024 ** 3)
    free_space = disk.free / (1024 ** 3)
    
    print(f"Total Space: {total_space:.2f} GB")
    print(f"Used Space: {used_space:.2f} GB")
    print(f"Free Space: {free_space:.2f} GB")
    return free_space
    
def get_file_creation_time(file_path):
    # Get file creation time
    return os.path.getctime(file_path)

def delete_files_until_target_size(directory, target_size):
    # Get a list of files in the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    # Sort files by creation time (oldest first)
    files.sort(key=lambda x: get_file_creation_time(os.path.join(directory, x)))
    deleted_size = 0
    # Delete files until reaching the target size
    for file in files:
        file_path = os.path.join(directory, file)
        file_size = os.path.getsize(file_path)
        if deleted_size + file_size <= target_size:
            # Delete the file
            os.remove(file_path)
            deleted_size += file_size
            print(f"Deleted: {file_path}")
        else:
            break

if __name__ == "__main__":
    print('uploading new files to dropbox')
    upload_new_files_to_dropbox()
    
    print('\nmoving files to storage directory')
    move_files(Pi_analemma_directory, Pi_analemma_storage_directory)
    
    print('\nclearing disk space as needed')
    free_disk_space_gb = get_disk_space()
    # print(f'Current disk space: {free_disk_space_gb:.2f} GB')
    # Keep disk usage below specified level. Check transfers weekly!
    target_open_space_gb = 10 # keep 10 GB free for transfers
    if (target_open_space_gb > free_disk_space_gb): # need to clear old files
        free_disk_space_bytes = free_disk_space_gb * (1024 ** 3)
        target_open_space_bytes = target_open_space_gb * (1024 ** 3)
        file_bytes_to_be_deleted=target_open_space_bytes - free_disk_space_bytes
        # Delete files until reaching the target size, starting with oldest
        delete_files_until_target_size(Pi_analemma_storage_directory, file_bytes_to_be_deleted)
    else:
        print ('\nNo directory clearing performed.')
        
    print('\nFile transfers and directory clearing complete.')
        
    
    
    
