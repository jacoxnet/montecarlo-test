'''
main file for monte-carlo retirement simulation
'''

from params import INITIAL_WEALTH, AVERAGE_RETURN, NUM_RUNS, NUM_YEARS, TARGET_SUCCESS_RATE, WITHDRAWAL_LOWER_LIMIT, WITHDRAWAL_UPPER_LIMIT
from runs import generate_jim_runs, print_stats, binary_search, dollar_format, percent_format

if __name__ == "__main__":
    print("Monte-Carlo Retirement Simulation")
    print(f"Initial Wealth: {dollar_format(INITIAL_WEALTH)}")
    print(f"Average Annual Return: {percent_format(AVERAGE_RETURN)}")
    print(f"Number of Simulation Runs: {NUM_RUNS}")
    print(f"Number of Years/Run: {NUM_YEARS}")
    print(f"Target Success Rate: {percent_format(TARGET_SUCCESS_RATE)}")

    found_rate = binary_search(TARGET_SUCCESS_RATE, WITHDRAWAL_LOWER_LIMIT, WITHDRAWAL_UPPER_LIMIT)
    print(f"Found optimal withdrawal rate: {dollar_format(found_rate)}")
    
    
