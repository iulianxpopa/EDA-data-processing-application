import time
import datetime
import threading
import queue
import serial

class COMPortReceiver():
    """ Creates a FMCI data receiver using a COMPort object,
    a configuration and a data buffer.  
    
    Keyword arguments:
    COM_port -- A COMPort class object which represents
    the communication serial port. 
    receiver_configuration -- a COMPortReceiverConfiguration object
    which contains the receiver settings from a JSON file. 
    data_buffer -- A Queue through which the received data is
    transmitted forward. 
    """
    def __init__(self, COM_port, receiver_configuration, data_buffer):
        self.__data_buffer = data_buffer
        self.__receiver_configuration = receiver_configuration
        self.__communication_queue = None
        self.__receiver_thread = None
        self.__COM_port = COM_port
        self.__port = None
        self.t0 = None

    def Start(self):
        """ Starts an 'infinite loop' which will receive and transmit 
        data on a separate thread until the *Stop* method is called.
        """
        # Creates a Serial object using the given COMPort object 
        # and the receiver configuration. 
        
        self.__port = serial.Serial(self.__COM_port.port, self.__receiver_configuration.BAUDRATE)

        if self.__receiver_thread is None:
            self.__communication_queue = queue.Queue()
            self.__receiver_thread = threading.Thread(target=self.__receiver_loop, args=[])
            self.__receiver_thread.start()
        
    def __receiver_loop(self):
        """ An 'infinite loop' which is stopped by *Stop* method. \n
        This method will get the data received through the COM
        port, preprocess it and send further via data buffer.
        """
        self.t0 = time.time()
        self.__port.flushInput()

        while True:
            if not self.__communication_queue.empty():
                cmd = self.__communication_queue.get()
                if isinstance(cmd, str) and cmd == 'quit':
                    break

            receivedMessage = self.__port.readline()
            processedData = self.__message_process(receivedMessage)          
            if processedData != None :
                self.__data_buffer.put((processedData[0], [processedData[1]]))
    
    def __message_process(self, data):
        """ Processes the data received through COM port and 
        returns the *ID of transmitter device* and a value
        captured by it.
        """
        decodedMessage = data.decode("utf-8").split(',')
        if len(decodedMessage) == 2: 
            id = str(decodedMessage[0])
            if id != "ID" and id != "GSR":
                value = str(decodedMessage[1][:-2])
                if value != 'error':
                    return (id, value)
        else:
            return None

    def Stop(self):
        """ Stops the 'infinite loop' thread created by *Start* call.
        """
        self.__communication_queue.put('quit')
        self.__receiver_thread.join()
        self.__communication_queue = None
        self.__receiver_thread = None