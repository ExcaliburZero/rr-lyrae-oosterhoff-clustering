import os.path

import pandas as pd

def main():
    lmc_dir = "../../data/interim/lmc"
    smc_dir = "../../data/interim/smc"

    output_dir = "../../data/processed"

    types = ["RRab", "RRc", "RRd", "aRRd"]

    columns = ["Sub-type", "Mean FM Period", "Mean FM I-band Amplitude", "Mean FO Period", "Mean FO I-band Amplitude"]
    data = []

    for t in types:
        lmc_type_file = os.path.join(lmc_dir, "{}.csv".format(t))
        lmc_of_type = pd.read_csv(lmc_type_file)

        smc_type_file = os.path.join(smc_dir, "{}.csv".format(t))
        smc_of_type = pd.read_csv(smc_type_file)

        all_of_type = pd.concat([lmc_of_type, smc_of_type])

        if t == "RRab":
            mean_fm_period = all_of_type["period"].mean()
            mean_fm_I_amplitude = all_of_type["I_amplitude"].mean()

            mean_fo_period = None
            mean_fo_I_amplitude = None
        elif t == "RRc":
            mean_fm_period = None
            mean_fm_I_amplitude = None

            mean_fo_period = all_of_type["period"].mean()
            mean_fo_I_amplitude = all_of_type["I_amplitude"].mean()
        elif t == "RRd" or t == "aRRd":
            mean_fm_period = all_of_type["fm_period"].mean()
            mean_fm_I_amplitude = all_of_type["fm_I_amplitude"].mean()

            mean_fo_period = all_of_type["fo_period"].mean()
            mean_fo_I_amplitude = all_of_type["fo_I_amplitude"].mean()

        data.append(
            (t, mean_fm_period, mean_fm_I_amplitude, mean_fo_period, mean_fo_I_amplitude)
        )

    summary = pd.DataFrame(data, columns=columns)

    summary_filename = "type_statistics.csv"
    summary_file = os.path.join(output_dir, summary_filename)

    summary.to_csv(summary_file, index=False)

if __name__ == "__main__":
    main()
