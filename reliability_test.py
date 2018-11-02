"""
In terminal, run command: 
python reliability_test.py [data file path] [output result and plot path] [column of timestamp in data file] [sensor frequency setting]

Arguments:
------------------------------------------------------------------------------------
[data file path]: 
    File path where the sampled data and timestamp are saved.

[output result and plot path]: 
    The path where plot and count-per-second file will be saved.

[column of timestamp in data file]:  
    The column of timestamp in data file. Eg, if the timestamp is in the first column, then [column of timestamp in data file] = 1

[sensor frequency setting]: 
    Sensor frequency setting

"""

from __future__ import division
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys


def get_sample_counts(totalTime):

    idleSecondCount = 0
    reliabilityTimeList = []
    reliabilitySampleCountsList = []
    count = 0

    for i in range(len(totalTime) - 1):
        if totalTime[i+1] == totalTime[i]:
            count += 1
        else:
            reliabilityTimeList.append(totalTime[i])
            reliabilitySampleCountsList.append(count+1)
            count = 0
            for time in range(totalTime[i] + 1, totalTime[i+1]):
                reliabilityTimeList.append(time)
                reliabilitySampleCountsList.append(0)
                idleSecondCount += 1

    reliabilityTimeList.append(totalTime[-1])
    reliabilitySampleCountsList.append(count + 1)
    countDf = pd.DataFrame({'Time':reliabilityTimeList,'SampleCounts':reliabilitySampleCountsList},\
        columns=['Time','SampleCounts'])

    return countDf, idleSecondCount


def write_results(outfolder, countDf, samplingFreq=20):

    countDf.to_csv(os.path.join(outfolder, 'reliability.csv'), index=False)
    countDf['Time'] = pd.to_datetime(countDf['Time'], unit='s', utc=True)
    print("Duration: {}".format(countDf.Time.iloc[-1] - countDf.Time.iloc[0]))

    countDf = countDf.set_index(['Time'])
    # countDf.index = countDf.index.tz_convert('US/Central')

    f = plt.figure(figsize=(12,5))
    countDf.plot(style=['b-'], ax=f.gca())
    plt.title('Frequency')
    plt.savefig(os.path.join(outfolder, 'reliability(frequency).png'))

    countNonIdleDf = countDf[countDf.SampleCounts != 0]
    countNonIdleArr = countNonIdleDf.SampleCounts.values
    samplingFreqArr = np.full_like(countNonIdleArr, samplingFreq)
    countNonIdleArr = np.minimum(countNonIdleArr, samplingFreqArr)
    reliabilityNonIdle = np.sum(countNonIdleArr)/np.sum(samplingFreqArr)

    print("Reliability for non-idle seconds: {}".format(reliabilityNonIdle))

    countArr = countDf.SampleCounts.values
    samplingFreqArr = np.full_like(countArr, samplingFreq)
    countArr = np.minimum(countArr, samplingFreqArr)
    reliability = np.sum(countArr)/np.sum(samplingFreqArr)

    print("Reliability for all the seconds: {}".format(reliability))



if __name__ == "__main__":
    # get the file path where the sampled data and timestamp are saved
    filePath = str(sys.argv[1])
    # specify the path where plot and count-per-second file will be saved.
    resultPath = str(sys.argv[2])
    # get the column of timestamp in data file
    timestampCol = int(sys.argv[3])
    # get the sensor frequency setting
    sensorFreq = int(sys.argv[4])

    if not os.path.exists(resultPath):
        os.makedirs(resultPath)

    try:
        df = pd.read_csv(filePath)
        time = df.iloc[:,timestampCol-1].as_matrix()
        timeNoDuplicateArr = np.unique(time)
    except Exception:
        print("Data file {} does not exists.".format(filePath))
        exit()

    timeNoDuplicateArr = np.floor_divide(timeNoDuplicateArr, 1000).astype(int)
    timeNoDuplicateArr = np.sort(timeNoDuplicateArr)

    countDf, _ = get_sample_counts(timeNoDuplicateArr)
    write_results(resultPath, countDf, sensorFreq)

 