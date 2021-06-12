import string
import random
import numpy as np
import pandas as pd
import datetime as datetime
import re
import math
import sys
sys.path.append('../yamlhandler')
from yamlhandler import YamlHandler


class Datagen:

    validVarTypes = ['categorical', 'cluster', 'range', 'time', 'timestamp']
    validErrorTypes = ['NV', 'WT', 'O']

    def __init__(self, pYamlFilePath, pSize):
        self.yamlHandler = YamlHandler(re.sub(r'\\+', r'/', pYamlFilePath.encode("unicode_escape").decode("utf-8")))
        self.configDict = self.yamlHandler.getDataConfig()
        self.size = pSize
        self.columnNames = []
        self.createColumnNames()
        self.dataframe = pd.DataFrame(columns=self.columnNames)
        self.fillColumns()
        if self.yamlHandler.getRelationsConfig() is not None:
            self.createRelations()

    # TODO
    def validateConfigDict(self):
        # if cluster var all lists in dictItem['vals'] have to contain the same datatype e.g. float
        # if categorical var all categories have to be boolean or string type
        return True

    def createColumnNames(self):
        for x, y in self.configDict.items():
            if y['count'] > 1:
                self.generateNames(name=x, count=y['count'])
            else:
                self.columnNames.append(x)

    def generateNames(self, name, count):
        for x in range(count):
            self.columnNames.append(name + '_' + str(x + 1))

    def fillColumns(self):
        # Column index
        counter = 0
        # Loop through all configDict items
        for key, dictItem in self.configDict.items():
            # Column values in current configDict item
            tmpColumnValues = 0
            # Count value in current item
            tmpCount = dictItem['count']
            # Loop count times
            for x in range(tmpCount):
                # If item is type range
                if dictItem['type'] == 'range':
                    tmpColumnValues = self.createRangeVar(dictItem['vals'], dictItem['dups'])
                # If item is type categorical
                if dictItem['type'] == 'categorical':
                    tmpColumnValues = self.createCategoricalVar(pCategories=dictItem.get('vals'),
                                                                pProb=dictItem.get('prob', None))
                # If item is type cluster
                if dictItem['type'] == 'cluster':
                    tmpColumnValues = self.createClusterVar(dictItem['vals'], pProb=dictItem.get('prob', None))
                # If item is type timestamp
                if dictItem['type'] == 'timestamp':
                    tmpColumnValues = self.createTimestampVar(dictItem['vals'], pFormat=dictItem.get('format', None))
                # If item is type time
                if dictItem['type'] == 'time':
                    tmpColumnValues = self.createTimeVar(dictItem['vals'])

                # Cast numpy ndarray to pandas series
                tmpColumnValues = pd.Series(tmpColumnValues)

                # Check if errors should be included
                if dictItem.get('errorRate', None) is not None:
                    tmpColumnValues = self.createErrors(tmpColumnValues, dictItem.get('type'), dictItem.get('vals'),
                                                        dictItem.get('errorRate', None),
                                                        dictItem.get('errorType', None))
                # Add values to column
                self.dataframe.iloc[:, counter] = tmpColumnValues
                # Add 1 to column index counter
                counter += 1

    def createErrors(self, pColumn, pColumnType, pVals, pErrorRate=None, pErrorType=None):
        # Creates N% samples from given column
        tmpSamples = pColumn.sample(frac=pErrorRate)

        translator = {'NV': self.createNVError,
                      'WT': self.createWTError,
                      'O': self.createOError}

        for x in tmpSamples.index:
            # Invokes functions in list randomly and fills samples with random errors
            tmpSamples[x] = translator[np.random.choice(pErrorType)](pColumnType, pVals)

        pColumn.loc[tmpSamples.index] = tmpSamples
        return pColumn

    def createRangeVar(self, pVals, pReplace=True):
        return np.random.choice(a=self.ownRange(pVals[0], pVals[1]), size=self.size, replace=pReplace)

    def createCategoricalVar(self, pCategories, pReplace=True, pProb=None):
        return np.random.choice(a=pCategories, size=self.size, replace=pReplace, p=pProb)

    def createClusterVar(self, pVals, pProb=None):
        tmpValues = []
        clusterCount = len(pVals)

        if pProb is not None:
            for i in range(len(pProb)):
                pProb[i] = round(pProb[i] * self.size)
            clusterSizes = pProb
        else:
            clusterSizes = np.random.multinomial(self.size, np.ones(clusterCount) / clusterCount, size=1)[0]

        for x in range(clusterCount):
            tmpValues.extend(np.random.choice(a=self.ownRange(pVals[x][0], pVals[x][1]), size=clusterSizes[x], replace=True))
        np.random.shuffle(tmpValues)
        return tmpValues

    # TODO
    #  wenn Anzahl Zeilen kleiner ist als angegebener Zeitraum, d.h. Zeilenzahl 20
    #  und Tageanzahl 30, muss ein Fehler geworfen werden oder eine Lösung
    def createTimestampVar(self, pVals, pFormat=None):
        # Creates n random numbers between 0 and 86400
        intTimes = np.random.choice(a=range(0, 86400), size=self.size, replace=True)
        # Casts numbers into times 0 -> 00:00:00, 86400 -> 24:00:00
        times = pd.to_datetime(intTimes, unit='s').time
        # Creates dates in given range
        dates = pd.date_range(pVals[0], pVals[1]).to_pydatetime()
        combined = []

        # TODO
        #  If date format only uses dates oder times don't combine dates and times.
        #  This will save some execution time
        # randomly combines dates and times 
        if len(times) > len(dates):
            # Combines dates with random chosen times
            for x in range(len(times)):
                combined.append(datetime.datetime.combine(np.random.choice(a=dates, size=1, replace=True)[0], times[x]))
        else:
            # Combines times with random chosen dates
            for x in range(len(dates)):
                combined.append(datetime.datetime.combine(dates[x], np.random.choice(a=times, size=1, replace=True)[0]))

        if pFormat is not None:
            for i in range(len(combined)):
                combined[i] = combined[i].strftime(pFormat)
        return combined

    def createTimeVar(self, pVals, pReplace=True):
        intTimes = self.createRangeVar(pVals, pReplace)
        times = pd.to_datetime(intTimes, unit='s').time
        return times

    # Temporary solution -> Bisher wird nur lower geprüft, upper sollte auch geprüft werden
    def ownRange(self, lower, upper):
        if isinstance(lower, float):
            return np.arange(lower, upper, step=0.1)
        if isinstance(lower, int):
            return range(lower, upper)

    def createNVError(self, pColumnType, pVals):
        return np.nan

    def createWTError(self, pColumnType, pVals):
        typeRef = None
        returnVal = None
        if isinstance(pVals[0], list):
            typeRef = pVals[0][0]
        else:
            typeRef = pVals[0]

        if isinstance(typeRef, (int, float, complex, bool)):
            returnVal = ''.join(random.choice(string.ascii_letters) for n in range(8))
        if isinstance(typeRef, str):
            returnVal = int(''.join(random.choice(string.digits) for n in range(8)))
        return returnVal

    def createOError(self, pColumnType, pVals):
        returnVal = None

        if pColumnType == 'categorical':
            # Outlier necessary?
            returnVal = None

        if pColumnType == 'cluster':
            tmpVals = []
            for x in range(len(pVals)):
                if x < (len(pVals) - 1):
                    tmpMedian = np.median([pVals[x][1], pVals[(x + 1)][0]])
                    tmpVals.insert(x, np.random.choice(self.ownRange(tmpMedian * 0.9, tmpMedian * 1.1)))
            returnVal = np.random.choice(tmpVals)

        if pColumnType == 'range':
            returnVal = self.createValOutOfList(pVals)

        if pColumnType == 'time':
            returnVal = pd.to_datetime(self.createValOutOfList(pVals), unit='s').time()

        if pColumnType == 'timestamp':
            # Outlier necessary?
            returnVal = None
        return returnVal

    def createValOutOfList(self, pRange):
        # Lower
        lowerVal = np.random.randint(low=(pRange[0] * 0.5), high=(pRange[0] * 0.9))
        # Higher
        higherVal = np.random.randint(low=(pRange[1] * 1.1), high=(pRange[1] * 1.5))
        # Return random choice
        return np.random.choice([lowerVal, higherVal])

    def createRelations(self):
        # list to safe used indices in dataframe
        tmpUsedIndices = []
        # loop to loop trough all relations
        for key, value in self.yamlHandler.getRelationsConfig().items():
            if not self.yamlHandler.overlap:
                # creates dataframe with unused indices from original dataframe
                tmpDataframe = self.dataframe[~self.dataframe.index.isin(tmpUsedIndices)]
            else:
                tmpDataframe = self.dataframe
            rowsTrueCond = tmpDataframe[tmpDataframe.eval(value['if'])]
            # creates N samples from dataframe with unused indices
            samples = rowsTrueCond.sample(n=math.floor(len(rowsTrueCond) * value['proportion']))
            # apply relation rule to samples
            samples[value['target']] = value['then']
            # adds modified samples to original dataframe
            self.dataframe.loc[samples.index] = samples
            # adds used indices to indices-list
            tmpUsedIndices.extend(list(samples.index))
