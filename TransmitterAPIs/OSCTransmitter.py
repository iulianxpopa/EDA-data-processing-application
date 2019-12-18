from TransmitterAPIs.IDataTransmitter import IDataTransmitter
import threading
import queue
import osc4py3.as_eventloop as osc
from osc4py3 import oscbuildparse
import time

class OSCTransmitter:
    
    def __init__(self, transmitterBuffer, configuration):
        self._transmitterThread = None
        self._communicationQueue = None

        self._configuration = configuration
        self._transmitterBuffer = transmitterBuffer

    def TransmitterLoop(self, communicationQueue):
        while True:
            print(self._transmitterBuffer)
            time.sleep(1)
            if len(self._transmitterBuffer) is 0:
                continue

            data = self._transmitterBuffer.popleft()
            msg = oscbuildparse.OSCMessage("test/me", ",sif", [data])
            osc.osc_send(msg, 'Gabi')
            osc.osc_process()

            if not communicationQueue.empty():
                cmd = communicationQueue.get()
                if isinstance(cmd, str) and cmd == 'quit':
                    break

    def Start(self):

        
        osc.osc_startup()
        osc.osc_udp_client(self._configuration.ipAddress, self._configuration.port, self._configuration.clientName)
        
        if self._transmitterThread is None:
            self._communicationQueue = queue.Queue()
            self._transmitterThread = threading.Thread(target=self.TransmitterLoop, args=[self._communicationQueue])
            self._transmitterThread.start()
    
    def Stop(self):
        osc.osc_terminate()
        self._communicationQueue.put('quit')
        self._transmitterThread.join()
        self._communicationQueue = None
        self._transmitterThread = None
