import os.path
import subprocess
import sys

import pandas as pd

def main():
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    dat_files = ["RRab", "RRc", "RRd", "aRRd"]

    rrab_rrc_cols = ["id", "mean_I_magnitude", "mean_V_magnitude", "period"
        , "period_uncertainty", "time_max_bright", "I_amplitude", "R21"
        , "phi21", "R31", "phi31"]

    rrd_arrd_cols = ["id", "mean_I_magnitude", "mean_V_magnitude", "fo_period"
        , "fo_period_uncertainty", "fo_time_max_bright", "fo_I_amplitude"
        , "fo_R21", "fo_phi21", "fo_R31", "fo_phi31", "fm_period"
        , "fm_period_uncertainty", "fm_time_max_bright", "fo_I_amplitude"
        , "fo_R21", "fo_phi21", "fo_R31", "fo_phi31"]

    column_sets = [
          rrab_rrc_cols
        , rrab_rrc_cols
        , rrd_arrd_cols
        , rrd_arrd_cols
    ]

    fix_rrab(input_dir, dat_files[0] + ".dat")

    [dat_to_csv(input_dir, output_dir, dat, columns) for (dat, columns) in zip(dat_files, column_sets)]

    combine_dat_files(output_dir, "RRab", "RRc", "RRd", "aRRd")

def fix_rrab(input_dir, rrab):
    rrab_file = os.path.join(input_dir, rrab)

    lines = []

    incorrect = "OGLE-LMC-RRLYR-12564  18.794 19.023  0.4568447 0.0000005 2450455.47085  0.732  0.481 3.978  0.336 1.935"

    correct =   "OGLE-LMC-RRLYR-12564  18.794 19.023  0.4568447 0.0000005      -       0.732  0.481 3.978  0.336 1.935"

    with open(rrab_file) as f:
        for line in f:
            line = line[:-1]
            if line == incorrect:
                lines.append(correct)
            else:
                lines.append(line)

    with open(rrab_file, "w") as f:
        f.write("\n".join(lines))

def dat_to_csv(input_dir, output_dir, dat, columns):
    data_file = os.path.join(input_dir, dat + ".dat")
    output_file = os.path.join(output_dir, dat + ".csv")

    data = pd.read_fwf(data_file, header=None)

    if columns is not None:
        data.columns = columns
        
        data.to_csv(output_file, index=False)
    else:
        data.to_csv(output_file, index=False, header=False)

    remove_empty_cells(os.path.join(output_dir, dat))

def remove_empty_cells(dat):
    """
    Remove all instances of "-"s indicating missing values, as csv files
    represent missing values as blank entries.
    """
    f = dat
    command = "cat '%s.csv' | sed 's/,-/,/g' > '%s_2.csv' && cat %s_2.csv > %s.csv && rm %s_2.csv" % (f, f, f, f, f)

    subprocess.call(command, shell=True)

def combine_dat_files(directory, rrab, rrc, rrd, arrd):
    rrab_dat = pd.read_csv(os.path.join(directory, rrab + ".csv"))
    rrc_dat = pd.read_csv(os.path.join(directory, rrc + ".csv"))
    rrd_dat = pd.read_csv(os.path.join(directory, rrd + ".csv"))
    arrd_dat = pd.read_csv(os.path.join(directory, arrd + ".csv"))

    rrab_dat = rrab_dat[["id", "period"]]
    rrab_dat["category"] = "RRab"

    rrc_dat = rrc_dat[["id", "period"]]
    rrc_dat["category"] = "RRc"

    rrd_dat = rrd_dat[["id", "fo_period"]]
    rrd_dat.columns = ["id", "period"]
    rrd_dat["category"] = "RRd"

    arrd_dat = arrd_dat[["id", "fo_period"]]
    arrd_dat.columns = ["id", "period"]
    arrd_dat["category"] = "aRRd"

    all_dat = pd.concat([rrab_dat, rrc_dat, rrd_dat, arrd_dat])
    all_dat.to_csv(os.path.join(directory, "all.csv"), index=False)

if __name__ == "__main__":
    main()
