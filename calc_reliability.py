"""
Development log:

1. function and script name the same - done
2. options for second, minute, hour - done
3. modification: more comments - done
4. (add y label in figure. - no figure saving) plot or not, to add one param y
5. non-idle -> hasData - done
6. one function: reliability_calc(dataDf, unit=["second","minute","hour"], save=0)


[participant]
    [device]
        [sensor]
            [day]:
                [hour]: csv(s)
        [sensor_reliability]: same structure as [day] folder, csv(s)

# USE THIS FORMAT:
# 'acc'---'20180824'---'2018082408.csv'
# 'acc_reliability'--'20180824.csv'
#                 --'20180824'--'2018082408.csv'
#
# 'gyr'---'20180824'---'2018082408.csv'
# 'gyr_reliability'--'20180824.csv'
#                 --'20180824'--'2018082408.csv'

"""




from __future__ import division
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def calc_reliability(timeArr, sensorFreq, unit, saveFolder, saveInFile=1):
    """
    Calculate the reliability of time series data from sensor.

    :param timeArr: time array of unixtimestamp in milliseconds, size N*1
    :param unit: str, options: "second", "minute", "hour"
    :return countDf: reliability result dataframe with columns 'Time' and 'SampleCounts'.
    """

    # generate the reliability dataframe

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

    if saveInFile:
        countDf.to_csv(os.path.join(saveFolder, 'reliability.csv'), index=False)

    # 
    idealCntInUnits = {
        "second": sensorFreq,
        "minute": sensorFreq*60,
        "hour": sensorFreq*3600,
    }


    return countDf


def write_results(outfolder, countDf, sensorFreq, unit):
    """

    :param outfolder:
    :param countDf:
    :param sensorFreq:
    :param unit:
    :return:
    """

    idealCntInUnits = {
        "second": sensorFreq,
        "minute": sensorFreq*60,
        "hour": sensorFreq*3600,
    }

    countDf.to_csv(os.path.join(outfolder, 'reliability.csv'), index=False)
    countDf['Time'] = pd.to_datetime(countDf['Time'], unit='s', utc=True)
    print("Duration: {}".format(countDf.Time.iloc[-1] - countDf.Time.iloc[0]))

    countDf = countDf.set_index(['Time'])
    # countDf.index = countDf.index.tz_convert('US/Central')

    ## plot figure and save
    # f = plt.figure(figsize=(12,5))
    # countDf.plot(style=['b-'], ax=f.gca())
    # plt.title('Frequency')
    # plt.savefig(os.path.join(outfolder, 'reliability(frequency).png'))

    countHasDataUnitsDf = countDf[countDf.SampleCounts != 0]
    countHasDataUnitsArr = countHasDataUnitsDf.SampleCounts.values
    samplingFreqArr = np.full_like(countHasDataUnitsArr, idealCntInUnits[unit])
    countHasDataUnitsArr = np.minimum(countHasDataUnitsArr, samplingFreqArr)
    reliabilityHasDataUnits = np.sum(countHasDataUnitsArr)/np.sum(samplingFreqArr)

    print("Reliability for has-data units(seconds or minutes or hours): {}".format(reliabilityHasDataUnits))

    countArr = countDf.SampleCounts.values
    samplingFreqArr = np.full_like(countArr, idealCntInUnits[unit])
    countArr = np.minimum(countArr, samplingFreqArr)
    reliability = np.sum(countArr)/np.sum(samplingFreqArr)

    print("Reliability for all the units(seconds or minutes or hours): {}".format(reliability))



if __name__ == "__main__":
    # # get the file path where the sampled data and timestamp are saved
    # filePath = str(sys.argv[1])
    # # specify the path where plot and count-per-second file will be saved.
    # saveFolder = str(sys.argv[2])
    # # get the column of timestamp in data file
    # timestampCol = int(sys.argv[3])
    # # get the sensor frequency setting
    # sensorFreq = int(sys.argv[4])

    filePath = './08-24-17_08.csv'
    saveFolder = './second'
    timestampCol = 1
    unit = 'second'
    sensorFreq = 20


    if not os.path.exists(saveFolder):
        os.makedirs(saveFolder)

    try:
        df = pd.read_csv(filePath)
        timeArr = df.iloc[:,timestampCol-1].values
    except Exception:
        print("Data file {} does not exists.".format(filePath))
        exit()

    # requirement: unixtimestamp must be in milliseconds
    countDf = calc_reliability(timeArr, unit, saveFolder, saveInFile=1)

    write_results(saveFolder, countDf, sensorFreq, unit)


 