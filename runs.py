import numpy as np

'''
Implements a monte-carlo simulation of a retirement plan with 
specified parameters
'''
FORMATD = "${:,.2f}"

DETERMINISTIC = False
INITIAL_WEALTH = 1000000
INITIAL_WITHDRAWAL_RATE = 0.04
AVERAGE_RETURN = 0.06
STD_RETURN = 0.09
INFLATION_RATE = 0.025
STD_INFLATION = 0.015
NUM_RUNS = 5000
NUM_YEARS = 30

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

def generate_jim_runs(): 
    runs = np.zeros((NUM_RUNS, NUM_YEARS), dtype=float)
    for i in range(NUM_RUNS):
        balance = INITIAL_WEALTH
        withdrawal = INITIAL_WITHDRAWAL_RATE * INITIAL_WEALTH
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

if __name__ == "__main__":
    the_runs = generate_jim_runs()
    print("\nJim's Runs Final Values:")
    for i in range(NUM_RUNS):
        pass
        # print (FORMATD.format(the_runs[i][NUM_YEARS - 1]))
    print("Run Mean:", dollar_format(np.mean(the_runs[:, NUM_YEARS - 1])))
    print("Run Median:", dollar_format(np.median(the_runs[:, NUM_YEARS - 1])))
    print("Run 10% percentile:", dollar_format(np.percentile(the_runs[:, NUM_YEARS - 1], 10)))
    print("Run 25% percentile:", dollar_format(np.percentile(the_runs[:, NUM_YEARS - 1], 25)))
    print("Run Min:", dollar_format(np.min(the_runs[:, NUM_YEARS - 1])))
    print("Run Max:", dollar_format(np.max(the_runs[:, NUM_YEARS - 1])))
    print("Run FV less than zero:", percent_format((np.count_nonzero(the_runs[:, NUM_YEARS - 1] < 0))/NUM_RUNS))
