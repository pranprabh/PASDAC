"""
Functionality:
    Calculate the reliability of time series data from sensor.

Requirement: 
    Unixtimestamp must be in milliseconds.

Development log:
    1. function and script name the same - done
    2. options for second, minute, hour - done
    3. modification: more comments - done
    4. (add y label in figure. - no figure saving) plot or not, to add one param y
    5. non-idle -> hasData - done
    6. add plot switch: reliability_calc(timeArr, sensorFreq, unit, plot=0) - done
    7. another script named 'save_reliability.py' - done

Note: data structure revisit:
    [participant]
        [device]
            [sensor]
                [day]:
                    [hour]: csv(s)
            [sensor_reliability]: same structure as [day] folder, csv(s)
    USE THIS FORMAT:
    'acc'---'20180824'---'2018082408.csv'
    'acc_reliability'--'20180824.csv'
                    --'20180824'--'2018082408.csv'
    'gyr'---'20180824'---'2018082408.csv'
    'gyr_reliability'--'20180824.csv'
                    --'20180824'--'2018082408.csv'

-Shibo
"""


from __future__ import division
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def calc_reliability(timeArr, sensorFreq, unit, plot=0):
    """
    Calculate the reliability of time series data from sensor.
    Requirement: unixtimestamp must be in milliseconds.
    :param timeArr: time array of unixtimestamp in milliseconds, size N*1
    :param unit: str, options: "second", "minute", "hour"
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

    reliabilityTimeList.append(timeNoDuplicateArr[-1])
    reliabilitySampleCountsList.append(count + 1)
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
        plt.title('Frequency')
        plt.show()
        # plt.savefig(os.path.join(outfolder, 'reliability(frequency).png')) # FYI, save fig function

    return countDf

