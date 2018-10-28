from plotnine import *

import os
import os.path

import pandas as pd

def main():
    i_input_dir = "../../data/raw/lmc/curves/I"
    v_input_dir = "../../data/raw/lmc/curves/V"

    output_dir = "../../reports/figures/light_curve_examples"
    os.makedirs(output_dir, exist_ok=True)

    data_id_number = "00001"
    data_id = "OGLE-LMC-RRLYR-{}".format(data_id_number)

    bands = [
        ("i", i_input_dir),
        ("v", v_input_dir)
    ]

    # Get the period to use for the period folded light curves
    rrab_data_file = "../../data/raw/lmc/RRab.csv"
    rrab = pd.read_csv(rrab_data_file)

    period = rrab[rrab["id"] == data_id]["period"].iloc[0]

    for band, band_dir in bands:
        data_file = os.path.join(band_dir, data_id + ".csv")

        data = pd.read_csv(data_file)

        # Regular light curve
        plot_raw = ggplot(data, aes("time", "mag")) +\
                geom_point() +\
                scale_y_reverse() +\
                xlab("Time (MJD)") +\
                ylab("Magnitude (mag)") +\
                ggtitle("Light Curve - {} - {} band".format(data_id, band.upper())) +\
                theme(
                    figure_size=(9, 9),
                    text=element_text(size=16)
                )

        plot_filename = "light_curve_raw_{}.png".format(band)
        plot_file = os.path.join(output_dir, plot_filename)

        ggsave(plot_raw, plot_file)

        # Period folded light curve
        data["phase"] = data["time"] % period

        plot_folded = ggplot(data, aes("phase", "mag")) +\
                geom_point() +\
                scale_y_reverse() +\
                xlab("Phase") +\
                ylab("Magnitude (mag)") +\
                ggtitle("Folded Light Curve - {} - {} band".format(data_id, band.upper())) +\
                theme(
                    figure_size=(9, 9),
                    text=element_text(size=16)
                )

        plot_folded_filename = "light_curve_folded_{}.png".format(band)
        plot_folded_file = os.path.join(output_dir, plot_folded_filename)

        ggsave(plot_folded, plot_folded_file)

if __name__ == "__main__":
    main()
