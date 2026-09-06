"""
This routine is designed to illustrate ergodicity
in that the return over time is different from
the return at a particular time from multiple
runs
"""
import numpy as np
from params import AVERAGE_RETURN, STD_RETURN, NUM_RUNS, NUM_YEARS

rng = np.random.default_rng()
returns = rng.normal(AVERAGE_RETURN, STD_RETURN, size=(NUM_RUNS, NUM_YEARS))

less = 0
more = 0
bet = 100000.0

for i in range(NUM_RUNS):
    for j in range(NUM_YEARS):
        if returns[i][j] < AVERAGE_RETURN:
            less += 1
            bet = bet * .7
        else:
            more += 1
            bet = bet * 1.5
        print(bet)
print(f"DEBUG: bet={bet}, less={less}, more={more}, total={less + more}, less%={less/(less+more):.2%}, more%={more/(less+more):.2%}")