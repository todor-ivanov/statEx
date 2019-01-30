--- A small set of statistical exercises --- __

The simple instrumentation developed for the exercises is called dist.py. The   __
usage is shown in [1]. The data samples are orginised in json files, an excerpt __
from one of them is presented in [2].__


[1]__
Usage:__
    usage: ./dist.py [options]__


Options:__
  -h, --help            show this help message and exit__
  -n NUM, --num=NUM     the sample number to read from 'file' (default: all)__
  -f FILE, --file=FILE  input .json file (default: table4.json)__
  -i, --ignore          ignore -i option if passed from 'ipython'__


[2]__
{__
"0": {__
 "n": 12,__
 "sample": [1.8, 2, 3.3, 2.6, 1.3, -4, 0.5, 0.7, -0.7, 5.1, 5.7, 2],__
 "eta": 0.9,__
 "m": 1.5,__
 "sigma": 2.5__
},__
"1": {__
 "n": 15,__
 "sample": [ -6, -4.4, -2, -7.6, -0.4, 0.1, -3.7, -5.4, -0.8, -3.9, -5.3, -0.3, -4.8, -8.6, -0.9 ],__
 "eta": 0.95,__
 "m": -4,__
 "sigma": 2__
},__
...__
}__

