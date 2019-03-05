#!/usr/bin/python

import json, ast, yaml
import array
import math
import decimal

from  distEx1 import Dist1
from  distEx2 import Dist2

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


def run1(*args, **kwargs):

    # if a 'sample' number is not provided on the command line
    # run on all the samples from the current table
    start=0
    stop=31
    if 'num' in kwargs.keys() and kwargs['num'] is not None:
        start=kwargs['num']
        stop=kwargs['num']+1

    # if 'file' in kwargs.keys() and kwargs['file']:
    #     file=kwargs['file']
    dataFile='table4.json'

    data=dict()
    with open(dataFile) as x:
        data=json.load(x)

    for i in range(start,stop):
        print("---------------------------------------------------------------")
        dist=Dist1(data[str(i)], i)
        dist.empDistFun()
        dist.ma()
        dist.disp(expVal=True)
        dist.disp(expVal=False)
        dist.confIntExpVal(stDev=True)
        dist.confIntExpVal(stDev=False)
        dist.dump()
        dist.plotEDF()
        dist.plotPDF()
        dist.plotCDF()
        dist.plotHist()
        print("---------------------------------------------------------------")
        plt.show()
        del dist

def run2(*args, **kwargs):

    # if a 'sample' number is not provided on the command line
    # run on all the samples from the current table
    start=0
    stop=31
    if 'num' in kwargs.keys() and kwargs['num'] is not None:
        start=kwargs['num']
        stop=kwargs['num']+1

    dataFile='table5.json'

    data=dict()
    with open(dataFile) as x:
        data=json.load(x)

    for i in range(start,stop):
        print("---------------------------------------------------------------")
        dist=Dist2(data[str(i)], i)
        dist.plotHist()
        dist.dump()
        print("---------------------------------------------------------------")
        plt.show()
        del dist

def run3(*argss, **kwargss):
    pass

def main(*argss, **kwargss):

    usage="""
    usage: ./%prog [options]
    """
    optParser=OptionParser(usage=usage)
    optParser.add_option("-n", "--num", action="store",
                         type='int', dest="num",
                         help="the sample number to read from 'file' (default: all)")

    # optParser.add_option("-f", "--file", action="store",
    #                      type='str', dest="file",
    #                      default="table4.json",
    #                      help="input .json file (default: table4.json)")

    optParser.add_option("-e", "--exercise", action="store",
                         type='int', dest="exer",
                         default=1,
                         help="the exercise number to execute (default: 1)")


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
    case={
        1: run1,
        2: run2,
        3: run3
        }
    # chose which run function to execute according to the  chosen exercise
    run=case.get(options.exer, 1)

    run(num=options.num)

if __name__ == "__main__":
    main()
    exit()

print("we are here")
main('-n', '0', '-e', '2',  '-i')
