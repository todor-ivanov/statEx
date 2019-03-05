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

class Dist1:
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

        self.step=step

        # print("step: %s" % step)

        sampleMin=min(self.data['sample'])
        sampleMax=max(self.data['sample'])
        self.sampleMax=sampleMax
        self.sampleMin=sampleMin
        self.avrStep=(self.sampleMax-self.sampleMin)/self.data['n']

        # generate the Probability space:
        self.probSpace=np.arange(self.sampleMin-3*self.avrStep, self.sampleMax+3*self.avrStep, self.step)
        # pprint(self.probSpace)

        # todo:
        #      to make the following with the proper Laplace transform instead of
        #      tabulated valued Laplace function
        # The commonly used values of the Laplace function [1] are in the key names
        # while the the values of the x argument are in the key values themselves.
        # [1]
        #      F(x) = (2/sqrt(2*pi))*int_0^x(exp(-(t**2)/2))dt

        self.laplFuncVals={
            '0.8':   1.2816,
            '0.9':   1.6449,
            '0.95':  1.9600,
            '0.99':  2.5758,
            '0.999': 3.2905
            }

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

    def disp(self, expVal=False):
        """
        Calculate the statistical dispersion (variance and standard deviation):

        1. Known expectation value:
        variance = sigma**2 = (1/n)*sum((x_i - m)**2)

        2. Unknown expectation value:
        variance = sigma**2 = (1/(n -1))*sum((x_i - ma)**2)

        """
        var=None
        stDev=None
        if expVal:
            var=(1/float(self.data['n']))*(np.sum((x - self.data['m'])**2 for x in self.data['sample']))
            varKey='sigmaTheo'
        else:
            var=(1/(float(self.data['n'])-1))*(np.sum( (x - self.data['ma'])**2 for x in self.data['sample']))
            varKey='sigmaEmp'

        stDev=np.sqrt(var)
        self.data[varKey]=stDev
        return var

    def confIntStDev(self, expVal=False):
        sigma1Emp=None
        sigme2Emp=None
        sgima1Theo=None
        sigma2Theo=None
        if expVal:
            
            sigm1Key='sgima1Theo'
            sigm2Key='sgima2Theo'
            
        pass

    def confIntExpVal(self, stDev=False):
        eps=None
        if stDev:
            x=self.laplFuncVals[str(self.data['eta'])]
            # print("x: %s" % x )
            eps=x*(float(self.data['sigma'])/np.sqrt(self.data['n']))
            epsKey='epsTheo'
        else:
            with open('studDistTab.yaml','r') as studDistTabFile:
                studDistTab=yaml.load(studDistTabFile)
            # pprint(studDistTab)
            stValComp=(1 - (1-self.data['eta'])/2)*(10**4)
            degFree=self.data['n'] - 1
            if degFree in studDistTab.keys():
                for tEst, stVal in iter(sorted(studDistTab[degFree].iteritems())):
                    # print("tEst: %s, stVal: %s" %(tEst,stVal))
                    if stVal >= stValComp:
                        break
                # print("Finally: \ntEst: %s, stVal: %s" %(tEst,stVal))
            else:
                print("degree of freedom out of range")
                return False
            eps=tEst*(float(self.data['sigmaEmp'])/np.sqrt(self.data['n']))
            epsKey='epsEmp'

        self.data[epsKey]=eps
        return eps

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
        plt.subplot(223)
        plt.title(title)
        plt.legend(loc='upper right')
        # for x in interval:
        #     print("F(t): %s" % self.cumDistFun(x))
        plt.plot(self.probSpace, self.cumDistFun(self.probSpace), 'r')
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
