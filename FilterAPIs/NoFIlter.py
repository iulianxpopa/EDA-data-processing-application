from IDataFilter import IDataFilter
import threading
import queue
from bitalino import BITalino

class NoFilter(IDataFilter):
    
    def __init__(self, receiverBuffer, transmitterBuffer):
        self._filterThread = None
        self._communicationQueue = None
        self._receiverBuffer = receiverBuffer
        self._transmitterBuffer = transmitterBuffer

    def FilterLoop(self, communicationQueue):
        while True:
            self._transmitterBuffer.put(self._receiverBuffer.get())

            if not communicationQueue.empty():
                cmd = communicationQueue.get()
                if isinstance(cmd, str) and cmd == 'quit':
                    break

    def Start(self):
        if self._filterThread is None:
            self._communicationQueue = queue.Queue()
            self._filterThread = threading.Thread(target=self.FilterLoop, args=[self._communicationQueue])
            self._filterThread.start()
    
    def Stop(self):
        self._communicationQueue.put('quit')
        self._filterThread.join()
        self._communicationQueue = None
        self._filterThread = None
