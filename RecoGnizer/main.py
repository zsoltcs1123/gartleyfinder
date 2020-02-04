import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from RecoGnizer.harmonic_patterns import *

# Dataset import
my_date_parser = lambda x: pd.datetime.strptime(x, '%d.%m.%Y %H:%M:%S.%f')
data = pd.read_csv('Data/EURUSD_Candlestick_1_Hour_ASK_01.12.2019-25.01.2020.csv',
                   index_col='Gmt time',
                   parse_dates=['Gmt time'],
                   date_parser=my_date_parser)
data.columns = [['open', 'high', 'low', 'close', 'volume']]  # Naming columns
data = data[['open', 'high', 'low', 'close', 'volume']]  # Data selection, columns to show
data.drop_duplicates(keep='last', inplace=True)  # Dropping duplicate rows
price = data.iloc[:, 3]  # Select all rows, column 3: "close"

# Find Gartley
tolerance = 0.1

for i in range(100, len(price)):
    current_idx, current_pattern, start_idx, end_idx = find_peak(price.values[:i])  # Calling find_peak function

    XA = current_pattern[1] - current_pattern[0]
    AB = current_pattern[2] - current_pattern[1]
    BC = current_pattern[3] - current_pattern[2]
    CD = current_pattern[4] - current_pattern[3]

    price_moves = [XA, AB, BC, CD]

    gartley_result = is_gartley(price_moves, tolerance)
    # TO BE IMPLEMENTED:
    # butterfly_result = is_butterfly(price_moves)
    # bat_result = is_bat(price_moves)
    # crab_result = is_crab(price_moves)

    if gartley_result == 1 or gartley_result == -1:
        date_start = data.iloc[start_idx].name
        date_end = data.iloc[end_idx].name
        print("Start: ", date_start)
        print("End: ", date_end)

        plt.title(date_end)
        plt.plot(np.arange(start_idx, i + 5), price.values[start_idx:i + 5])
        plt.plot(current_idx, current_pattern, c="r")
        plt.show()
