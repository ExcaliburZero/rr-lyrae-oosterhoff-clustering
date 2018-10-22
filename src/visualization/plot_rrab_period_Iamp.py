from plotnine import *

import os
import os.path

import pandas as pd

def main():
    data_files = [
        ("../../data/raw/lmc/RRab.csv", "LMC"),
        ("../../data/raw/smc/RRab.csv", "SMC")
    ]

    output_dir = "../../reports/figures/rrab_period_Iamp"
    os.makedirs(output_dir, exist_ok=True)

    for data_f, title in data_files:
        data = pd.read_csv(data_f)

        plot = ggplot(data, aes("period", "I_amplitude")) +\
            stat_bin_2d(bins=150) +\
            xlab("Period (days)") +\
            ylab("I-band Amplitude (mag)") +\
            ggtitle("OGLE IV {} RRab Period vs I-band Amplitude".format(title)) +\
            theme(figure_size=(9, 9))

        plot_file = os.path.join(output_dir, "rrab_per_Iamp_{}.png".format(title))

        ggsave(plot, plot_file)

if __name__ == "__main__":
    main()
