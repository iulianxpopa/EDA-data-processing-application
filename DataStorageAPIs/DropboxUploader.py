import os
import sys
import dropbox
import json


class DropboxUpload():  
    def __init__(self, configuration):
        self._configuration = configuration

    def UploadFolderOnDropbox(self):
        dbx = dropbox.Dropbox(self._configuration.dropboxAccesToken)

        # enumerate local files recursively
        for root, _ , files in os.walk(self._configuration.localDirectoryPath):
            for filename in files:
                try:
                    # construct the full path of the file
                    filePath = os.path.join(root, filename).replace("\\", "/")

                    # construct the full Dropbox path of the file in the specified folder on dropbox
                    relativePath = os.path.relpath(filePath, self._configuration.localDirectoryPath).replace("\\", "/")
                    destPath = os.path.join(self._configuration.dropboxDirectory, relativePath).replace("\\", "/")

                    print('\033[1m' +'Uploading %s to %s' %  (filePath, destPath), end = '.............................' + '\033[0m')

                    with open(filePath, 'rb') as f:
                        dbx.files_upload(f.read(), destPath, mute=True)
                    
                    print('\033[1m' +'\033[32m' + 'Done' + '\033[0m')

                except Exception as err:
                    print('\033[91m' + 'Error' + '\033[0m')
                    print('\033[91m' + "Failed to upload %s\n%s" % (filename, err) + '\033[0m')
                    
                    
        print('\033[1m' + '\033[92m' +'\nUpload finished! \n'+ '\033[0m')