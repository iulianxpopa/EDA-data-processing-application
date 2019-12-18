import pandas
import time
import datetime
import AppContext

class DataSaver():

    def __init__(self, configuration, t0):
        self._folderName = configuration.localDirectoryPath + '/'
        _datetime = datetime.datetime.fromtimestamp(t0)
        self._fileDatetime = (_datetime).strftime('%Y%m%d_%H%M')

    def SaveData(self, receiverID, currentTimestamp, valuesArray):
        import os
        import sys 

        if not os.path.exists(self._folderName):
            os.makedirs(self._folderName)

        csvFullPath = self._folderName + '/' + self._fileDatetime + '_'+ str(receiverID) + '.txt'

        outputDataframe = self._CreateOutputDataframe(receiverID, currentTimestamp, valuesArray)
        
        if receiverID in AppContext.samples_counter:
            AppContext.samples_counter[receiverID] += 1 
        else:
            AppContext.samples_counter[receiverID] = 1

        self.SaveToTxt(outputDataframe, csvFullPath)
        
        print(AppContext.samples_counter, end='\r')

    def _CreateOutputDataframe(self, receiverID, currentTimestamp, valuesArray):
        auxTimestamp = currentTimestamp
        period = 0

        if len(valuesArray) > 1:
            period = 0.95 / len(valuesArray)

        outputMap = []

        for value in valuesArray:
            outputMap.append([round(auxTimestamp, 5), value])
            auxTimestamp += period
        
        outputDataframe = pandas.DataFrame(outputMap, columns=['Timestamp', 'Value'])

        return outputDataframe

    def SaveToTxt(self, dataframe, csvFullPath):
        dataframe.to_csv(path_or_buf = csvFullPath
                            , sep = ' '
                            , float_format = '%5.5f'
                            , header = False
                            , index = False
                            , mode = 'a'
                            , encoding = 'utf-8'
        )

        
