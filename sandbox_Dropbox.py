import dropbox
import os
from datetime import datetime

Pi_analemma_directory = '/home/DK/Pictures/analemma_to_be_uploaded/'
Pi_analemma_storage_directory = '/home/DK/Pictures/analemma_uploaded/'
# get list of filenames
Pi_uploads = os.listdir(Pi_analemma_directory)

# token points to NFC_Upload
DBX_token = 'PUT OUR TOKEN HERE'
#create Dropbox object for the upload
dbx = dropbox.Dropbox(DBX_token)

print('starting upload')
tock=datetime.now()
# upload all the files listed
for filename in Pi_uploads:
    with open(Pi_analemma_directory+filename, "rb") as f:
        dbx.files_upload(f.read(), '/Analemma/'+filename)
tick=datetime.now()
print('upload complete.')
print('upload time: ', tick-tock)

def move_files(source, destination):
    allfiles = os.listdir(source)
    for f in allfiles:
        src_path=os.path.join(source, f)
        dst_path=os.path.join(destination, f)
        os.rename(src_path, dst_path)
        
print('\nmoving files to storage directory')
tock=datetime.now()
move_files(Pi_analemma_directory, Pi_analemma_storage_directory)
tick=datetime.now()
print('transfer time: ', tick-tock)
    
    
    