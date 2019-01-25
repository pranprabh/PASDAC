Reliability Test:
------------------------------------------------------------------------------------
## Install PASDAC

> `git clone git@github.com:HAbitsLab/PASDAC.git`

> `cd PASDAC`

> `pip install . --user`


1. Function: calculate the reliablility for given data file, save counts per second in path_of_output/reliability.csv and plot the points of every second in path_of_output/reliability(frequency).png

2. Requirement: python(either python2.x or python 3.x), pandas, numpy, matplotlib

3. In terminal, run command: python reliability_test.py [data file path] [output result and plot path] [column of timestamp in data file] [sensor frequency setting]

```
Arguments:
[data file path]: 
    File path where the sampled data and timestamp are saved.

[output result and plot path]: 
    The path where plot will be saved.

[column of timestamp in data file]:  
    The column of timestamp in data file. Eg, if the timestamp is in the first column, then [column of timestamp in data file] = 1

[sensor frequency setting]: 
    Sensor frequency setting
```

```
For example, when the data file is 08-24-17_08.csv in current folder, output folder is current folder, the timestamp is in the 1st column of the data file, sensor frequency setting is 20:
>>>python reliability_test.py './08-24-17_08.csv' './' 1 20

>>>Duration: 0 days 00:59:58
>>>Reliability for non-idle seconds: 0.997902195054
>>>Reliability for all the seconds: 0.997902195054
```

