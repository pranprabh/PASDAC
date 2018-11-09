"""Smoothing algorithms

Implement different smoothing algorithms used during preprocessing
"""
import os
import sys
import logging
import numpy as np
from scipy.signal import boxcar, gaussian
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

logger = logging.getLogger(__name__)


def smoothboxcar(data, selected_columns, winsize):
    """Boxcar smoothing of data

    Parameters
    ----------
    data:                   dataframe
    selected_columns:       list of keys, stating which columns will be smoothed
    winsize:                number of samples of rectangle window

    Return
    ------
    smoothed:               dataFrame

    """

    logger.info("Boxcar smoothing with winsize %d", winsize)

    smoothed = data.copy(deep=True)

    for col_header in selected_columns:
        column = smoothed[col_header].values

        # padding data
        # when winsize is even, int(winsize/2) is bigger than int((winsize-1)/2) by 1
        # when winsize is odd, int(winsize/2) is the same as int((winsize-1)/2)
        pad_head = [column[0]] * int((winsize - 1) / 2)
        pad_tail = [column[-1]] * int(winsize / 2)
        signal = np.r_[pad_head, column, pad_tail]

        window = boxcar(winsize)

        smoothed[col_header] = np.convolve(
            window / window.sum(), signal, mode='valid')

    return smoothed


def smoothgaussian(data, selected_columns, winsize, sigma):
    """Gaussian smoothing of data

    Parameters
    ----------
    data:                   dataframe
    selected_columns:       list of keys, stating which columns will be smoothed
    winsize:                number of samples of Gaussian window
    sigma:                  variance of Gaussian window

    Return
    ------
    smoothed:               dataFrame

    """
    logger.info("Gaussian smoothing with winsize %d and sigma %s",
                winsize, sigma)

    smoothed = data.copy(deep=True)

    for col_header in selected_columns:
        column = smoothed[col_header].values

        # padding data
        # when winsize is even, int(winsize/2) is bigger than int((winsize-1)/2) by 1
        # when winsize is odd, int(winsize/2) is the same as int((winsize-1)/2)
        pad_head = [column[0]] * int((winsize - 1) / 2)
        pad_tail = [column[-1]] * int(winsize / 2)
        signal = np.r_[pad_head, column, pad_tail]

        window = gaussian(winsize, sigma)

        smoothed[col_header] = np.convolve(
            window / window.sum(), signal, mode='valid')

    return smoothed
