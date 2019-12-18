from Configuration.BluetoothReceiverConfiguration import BluetoothReceiverConfiguration
from Configuration.COMPortReceiverConfiguration import COMPortReceiverConfiguration
from ReceiverAPIs.BluetoothDataReceiver import BluetoothDataReceiver
from ReceiverAPIs.COMPortReceiver import COMPortReceiver
from Configuration.DataConfiguration import DataConfiguration
from DataStorageAPIs.DataSaver import DataSaver
from DataStorageAPIs.DropboxUploader import DropboxUpload
from ReceiverAPIs.COMPort import COMPort

import queue
import numpy as np
import logging
import AppContext
import signal
import time

logging.basicConfig(filename="App.log", format="%(levelname)s %(asctime)s %(module)s %(threadName)s: %(message)s",level=logging.INFO)
logging.info('App start')

dataBuffer = queue.Queue()

dataConfig = DataConfiguration()
dataConfig.LoadConfiguration()

dbxUpload = DropboxUpload(dataConfig)

bluetoothConfig = BluetoothReceiverConfiguration()
bluetoothConfig.LoadConfiguration()
comPortConfig = COMPortReceiverConfiguration()
comPortConfig.LoadConfiguration()

COM_Port = COMPort()

#receiver = BluetoothDataReceiver(dataBuffer, bluetoothConfig)
receiver = COMPortReceiver(COM_Port, dataBuffer, comPortConfig)
receiver.Start()

dataSaver = DataSaver(dataConfig, receiver.t0)

def filter(data):
    data[5] = np.where(data[5] > 99, 99, data[5])

while True:
    if not AppContext.message_queue.empty():
        cmd = AppContext.message_queue.get()
        if isinstance(cmd, str) and cmd == 'quit':
            receiver.Stop()
            break
    
    data = dataBuffer.get()
    
    ID = data[0]
    VALUE_Array = data[1]
    TIMESTAMP = time.time() - receiver.t0

    dataSaver.SaveData(ID, TIMESTAMP, VALUE_Array)

#dbxUpload.UploadFolderOnDropbox()

logging.info('App finish')

'''
OSC
Refactor the code
Add more documentation
Filters for an array of data
'''