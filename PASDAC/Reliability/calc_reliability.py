"""
Function:
    calc_reliability(timeArr, unit, plot=0)

    : Calculate the reliability of time series data from sensor.

Requirement: 
    package: python(either python2.x or python 3.x), pandas, numpy, matplotlib
    The time must be unixtimestamp in milliseconds.

Development log:
    1. function and script name the same - done
    2. options for second, minute, hour - done
    3. modification: more comments - done
    4. (add y label in figure. - no figure saving) plot or not, to add one param y - done
    5. non-idle -> hasData - done
    6. add plot switch: reliability_calc(timeArr, unit, plot=0) - done
    7. another script named 'save_reliability.py' - done

"""


from __future__ import division
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def calc_reliability(timeArr, unit='second', plot=0):
    """
    Calculate the reliability of time series sensor data in each 'unit' from the start of the 'timeArr' to the end.
    Plot is optional.

    Requirement: timeArr must be unixtimestamp in milliseconds.

    :param timeArr: time array of unixtimestamp in milliseconds, size N*1
    :param unit: str, options: "second", "minute", "hour"
    :param plot: 0 or 1
    :return countDf: reliability result dataframe with columns 'Time' and 'SampleCounts'.

    """

    # ==================================================================================
    # generate the reliability dataframe
    # ==================================================================================
    msecCnts = {
        "second": 1000,
        "minute": 60000,
        "hour": 3600000,
    }

    timeNoDuplicateArr = np.unique(timeArr)
    timeNoDuplicateArr = np.floor_divide(timeNoDuplicateArr, msecCnts[unit]).astype(int)
    timeNoDuplicateArr = np.sort(timeNoDuplicateArr)

    reliabilityTimeList = []
    reliabilitySampleCountsList = []
    count = 0

    # loop through the timeNoDuplicateArr
    for i in range(len(timeNoDuplicateArr) - 1):
        # if next timestamp is the same as current one
        if timeNoDuplicateArr[i+1] == timeNoDuplicateArr[i]:
            count += 1
        else:
            reliabilityTimeList.append(timeNoDuplicateArr[i])
            # count+1 instead of count because it's looking at the next second
            reliabilitySampleCountsList.append(count+1)
            count = 0
            # if the data have a gap, which means unit(s) with no data exist(s)
            for time in range(timeNoDuplicateArr[i] + 1, timeNoDuplicateArr[i+1]):
                reliabilityTimeList.append(time)
                # append 0 to noData seconds
                reliabilitySampleCountsList.append(0)
    
    # With try-except, no need to check the input and the empty countDf will be returned.
    # Advantage: In batch processing, when empty data files with only header exist, 
    #  the reliability files will follow the same pattern.
    try: 
        reliabilityTimeList.append(timeNoDuplicateArr[-1])
        reliabilitySampleCountsList.append(count + 1)
    except:
        print('Warning: timeArr is empty!')

    countDf = pd.DataFrame({'Time':reliabilityTimeList,'SampleCounts':reliabilitySampleCountsList},\
                            columns=['Time','SampleCounts'])

    # ==================================================================================
    # plot figure
    # ==================================================================================
    if plot:
        countDf['Time'] = pd.to_datetime(countDf['Time'], unit='s', utc=True)
        countDf = countDf.set_index(['Time'])
        countDf.index = countDf.index.tz_convert('US/Central')

        f = plt.figure(figsize=(12,5))
        countDf.plot(style=['b-'], ax=f.gca())
        plt.title('Reliability Test')
        plt.ylabel('Count Per Unit')
        plt.show()
        # plt.savefig(os.path.join(outfolder, 'reliability(frequency).png')) # FYI, save fig function

    return countDf


def test_case():
    filePath = 'tests/08-24-17_08.csv'
    timestampCol = 1
    saveFolder = 'second'
    unit = 'second'

    if not os.path.exists(saveFolder):
        os.makedirs(saveFolder)
    try:
        df = pd.read_csv(filePath)
        timeArr = df.iloc[:,timestampCol-1].values
    except Exception:
        print("Data file {} does not exists.".format(filePath))
        exit()

    # requirement: unixtimestamp must be in milliseconds
    countDf = calc_reliability(timeArr, unit, plot=1)
    print(countDf)


def call_from_cmd_line():
    # get the file path where the sampled data and timestamp are saved
    filePath = str(sys.argv[1])
    # specify the path where plot and count-per-second file will be saved.
    saveFolder = str(sys.argv[2])
    # get the column of timestamp in data file
    timestampCol = int(sys.argv[3])

    if not os.path.exists(saveFolder):
        os.makedirs(saveFolder)
    try:
        df = pd.read_csv(filePath)
        timeArr = df.iloc[:,timestampCol-1].values
    except Exception:
        print("Data file {} does not exists.".format(filePath))
        exit()

    # Requirement: timeArr must be unixtimestamp in milliseconds.
    countDf = calc_reliability(timeArr, unit, plot=0)


if __name__ == "__main__":
    test_case()

 