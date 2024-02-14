"""
Class_analemma_dropbox_handler.py
Class for handling analemma file transfers to Dropbox,
intermediate storage on Pi,
and keeping Pi drive clear enough to verify Dropbox transfers.
Started 12 February 2024
DK
"""

import dropbox
import os
import psutil
from datetime import datetime

class Analemma_dropbox_handler:
# globals:
    Pi_analemma_directory = '/home/DK/Pictures/analemma_to_be_uploaded/'
    Pi_analemma_storage_directory = '/home/DK/Pictures/analemma_uploaded/'
    # get list of filenames
    Pi_uploads = os.listdir(Pi_analemma_directory)
    DBX_token = '' #placemarker, will fill in file read next.
    # token stored in file points to NFC_Upload
    with open('/home/DK/Documents/analemma_python_code/DBX_token.txt') as f:
        DBX_token = f.read()
    #create Dropbox object for the upload
    dbx = dropbox.Dropbox(DBX_token)

    def upload_new_files_to_dropbox(self):
        print('starting upload')
        filecount=0
        tock=datetime.now()
        # upload all the files listed
        for filename in self.Pi_uploads:
            with open(self.Pi_analemma_directory+filename, "rb") as f:
                self.dbx.files_upload(f.read(), '/Analemma/'+filename)
            filecount += 1
        tick=datetime.now()
        print('upload complete, ', filecount, 'files transferred')
        print('upload time: ', tick-tock)

    def move_files(self):
        tock=datetime.now()
        allfiles = os.listdir(self.Pi_analemma_directory)
        for f in allfiles:
            src_path=os.path.join(self.Pi_analemma_directory, f)
            dst_path=os.path.join(self.Pi_analemma_storage_directory, f)
            os.rename(src_path, dst_path)
        tick=datetime.now()
        print('transfer time: ', tick-tock)
        
    def get_disk_space(self): # finds available disk space
        disk = psutil.disk_usage('/')
        total_space = disk.total / (1024 ** 3)  # Convert to GB
        used_space = disk.used / (1024 ** 3)
        free_space = disk.free / (1024 ** 3)
        
        print(f"\nTotal Space: {total_space:.2f} GB")
        print(f"Used Space: {used_space:.2f} GB")
        print(f"Free Space: {free_space:.2f} GB")
        return free_space
        
    def get_file_creation_time(self, file_path): # Get file creation time
        return os.path.getctime(file_path)

    def delete_files_until_target_open_space(self, directory, target_open_space): # space in GB
        free_space = self.get_disk_space()
        if free_space < target_open_space:
            # Get a list of files in the directory
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            # Sort files by creation time (oldest first)
            files.sort(key=lambda x: self.get_file_creation_time(os.path.join(directory, x)))
            deleted_size = 0
            # Delete files until reaching the target open space
            for file in files:
                file_path = os.path.join(directory, file)
                file_size = os.path.getsize(file_path)
                if deleted_size + file_size <= target_open_space: # this will leave space below minimum
                    # Delete the file
                    os.remove(file_path)
                    deleted_size += file_size
                    print(f"Deleted: {file_path}")
                else:
                    break # might print remaining space here
        else:
            print ('open space above target, no files removed')
            
    def dummy_method(self):
        return('return from dummy_method()')


if __name__ == '__main__':
    ADH = Analemma_dropbox_handler()
    ADH.upload_new_files_to_dropbox()
    ADH.move_files()
    #ADH.get_disk_space()
    ADH.delete_files_until_target_open_space('/home/DK/Pictures/analemma_uploaded/', target_open_space=4)