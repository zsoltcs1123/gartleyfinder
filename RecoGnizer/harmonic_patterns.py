import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema


def find_peak(price, order=10):
    max_idx = list(argrelextrema(price, np.greater, order=order)[0])  # returns the indices of maximums
    min_idx = list(argrelextrema(price, np.less, order=order)[0])  # returns the indices of minimums
    idx = max_idx + min_idx + [len(price) - 1]
    idx.sort()

    current_idx = idx[-5:]  # last 5 indices
    start_idx = min(current_idx)
    end_idx = max(current_idx)

    current_pattern = price[current_idx]  # draw a pattern using the last 5 indices
    return current_idx, current_pattern, start_idx, end_idx


def is_gartley(price_moves, tolerance):
    # Price movements
    XA = price_moves[0]
    AB = price_moves[1]
    BC = price_moves[2]
    CD = price_moves[3]

    # Define ranges for price movements
    AB_range = np.array([0.618 - tolerance, 0.618 + tolerance]) * abs(XA)
    BC_range = np.array([0.382 - tolerance, 0.618 + tolerance]) * abs(AB)
    # CD_range = np.array([1.27 - tolerance, 1.618 + tolerance]) * abs(BC)
    CD_range = np.array([1 - tolerance, 1 + tolerance]) * abs(AB)  # CD equals AB +- tolerance
    # CD_range = np.array([0.618 - tolerance, 0.786 + tolerance]) * abs(XA)  # full trace between 0.618-0.786 +- tol

    # Find an up-down-up-down pattern
    if XA > 0 and AB < 0 and BC > 0 and CD < 0:
        # print("UP_DOWN_UP_DOWN")
        if (  # determine if that pattern is a Bullish Gartley pattern
                AB_range[0] < abs(AB) < AB_range[1]
                and BC_range[0] < abs(BC) < BC_range[1]
                and CD_range[0] < abs(CD) < CD_range[1]
        ):
            print("Bullish Gartley!")
            return 1
        else:
            return np.NAN

    # Find a down-up-down-up pattern
    elif XA < 0 and AB > 0 and BC < 0 and CD > 0:
        # print("DOWN_UP_DOWN_UP")
        if (  # determine if that pattern is a Bearish Gartley pattern
                AB_range[0] < abs(AB) < AB_range[1]
                and BC_range[0] < abs(BC) < BC_range[1]
                and CD_range[0] < abs(CD) < CD_range[1]
        ):
            print("Bearish Gartley!")
            return -1
        else:
            return np.NAN
    else:
        return np.NAN

# TO BE IMPLEMENTED:
# def is_butterfly(price_moves, tolerance):
# def is_bat(price_moves, tolerance):
# def is_crab(price_moves, tolerance):

