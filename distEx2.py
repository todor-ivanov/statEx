import json, ast, yaml
import array
import math
import decimal

from pprint import pprint
from pprint import pformat
from optparse import OptionParser
from math import ceil
from math import log

from numpy import sqrt, sin, cos, pi, exp, inf

import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy.special as sps
import scipy.stats as stats
import pdb

import scipy.integrate as integrate
# import scipy.special as special

class Iter2D:
        """
        a class used to create an iterator of the n-th elemnts
        of a list of tuples (lot) (or any two dimensional object).
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

        binWidth=(self.data['xmax']-self.data['xmin'])/self.data['l']
        binsEdges=range(self.data['xmin'], self.data['xmax'] + binWidth, binWidth)
        self.binWidth=binWidth
        self.binsEdges=binsEdges

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
        self.binTuples=binTuples

        # create the figure
        self.figure=plt.figure(num=None, figsize=(15, 12), dpi=80)

    def lapInt(self, x):
        """
        Intgrate the Laplace function in the interval [0,x]
        """
        coef=(2/(sqrt(2*pi)))
        integ=integrate.quad(lambda t: exp(-(t**2)/2) ,0,x)
        return coef*integ[0]


    def chiSqrtInt(self, x, k):
        pass

    def chiSqrtTest(self):
        lapVals=dict()
        for x in map(lambda x: x/10.0, range(0, 40, 1)):
            lapVals[x]=self.lapInt(x)
        self.data['lapVals']=lapVals

        expVal=self.data['expVal']
        stDev=self.data['stDev']
        binWidth=self.binWidth
        binsEdges=self.binsEdges
        binTuplesChi=[]
        accum=0
        for binTuple in self.binTuples:
            accum += binTuple[3]
            if accum  > 5:
                binTuplesChi.append((len(binTuplesChi),
                                     binTuple[1],
                                     binTuple[2],
                                     accum))
                accum=0
            else:
                continue

        # add the final hits to the last tupple
        if accum:
            tmpTuple=binTuplesChi.pop()
            binTuplesChi.append((len(binTuplesChi),
                                 tmpTuple[1],
                                 tmpTuple[2],
                                 tmpTuple[3]+accum))

        for i, binn in enumerate(binTuplesChi):
            x1=(binn[0]-expVal)/stDev
            x2=(binn[1]-expVal)/stDev
            teorProb=(self.lapInt(x2) - self.lapInt(x1))/2.0
            binTuplesChi[i] = binn + (teorProb,)

        self.data['binTuplesChi']=binTuplesChi



    def parMom(self):
        """
        Estimate distribution parameters from the sample
        using the 'Method of moments'
        """
        binWidth=self.binWidth
        binsEdges=self.binsEdges
        binTuples=self.binTuples
        # # estimate binTuples per bin
        # edge1=None
        # edge2=None
        # binTuples=[]
        # binCount=0
        # binHits=None
        # binAvr=None
        # empProb=None
        # relFreq=None
        # binExpVal=None
        # for edge in binsEdges:
        #     edge1=edge2
        #     edge2=edge
        #     if edge1 and edge2:
        #         binHits=self.data['ni'][binCount]
        #         binAvr=(edge1+edge2)/2.
        #         empProb=float(binHits)/self.data['n']
        #         relFreq=float(empProb)/binWidth
        #         binExpVal=binAvr*empProb
        #         binTuples.append((binCount,    # 0
        #                           edge1,       # 1
        #                           edge2,       # 2
        #                           binHits,     # 3
        #                           binAvr,      # 4
        #                           empProb,     # 5
        #                           binExpVal,   # 6
        #                       ))
        #         binCount += 1

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

        stDev=sqrt(variance)
        self.data['stDev']=stDev

        # Estimate Unform Distribution parameters:
        uniLimMin=expVal-stDev*sqrt(3)
        uniLimMax=expVal+stDev*sqrt(3)
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


    def dump(self):
        print("outputfile: %s" % self.outputFile )
        print("data[%s]: %s\n\n\n" % (self.iD, pformat(self.data)))

    def chiSqrt(self):
        pass

    def plotHist(self):
        plt.rc('text', usetex=True)
        mu=self.data['expVal']
        sigma=self.data['stDev']
        label="HIST"
        title=r'Histogram for Sample N: %s  $\sigma$ = %s  $\mu$ = %s ' % (self.iD, sigma, mu)
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

        x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
        y = stats.norm.pdf(x, mu, sigma)
        plt.plot(x, y, 'red')

        a=self.data['uniLimMin']
        b=self.data['uniLimMax']
        y=map(lambda xval: 0 if xval < a or xval > b else 1.0/(b-a)  ,x)
        plt.plot(x, y, 'black')
