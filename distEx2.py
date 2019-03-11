import json, ast, yaml
import array
import math
import decimal

from pprint import pprint
from pprint import pformat
from optparse import OptionParser
from math import ceil
from math import log

import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy.special as sps
import pdb

class Iter2D:
        """
        a class used to create an iterator of the n-th elemnts
        of a list of tuples (lot) (or any two dimensional object in python).
        """
        def __init__(self, lot, n):
            self.lot=lot
            self.index=0
            self.n=n

        def __iter__(self):
            return self

        def __next__(self):
            try:
                result = self.lot[self.index][self.n]
            except IndexError:
                raise StopIteration
            self.index += 1
            return result

        def iter(self):
            return self.__iter__()

        def next(self):
            return self.__next__()

class Dist2:
    """"
    A simle class representing a distribution.
    methods:
        empDistFun(): calculates the values of the Empirical Distribution Function
        dump(): dumps the contents of a single object
    """
    def __init__(self, data, iD):
        print("A Dist2 instance")
        # self.data = data
        # clean unicode chars from dict
        self.data = ast.literal_eval(json.dumps(data))
        self.iD = iD
        self.outputFile="dist.%s.png" % iD
        # explicitly calculate the lenth of the sample and
        # correct eventual typos in the .json file
        self.data['l']=len(self.data['ni'])
        # explicitly calculate the sample volume and
        # correct eventual typos in the .json file
        self.data['n']=sum(self.data['ni'])

        # Full binsRange
        binsRange=(self.data['xmin'], self.data['xmax'])
        self.binsRange=binsRange

        numBins=self.data['l']
        self.numBins=numBins

        # create the figure
        self.figure=plt.figure(num=None, figsize=(15, 12), dpi=80)

    def parMom(self):
        """
        Estimate distribution parameters from the sample
        using the 'Method of moments'
        """

        binWidth=(self.data['xmax']-self.data['xmin'])/self.data['l']
        binsEdges=range(self.data['xmin'], self.data['xmax'] + binWidth, binWidth)

        # estimate binTuples per bin
        edge1=None
        edge2=None
        binTuples=[]
        binCount=0
        binHits=None
        binAvr=None
        empProb=None
        relFreq=None
        binExpVal=None
        for edge in binsEdges:
            edge1=edge2
            edge2=edge
            if edge1 and edge2:
                binHits=self.data['ni'][binCount]
                binAvr=(edge1+edge2)/2.
                empProb=float(binHits)/self.data['n']
                relFreq=float(empProb)/binWidth
                binExpVal=binAvr*empProb
                binTuples.append((binCount,    # 0
                                  edge1,       # 1
                                  edge2,       # 2
                                  binHits,     # 3
                                  binAvr,      # 4
                                  empProb,     # 5
                                  binExpVal,   # 6
                              ))
                binCount += 1

        expVal=sum(Iter2D(binTuples, 6))
        self.data['expVal']=expVal

        edge1=None
        edge2=None
        binDev=None
        binDevSq=None
        binDisp=None
        for i, binn in enumerate(binTuples):
            binDev=binn[4]-expVal
            binDevSq=binDev**2
            binDisp=binDevSq*binn[5]
            binTuples[i] = binn + (binDev, binDevSq, binDisp)
        self.data['binTuples']=binTuples

        # Estimate Normal Distribution parameters:
        variance=sum(Iter2D(binTuples,9))
        self.data['variance']=variance

        stDev=math.sqrt(variance)
        self.data['stDev']=stDev

        # Estimate Unform Distribution parameters:
        uniLimMin=expVal-stDev*math.sqrt(3)
        uniLimMax=expVal+stDev*math.sqrt(3)
        self.data['uniLimMin']=uniLimMin
        self.data['uniLimMax']=uniLimMax

        # artificially generate sample with the porper number of entries per bin
        # matplotlib cannot plot histograms in ranges - it expects a full sample
        sample=[]
        for binn in binTuples:
            # generate sample into the half-opened interval [0.0,1) with size ni
            binSample=np.random.random_sample(binn[3])
            for ranVal in binSample:
                sample.append(binn[1] + binWidth*ranVal)
        self.data['sample']=sample

        ########################################################

    def dump(self):
        print("outputfile: %s" % self.outputFile )
        print("data[%s]: %s\n\n\n" % (self.iD, pformat(self.data)))

    def plotHist(self):
        label="HIST"
        title="Histogram for Sample N: %s" % (self.iD)

        self.figure.add_subplot(222, label=label)
        plt.subplot(222)
        plt.title(title)
        plt.legend(loc='upper right')
        plt.grid(b=True, which='both', axis='both')
        plt.hist(self.data['sample'],
                 normed=True,
                 facecolor='blue',
                 alpha=0.75,
                 label=label,
                 bins=self.numBins,
                 range=self.binsRange)

