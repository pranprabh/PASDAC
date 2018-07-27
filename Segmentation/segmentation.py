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

    segmentation_settings = SETTINGS['SEGMENTATION_TECHNIQUE']

    if segmentation_settings['method'] == 'slidingWindow':
        return segment_sliding_window(data, segmentation_settings['winSizeSecond'],
                                      segmentation_settings['stepSizeSecond'])

    else:
        raise ValueError("Invalid segmentation technique")


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

    start_time = data['Time'].iloc[0]
    end_time = data['Time'].iloc[-1]

    segments_start = np.arange(start_time, end_time - winSizeMillisecond, stepSizeMillisecond)
    segments_end = segments_start + winSizeMillisecond

    segment = pd.DataFrame({'Start': segments_start,
                            'End': segments_end},
                           columns=['Start', 'End'])

    return segment
