"""Segmentation algorithms

Implement different segmentation algorithms
"""

import logging
import pandas as pd
import numpy as np
from PASDAC.settings import SETTINGS

logger = logging.getLogger(__name__)


def segment(data):
    """Master segment function
    Based on SETTINGS, run corresponding function

    Parameters
    ----------
    data:           dataFrame

    Return
    ------
    segmentDf:      dataFrame

    """


def segment_sliding_window(data, winSizeMillisecond=1000, stepSizeMillisecond=100):
    """Sliding window algorithm realization Output 'segments'
    contains start and end indexes for each step

    Comment: we do not handle large dataFrame

    Assumption
    ----------
    data is contiguous data

    Parameters
    ----------
    data:           dataFrame
    SETTINGS:       object

    Return
    ------
    segment:       dataFrame

    """

    logger.info("Sliding window with win size %.2f second and step size %.2f second",
                winSizeSecond, stepSizeSecond)

    if stepSizeSecond > winSizeSecond:
        raise ValueError("Step size %.2f must not be larger than window size %.2f",
                         stepSizeSecond, winSizeSecond)

    startTime = data['Time'].iloc[0]
    endTime = data['Time'].iloc[-1]

    segmentStart = np.arange(startTime, endTime - winSizeMillisecond, stepSizeMillisecond)
    segmentEnd = segmentStart + winSizeMillisecond

    segment = pd.DataFrame({'Start': segmentStart,
                            'End': segmentEnd},
                           columns=['Start', 'End'])

    return segment
