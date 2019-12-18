import logging
import json
import AppContext

class OSCTransmitterConfiguration:
    def __init__(self):
        self.ipAddress = None
        self.port = None
        self.clientName = "ClientName"

    def LoadConfiguration(self):
        file = "Configuration/OSCTransmitterConfig.json"
        
        with open(file) as configFile:
            try:
                data = json.load(configFile)
            except ValueError:
                logging.warning(f"{file} can not be decoded as a JSON file.")
                AppContext.message_queue.put('quit')
                return
        
        self.ipAddress = data["ipAdress"]
        self.port = data["port"]
        self.clientName = data["clientName"]
