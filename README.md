--- A small set of statistical exercises --- <br />

The simple instrumentation developed for the exercises is called dist.py. The   <br />
usage is shown in [1]. The data samples are orginised in json files, an excerpt <br />
from one of them is presented in [2].<br />


[1]<br />
Usage:<br />
    usage: ./dist.py [options]<br />


Options:<br />
  -h, --help            show this help message and exit<br />
  -n NUM, --num=NUM     the sample number to read from 'file' (default: all)<br />
  -f FILE, --file=FILE  input .json file (default: table4.json)<br />
  -i, --ignore          ignore -i option if passed from 'ipython'<br />


[2]<br />
{<br />
"0": {<br />
 "n": 12,<br />
 "sample": [1.8, 2, 3.3, 2.6, 1.3, -4, 0.5, 0.7, -0.7, 5.1, 5.7, 2],<br />
 "eta": 0.9,<br />
 "m": 1.5,<br />
 "sigma": 2.5<br />
},<br />
"1": {<br />
 "n": 15,<br />
 "sample": [ -6, -4.4, -2, -7.6, -0.4, 0.1, -3.7, -5.4, -0.8, -3.9, -5.3, -0.3, -4.8, -8.6, -0.9 ],<br />
 "eta": 0.95,<br />
 "m": -4,<br />
 "sigma": 2<br />
},<br />
...<br />
}<br />

