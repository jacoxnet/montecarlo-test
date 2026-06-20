import random

'''
Given a starting mean and standard deviation, generates 10 sample runs
of 10 years each simulating returns on an investment. The first
run implements Mike's view where the mean return for each run
is exactly the same as the distribution mean. The second implements
the Jim view where the mean return for each run is randomly drawn from
the distribution.
'''

DISTRIBUTION_MEAN = 7
DISTRIBUTION_STD_DEV = .68 * DISTRIBUTION_MEAN
NUM_RUNS = 10
NUM_YEARS = 5


def generate_mike_runs():
    runs = []
    for i in range(NUM_RUNS):
        run = []
        for j in range(NUM_YEARS):
            return_value = random.gauss(DISTRIBUTION_MEAN, DISTRIBUTION_STD_DEV)
            run.append(return_value)
        # now we must normalize the run to have the same mean 
        # as the distribution mean
        run_mean = sum(run) / len(run)
        normalized_run = [x + (DISTRIBUTION_MEAN - run_mean) for x in run]
        runs.append(normalized_run)
    return runs

def generate_jim_runs():
    runs = []
    for i in range(NUM_RUNS):
        run = []
        for j in range(NUM_YEARS):
            return_value = random.gauss(DISTRIBUTION_MEAN, DISTRIBUTION_STD_DEV)
            run.append(return_value)
        runs.append(run)
    return runs

if __name__ == "__main__":
    mike_runs = generate_mike_runs()
    jim_runs = generate_jim_runs()

    print("Mike's Runs:")
    for run in mike_runs:
        print(run)
        print("Run Mean:", sum(run) / len(run))
    

    print("\nJim's Runs:")
    for run in jim_runs:
        print(run)
        print("Run Mean:", sum(run) / len(run))

    print("Overall Mean of Mike's Runs:", sum([sum(run) for run in mike_runs]) / (NUM_RUNS * NUM_YEARS))
    print("Overall Mean of Jim's Runs:", sum([sum(run) for run in jim_runs]) / (NUM_RUNS * NUM_YEARS))