library(ggplot2)
library(repr)
options(repr.plot.width=10, repr.plot.height=8)
library(ggrepel)
require(plyr)

data <- read.csv("../../data/raw/gc_oosterhoff/Collected Globular Cluster Information - Globular Clusters Summary.csv")

data$Oost.Type <- factor(data$Oost.Type, levels = c("I", "II", "III", "Oo-Int", "Conflicted"))
data$Location <- ifelse(data$GC.Location == "Milky Way", "Milky Way", "Non-Milky Way")

plot <- ggplot(data, aes(x=Mean.RRab.Period, y=Metalicity, color=Oost.Type, shape=Oost.Type)) +
    geom_point() +
    geom_text_repel(aes(label=NGC), box.padding = 0.35, show_guide = FALSE) +
    xlab("Mean RRab Period (days)") + 
    ylab("Metalicity [Fe/H]") + 
    ggtitle("Globular Clusters by Oosterhoff Classification") +
    guides(color=guide_legend(title="Oosterhoff\nClassification"), shape=guide_legend(title="Oosterhoff\nClassification")) +
    theme_set(theme_gray(base_size = 14)) +
    scale_color_manual(values=c("#1b9e77", "#d95f02", "#e6ab02", "#e7298a", "#7570b3"))

ggsave("../../reports/figures/globular_clusters/globular_clusters_by_oosterhoff_type.png", plot, width=13, height=8)

plot_by_location <- ggplot(data[data$Oost.Type %in% c("I", "II", "III", "Oo-Int"),], aes(x=Mean.RRab.Period, y=Metalicity, color=Oost.Type, shape=Oost.Type)) +
    geom_point() +
	facet_wrap(~Location) +
    geom_text_repel(aes(label=NGC), box.padding = 0.35, show_guide = FALSE) +
    xlab("Mean RRab Period (days)") + 
    ylab("Metalicity [Fe/H]") + 
    ggtitle("Globular Clusters by Oosterhoff Classification and Location") +
    guides(color=guide_legend(title="Oosterhoff\nClassification"), shape=guide_legend(title="Oosterhoff\nClassification")) +
    theme_set(theme_gray(base_size = 14)) +
    scale_color_manual(values=c("#1b9e77", "#d95f02", "#e6ab02", "#e7298a", "#7570b3"))

ggsave("../../reports/figures/globular_clusters/globular_clusters_by_location.png", plot_by_location, width=13, height=8)
