"""
Functionality:
    Calculate and print out the reliability score.
Requirement: 
    Unixtimestamp must be in milliseconds.
"""

from __future__ import division
import os
import sys
import numpy as np
import pandas as pd
from calc_reliability import calc_reliability 


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

    return reliabilityHasDataUnits, reliability