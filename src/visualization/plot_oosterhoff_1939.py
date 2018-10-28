from plotnine import *

import os
import os.path

import numpy as np
import pandas as pd

def main():
    input_dir = "../../data/raw/gc_oosterhoff"

    output_dir = "../../reports/figures/globular_clusters"
    os.makedirs(output_dir, exist_ok=True)

    data_file_name = "Oosterhoff_1939.csv"
    data_file = os.path.join(input_dir, data_file_name)

    data = pd.read_csv(data_file)

    xmin = np.min(data["MeanRRabPeriod"])
    xmax = np.max(data["MeanRRabPeriod"]) + 0.01

    plot = ggplot(data, aes("MeanRRabPeriod", "MeanRRcPeriod", label="GlobularCluster")) +\
            geom_point(size=3) +\
            geom_text(va="top", ha="left", nudge_y=-0.001, nudge_x=0.002, size=14) +\
            xlim(xmin, xmax) +\
            xlab("Mean RRab Period (Days)") +\
            ylab("Mean RRc Period (Days)") +\
            ggtitle("Globular Clusters Examined in Oosterhoff (1939)") +\
            theme(
                figure_size=(12, 9),
                text=element_text(size=16)
            )

    plot_file_name = "oosterhoff_1939.png"
    plot_file = os.path.join(output_dir, plot_file_name)

    ggsave(plot, plot_file)

if __name__ == "__main__":
    main()
