import json
import logging
import AppContext


class COMPortReceiverConfiguration:
    def __init__(self):
        self.BAUDRATE = 9600

    def LoadConfiguration(self):
        file = "Configuration/COMPortReceiverConfig.json"
        
        with open(file) as configFile:
            try:
                config = json.load(configFile)
            except ValueError:
                logging.warning(f"{file} can not be decoded as a JSON file.")
                AppContext.message_queue.put('quit')
                return
        
        self.BAUDRATE = config["BAUDRATE"]