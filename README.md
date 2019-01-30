--- A small set of statistical exercises ---

The simple instrumentation developed for the exercises is called dist.py. The
usage is shown in [1]. The data samples are orginised in json files, an excerpt
from one of them is presented in [2].

[1]
Usage:
    usage: ./dist.py [options]


Options:
  -h, --help            show this help message and exit
  -n NUM, --num=NUM     the sample number to read from 'file' (default: all)
  -f FILE, --file=FILE  input .json file (default: table4.json)
  -i, --ignore          ignore -i option if passed from 'ipython'


[2]
{
"0": {
 "n": 12,
 "sample": [1.8, 2, 3.3, 2.6, 1.3, -4, 0.5, 0.7, -0.7, 5.1, 5.7, 2],
 "eta": 0.9,
 "m": 1.5,
 "sigma": 2.5
},
"1": {
 "n": 15,
 "sample": [ -6, -4.4, -2, -7.6, -0.4, 0.1, -3.7, -5.4, -0.8, -3.9, -5.3, -0.3, -4.8, -8.6, -0.9 ],
 "eta": 0.95,
 "m": -4,
 "sigma": 2
},
...
}

