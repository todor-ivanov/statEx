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

class Dist2:
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

        # create the figure
        self.figure=plt.figure(num=None, figsize=(15, 12), dpi=80)

    def dump(self):
        print("outputfile: %s" % self.outputFile )
        print("data[%s]: %s\n\n\n" % (self.iD, pformat(self.data)))

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

    # def expVal(self):
    #     # Find the mean of a sample.
    #     # Using the simplest - arithmetic approach for the moment.
    #     sampSum=sum(self.data['sample'])
    #     expVal=float(sampSum)/self.data['n']
    #     self.data['expVal']=expVal
    #     return expVal

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