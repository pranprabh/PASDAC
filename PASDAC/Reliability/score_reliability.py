"""
<<<<<<< HEAD
Functionality:
    Calculate and print out the reliability score.
Requirement: 
    Unixtimestamp must be in milliseconds.
=======
Function:
    score_reliability(countDf, sensorFreq=20, unit='second')

    : Calculate and print out the reliability score.

Requirement: 
    package: python(either python2.x or python 3.x), pandas, numpy, matplotlib
    The time must be unixtimestamp in milliseconds.

>>>>>>> Shibo_reliability
"""

from __future__ import division
import os
import sys
import numpy as np
import pandas as pd
from calc_reliability import calc_reliability 


<<<<<<< HEAD
def score_reliability(countDf, sensorFreq, unit):
    """
    :param countDf:
    :param sensorFreq:
    :param unit:
    :return: None
    """

    # # ==================================================================================
    # # save reliability 
    # # (This is a simple one-line command so it should be a seperate function - Shibo)
    # # ==================================================================================
    # countDf.to_csv(os.path.join(outfolder, 'reliability.csv'), index=False)
=======
def score_reliability(countDf, sensorFreq, unit='second'):
    """
    Calculate and print out the reliability score.

    :param countDf: the dataframe of ['Time','SampleCounts'], which is the return of function calc_reliability
    :param sensorFreq: in Hz
    :param unit: str, options: "second", "minute", "hour"
    :return: reliabilityHasDataUnits: the average reliability score for the units that has data 
    :return: reliability: the average reliability score for all the units
    """
>>>>>>> Shibo_reliability

    # ==================================================================================
    # print out reliability score for has-data units and for all units
    # ==================================================================================
    
    countDf.index = pd.to_datetime(countDf.index, unit='s', utc=True)
    print("Duration: {}".format(countDf.index[-1] - countDf.index[0]))

    idealCntInUnits = {
        "second": sensorFreq,
        "minute": sensorFreq*60,
        "hour": sensorFreq*3600,
    }
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

<<<<<<< HEAD
    return reliabilityHasDataUnits, reliability
=======
    return reliabilityHasDataUnits, reliability


def test_case():
    filePath = '08-24-17_08.csv'
    timestampCol = 1
    saveFolder = 'minute'
    unit = 'minute'
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
    countDf = calc_reliability(timeArr, sensorFreq, unit, plot=0)
    countDf.to_csv(os.path.join(saveFolder, 'reliability.csv'), index=False)

    score_reliability(countDf, sensorFreq, unit)


def call_from_cmd_line():
    # get the file path where the sampled data and timestamp are saved
    filePath = str(sys.argv[1])
    # specify the path where plot and count-per-second file will be saved.
    saveFolder = str(sys.argv[2])
    # get the column of timestamp in data file
    timestampCol = int(sys.argv[3])
    # get the sensor frequency setting
    sensorFreq = int(sys.argv[4])

  
    if not os.path.exists(saveFolder):
        os.makedirs(saveFolder)
    try:
        df = pd.read_csv(filePath)
        timeArr = df.iloc[:,timestampCol-1].values
    except Exception:
        print("Data file {} does not exists.".format(filePath))
        exit()

    # requirement: unixtimestamp must be in milliseconds
    countDf = calc_reliability(timeArr, sensorFreq, unit, plot=0)
    countDf.to_csv(os.path.join(saveFolder, 'reliability.csv'), index=False)

    score_reliability(countDf, sensorFreq, unit)


if __name__ == "__main__":
	test_case()


>>>>>>> Shibo_reliability
