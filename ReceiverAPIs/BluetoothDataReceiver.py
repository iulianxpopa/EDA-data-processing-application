import time
import datetime
import threading
import queue
from bitalino import BITalino

class BluetoothDataReceiver():
    """ Creates a data receiver via Bitalino class object,
    a configuration and a data buffer. 

    Keyword arguments:
    receiver_configuration -- a BluetoothReceiverConfiguration object
    which contains the receiver settings from a JSON file. 
    data_buffer -- A Queue through which the received data is
    transmitted forward. 
    """
    def __init__(self, receiver_configuration, data_buffer):
        self.__data_buffer = data_buffer
        self.__receiver_configuration = receiver_configuration        
        self.__communication_queue = None
        self.__receiver_thread = None
        self.__bitalino_device = BITalino(receiver_configuration.macAddress)
        self.t0 = None

    def Start(self):
        """ Starts an 'infinite loop' which will receive and transmit 
        data on a separate thread until the *Stop* method is called.
        """
        # Creates a Bitalino object using the given receiver configuration 
        # and try to connect to the Bitalino device. 
        self.__bitalino_device.start(self.__receiver_configuration.samplingRate, self.__receiver_configuration.acqChannels)
        
        if self.__receiver_thread is None:
            self.__communication_queue = queue.Queue()
            self.__receiver_thread = threading.Thread(target=self.__receiver_loop, args=[])
            self.__receiver_thread.start()
    
    def __receiver_loop(self):
        """ An 'infinite loop' which is stopped by *Stop* method. \n
        This method will get the data received through the Bitalino 
        device and send further via data buffer.
        """
        self.t0 = time.time()

        while True:
            if not self.__communication_queue.empty():
                cmd = self.__communication_queue.get()
                if isinstance(cmd, str) and cmd == 'quit':
                    break
                
            data = self.__bitalino_device.read(self.__receiver_configuration.nSamples)
            self.__data_buffer.put((self.__receiver_configuration.macAddress[-5:].replace(':', ''), data[:,5]))

    def Stop(self):
        """ Stops the 'infinite loop' thread created by *Start* call.
        """
        self.__communication_queue.put('quit')
        self.__receiver_thread.join()
        self.__bitalino_device.stop()
        self.__bitalino_device.close()
        self.__communication_queue = None
        self.__receiver_thread = None
