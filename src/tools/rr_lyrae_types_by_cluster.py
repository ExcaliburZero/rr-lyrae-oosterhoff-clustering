import os.path

import pandas as pd

def main():
    lmc_dir = "../../data/raw/lmc"
    smc_dir = "../../data/raw/smc"

    output_dir = "../../data/processed"

    types = ["RRab", "RRc", "RRd", "aRRd"]

    columns = ["Cloud", "Type", "Count"]
    data = []

    for t in types:
        type_file = os.path.join(lmc_dir, "{}.csv".format(t))
        all_of_type = pd.read_csv(type_file)

        count = len(all_of_type)
        data.append(("LMC", t, count))

    for t in types:
        type_file = os.path.join(smc_dir, "{}.csv".format(t))
        all_of_type = pd.read_csv(type_file)

        count = len(all_of_type)
        data.append(("SMC", t, count))

    summary = pd.DataFrame(data, columns=columns)

    summary_filename = "type_counts.csv"
    summary_file = os.path.join(output_dir, summary_filename)

    summary.to_csv(summary_file, index=False)

if __name__ == "__main__":
    main()
