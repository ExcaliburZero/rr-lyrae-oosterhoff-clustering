import os
import os.path

import pandas as pd

def main():
    print("LMC V band")
    print("----------")
    print_light_curve_stats("../../data/interim/lmc/curves/V")

    print("LMC I band")
    print("----------")
    print_light_curve_stats("../../data/interim/lmc/curves/I")

    print("SMC V band")
    print("----------")
    print_light_curve_stats("../../data/interim/smc/curves/V")

    print("SMC I band")
    print("----------")
    print_light_curve_stats("../../data/interim/smc/curves/I")

def print_light_curve_stats(lc_dir):
    observation_counts = []

    for filename in os.listdir(lc_dir):
        if filename.endswith(".csv"):
            # Read in the light curve
            curve_file = os.path.join(lc_dir, filename)
            curve = pd.read_csv(curve_file)

            # Record the number of observations
            count = len(curve)
            observation_counts.append(count)

    print(pd.Series(observation_counts).describe())

if __name__ == "__main__":
    main()
