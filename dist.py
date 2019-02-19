#!/usr/bin/python

import json, ast
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

class Dist:
    """"
    A simle class representing a distribution.
    methods:
        empDistFun(): calculates the values of the Empirical Distribution Function
        dump(): dumps the contents of a single object
    """
    def __init__(self, data, iD):
        # self.data = data
        self.data = ast.literal_eval(json.dumps(data)) # clean unicode chars from dict
        self.iD = iD
        self.outputFile="dist.%s.png" % iD
        # explicitly calulate the lenth of the sample and
        # correct eventual typos in the .json file
        self.data['n']=len(self.data['sample'])
        # sort the sample in advance (to be used in the edf later):
        self.data['sample'].sort()

        # find the Probability Space for the current sample:

        # find the sample data Type:
        sampleType='float'
        if all(isinstance(n, int) for n in self.data['sample']):
            sampleType='int'

        # find the sample decimial precision:
        precisionList=[]
        for i in self.data['sample']:
            d = decimal.Decimal(str(i))
            # pprint(d.as_tuple())
            precisionList.append(abs(d.as_tuple().exponent))
        precision=max(precisionList)
        # pprint(precisionList)
        # print("precision: %s" % precision)
        # print("sampleType: %s" % str(sampleType))
        del precisionList

        # estimate the Step for the sample Probability Space:
        if sampleType == int:
            step=1
        else:
            step="0."
            for x in range(1,precision):
                step += '0'
            step += '1'
            step = float(step)

        # print("step: %s" % step)

        sampleMin=min(self.data['sample'])
        sampleMax=max(self.data['sample'])
        self.sampleMax=sampleMax
        self.sampleMin=sampleMin
        # generate the Probability space:
        self.probSpace=np.arange(sampleMin, sampleMax + step, step)
        # self.probSpace=np.arange( 0.089, 0.12 + 0.001, 0.001)
        # pprint(self.probSpace)

        # create the figure
        self.figure=plt.figure(num=None, figsize=(15, 12), dpi=80)

    def dump(self):
        print("outputfile: %s" % self.outputFile )
        print("data[%s]: %s\n\n\n" % (self.iD, pformat(self.data)))

    def empDistFun(self):
        self.data['edfVal'] = []
        # list.index(x) Returns the index in the list of the first item whose value is x
        # Here data['sample'].index(i) = number of elements with value < the current element
        # (the list has been sorted in advance).
        for i in self.data['sample']:
            m=self.data['sample'].index(i)
            n=self.data['n']
            self.data['edfVal'].append(float(m)/float(n))
            # print("%s/%s=" % (float(m), float(n)))

    def cumDistFun(self, x):
        """
        Cumulative distribution function for a normal Distribution with
        known mean and standard deviation.
        erf: https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.special.erf.html
        cdf: https://en.wikipedia.org/wiki/Normal_distribution#Cumulative_distribution_function
        F(t) = F((x-m)/sigma)=(1/2)*(1+erf((x-m)/(sigma*sqrt(2))))
        """
        m=self.data['m']
        sigma=self.data['sigma']
        print("m=%s,sigma=%s" %(m,sigma))
        return (1/2.0) * (1.0 + sps.erf((x-m)/(sigma * np.sqrt(2))))

    def ma(self):
        # Find the mean of a sample.
        # Using the simplest - arithmetic approach for the moment.
        sampSum=sum(self.data['sample'])
        ma=float(sampSum)/self.data['n']
        self.data['ma']=ma
        return ma

    def plotEDF(self):
        label="EDF"
        title="Empirical Distribution Function for Sample N: %s" % (self.iD)
        self.figure.add_subplot(223, label=label)
        plt.subplot(223)
        plt.title(title)
        plt.legend(loc='upper right')
        plt.xlabel('Sample')
        plt.xticks(self.data['sample'], rotation = 'vertical', color='r')
        plt.minorticks_on()
        plt.ylabel('EDF')
        # plt.plot(self.data['sample'], self.data['edfVal'])
        plt.step(self.data['sample'], self.data['edfVal'])
        plt.grid(b=True, which='both', axis='both')
        # plt.show()

    def plotCDF(self):
        label="CDF"
        title="Cumulative Distribution Function for Sample N: %s" % (self.iD)
        interval=np.arange(self.sampleMin, self.sampleMax, 0.1)
        # calculate 
        avrStep=(self.sampleMax-self.sampleMin)/self.data['n']
        extInterval=np.arange(self.sampleMin-3*avrStep, self.sampleMax+3*avrStep, 0.2)
        plt.subplot(223)
        plt.title(title)
        plt.legend(loc='upper right')
        # for x in interval:
        #     print("F(t): %s" % self.cumDistFun(x))
        plt.plot(extInterval, self.cumDistFun(extInterval), 'r')
        plt.grid(b=True, which='both', axis='both')


    def plotPDF(self):
        label="PDF"
        title="Probability Distribution Function for Sample N: %s" % (self.iD)
        self.figure.add_subplot(221, label=label)
        plt.subplot(221)
        plt.title(title)
        plt.legend(loc='upper right')
        plt.grid(b=True, which='both', axis='both')


    def plotHist(self):
        label="HIST"
        title="Histogram for Sample N: %s" % (self.iD)
        # binWidth=
        # binsRange=range(min(self.probSpace),
        #                 max(self.probSpace) + binWidth,
        #                 binWidth)

        # Using Sturges' formula to estimate the number of bins
        numBins=ceil(log(self.data['n'], 2)) + 1
        print("numBins: %s" % numBins)

        self.figure.add_subplot(222, label=label)
        plt.subplot(222)
        plt.title(title)
        plt.legend(loc='upper right')
        plt.grid(b=True, which='both', axis='both')
        plt.hist(self.data['sample'],
                 facecolor='blue',
                 alpha=0.75,
                 label=label,
                 bins=numBins,
                 align='left')


    def fit(self):
        pass

def isValidOpt():
    return True

def run(*args, **kwargs):

    # if a 'sample' number is not provided on the command line
    # run on all the samples from the current table
    start=0
    stop=31
    if 'num' in kwargs.keys() and kwargs['num'] is not None:
        start=kwargs['num']
        stop=kwargs['num']+1

    if 'file' in kwargs.keys() and kwargs['file']:
        file=kwargs['file']

    data=dict()
    with open(file) as x:
        data=json.load(x)

    for i in range(start,stop):
        dist=Dist(data[str(i)], i)
        dist.empDistFun()
        dist.ma()
        dist.dump()
        dist.plotEDF()
        dist.plotPDF()
        dist.plotCDF()
        dist.plotHist()
        plt.show()
        del dist


def main(*argss, **kwargss):

    usage="""
    usage: ./%prog [options]
    """
    optParser=OptionParser(usage=usage)
    optParser.add_option("-n", "--num", action="store",
                         type='int', dest="num",
                         help="the sample number to read from 'file' (default: all)")

    optParser.add_option("-f", "--file", action="store",
                         type='str', dest="file",
                         default="table4.json",
                         help="input .json file (default: table4.json)")

    optParser.add_option("-i", "--ignore", action="store_true",
                         dest="ignore",
                         help="ignore -i option if passed from 'ipython'")

    if argss:
        # print(type(argss))
        argss=list(argss)
        (options, args) = optParser.parse_args(argss)
    else:
        (options, args) = optParser.parse_args()

    # pprint(options)
    run(num=options.num, file=options.file)

if __name__ == "__main__":
    main()
    exit()

print("we are here")
# main('-n 5', '-ftable4.json', '-i')
main('-n', '9', '-f', 'table4.json',  '-i')
