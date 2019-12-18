import logging
import json
import AppContext

class BluetoothReceiverConfiguration:
    def __init__(self):
        self.macAddress = "00:00:00:00:00:00"
        self.acqChannels = []
        self.samplingRate = 1000
        self.nSamples = 5

    def LoadConfiguration(self):
        file = "Configuration/BluetoothReceiverConfig.json"
        
        with open(file) as configFile:
            try:
                config = json.load(configFile)
            except ValueError:
                logging.warning(f"{file} can not be decoded as a JSON file.")
                AppContext.message_queue.put('quit')
                return
        
        self.macAddress = config["macAddress"]
        self.acqChannels = config["acqChannels"]
        self.samplingRate = config["samplingRate"]
        self.nSamples = config["nSamples"]
