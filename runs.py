'''
Implements a monte-carlo simulation of a retirement plan with 
specified parameters
'''

import numpy as np
from params import DETERMINISTIC, INITIAL_WEALTH, AVERAGE_RETURN, STD_RETURN, INFLATION_RATE, STD_INFLATION, NUM_RUNS, NUM_YEARS

FORMATD = "${:,.0f}"

def print_stats(the_runs):
    print("\nRuns Final Values:")
    # print out the_runs
    # for i in range(NUM_RUNS):
        # print (FORMATD.format(the_runs[i][NUM_YEARS - 1]))
    print("Run Mean:", dollar_format(np.mean(the_runs[:, NUM_YEARS - 1])))
    print("Run Median:", dollar_format(np.median(the_runs[:, NUM_YEARS - 1])))
    print("Run 10% percentile:", dollar_format(np.percentile(the_runs[:, NUM_YEARS - 1], 10)))
    print("Run 25% percentile:", dollar_format(np.percentile(the_runs[:, NUM_YEARS - 1], 25)))
    print("Run Min:", dollar_format(np.min(the_runs[:, NUM_YEARS - 1])))
    print("Run Max:", dollar_format(np.max(the_runs[:, NUM_YEARS - 1])))
    print("Run FV less than zero:", percent_format((np.count_nonzero(the_runs[:, NUM_YEARS - 1] < 0))/NUM_RUNS))


rng = np.random.default_rng()
if DETERMINISTIC:
    # generate deterministic numbers for returns and inflation
    returns = np.ones((NUM_RUNS, NUM_YEARS)) * AVERAGE_RETURN
    inflation = np.ones((NUM_RUNS, NUM_YEARS)) * INFLATION_RATE
else:
    # generate random returns for normal distributions for returns and inflation
    returns = rng.normal(AVERAGE_RETURN, STD_RETURN, size=(NUM_RUNS, NUM_YEARS))
    inflation = rng.normal(INFLATION_RATE, STD_INFLATION, size=(NUM_RUNS, NUM_YEARS))

def dollar_format(value):
    return FORMATD.format(value)

def percent_format(value):
    return "{:.2%}".format(value)

def generate_jim_runs(initial_withdrawal): 
    runs = np.zeros((NUM_RUNS, NUM_YEARS), dtype=float)
    for i in range(NUM_RUNS):
        balance = INITIAL_WEALTH
        withdrawal = initial_withdrawal
        for j in range(NUM_YEARS):
            # no earnings if balance is zero or negative
            earnings = balance * returns[i][j] if balance > 0 else 0
            # inflation is prior year otherwise none
            adj_inflation = inflation[i][j - 1] if j > 0 else 0
            withdrawal = withdrawal * (1 + adj_inflation)
            end_balance = balance + earnings - withdrawal
            # print(f"DEBUG: old balance={dollar_format(balance)}, returns={percent_format(returns[i][j])}, earnings={dollar_format(earnings)}, inflation={percent_format(adj_inflation)}, wdraw={dollar_format(withdrawal)}, new balance={dollar_format(end_balance)}")
            runs[i][j] = end_balance
            balance = end_balance
    return runs

def binary_search(target_success_rate, lower_limit, upper_limit, tolerance=0.001):
    while upper_limit - lower_limit > tolerance:
        mid = (upper_limit + lower_limit) / 2
        the_runs = generate_jim_runs(mid)
        success_rate = np.count_nonzero(the_runs[:, NUM_YEARS - 1] >= 0) / NUM_RUNS
        print(f"DEBUG: testing={dollar_format(mid)}, success_rate={percent_format(success_rate)}")
        if abs(success_rate - target_success_rate) < tolerance:
            break
        if success_rate < target_success_rate:
            upper_limit = mid
        else:
            lower_limit = mid
    return mid