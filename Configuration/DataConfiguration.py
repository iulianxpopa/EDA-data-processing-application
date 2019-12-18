import logging
import json
import AppContext

class DataConfiguration:
    def __init__(self):
        self.localDirectoryPath = "localDirectoryPath"
        
        self.dropboxAccesToken = "dropboxAccesToken"
        self.dropboxDirectory = "dropboxDirectory"

    def LoadConfiguration(self):
        file = "Configuration/DataConfig.json"
        
        with open(file) as configFile:
            try:
                data = json.load(configFile)
            except ValueError:
                logging.warning(f"{file} can not be decoded as a JSON file.")
                AppContext.message_queue.put('quit')
                return

        self.localDirectoryPath = data["localSave"]["localDirectoryPath"]
        
        self.dropboxAccesToken = data["dropboxSave"]["dropboxAccesToken"]
        self.dropboxDirectory = '/' + data["dropboxSave"]["dropboxDirectory"]
