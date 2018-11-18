library(ggplot2)
library(repr)
options(repr.plot.width=10, repr.plot.height=8)
library(ggrepel)
require(plyr)

data <- read.csv("../../data/raw/gc_oosterhoff/Collected Globular Cluster Information - Globular Clusters Summary.csv")

data$Oost.Type <- factor(data$Oost.Type, levels = c("I", "II", "III", "Oo-Int", "Conflicted"))

#######
# LMC #
#######
ogleLmc <- read.csv("../../data/interim/lmc/RRab_clustered.csv")

ogleLmcOoI <- subset(ogleLmc, is_oost_ii == "False")
ogleLmcOoII <- ogleLmc[ogleLmc$is_oost_ii == "True",]

allWithLmc <- data[,c("NGC", "Mean.RRab.Period", "Metalicity", "Oost.Type")]
allWithLmc <- rbind(allWithLmc, data.frame(Mean.RRab.Period=mean(ogleLmcOoI$period), NGC="LMC OoI?", Metalicity=mean(ogleLmcOoI$metalicity_jk_v), Oost.Type="LMC"))
allWithLmc <- rbind(allWithLmc, data.frame(Mean.RRab.Period=mean(ogleLmcOoII$period), NGC="LMC OoII?", Metalicity=mean(ogleLmcOoII$metalicity_jk_v), Oost.Type="LMC"))

lmcPlot <- ggplot(allWithLmc[allWithLmc$Oost.Type %in% c("I", "II", "III", "Oo-Int", "LMC"),], aes(x=Mean.RRab.Period, y=Metalicity, color=Oost.Type, shape=Oost.Type)) +
    geom_point() +
    geom_text_repel(aes(label=NGC), box.padding = 0.35, show_guide = FALSE) +
    xlab("Mean RRab Period (days)") + 
    ylab("Metalicity [Fe/H]") + 
    ggtitle("LMC Clusters plotted with Globular Clusters") +
    scale_color_manual(values=c("#f8766d", "#7cae00", "#00bfc4", "#c77cff", "#f7a32c")) +
    guides(shape=guide_legend(title="Oosterhoff Type"), color=guide_legend(title="Oosterhoff Type")) +
    theme_set(theme_gray(base_size = 14)) +
    scale_color_manual(values=c("#1b9e77", "#d95f02", "#e6ab02", "#e7298a", "#9b59b6"))

ggsave("../../reports/figures/globular_clusters/lmc_clusters_with_globular_clusters.png", lmcPlot, width=13, height=8)

#######
# SMC #
#######
ogleSmc <- read.csv("../../data/interim/smc/RRab_clustered.csv")

ogleSmcOoI <- subset(ogleSmc, is_oost_ii == "False")
ogleSmcOoII <- ogleSmc[ogleSmc$is_oost_ii == "True",]

allWithSmc <- data[,c("NGC", "Mean.RRab.Period", "Metalicity", "Oost.Type")]
allWithSmc <- rbind(allWithSmc, data.frame(Mean.RRab.Period=mean(ogleSmcOoI$period), NGC="SMC OoI?", Metalicity=mean(ogleSmcOoI$metalicity_jk_v), Oost.Type="SMC"))
allWithSmc <- rbind(allWithSmc, data.frame(Mean.RRab.Period=mean(ogleSmcOoII$period), NGC="SMC OoII?", Metalicity=mean(ogleSmcOoII$metalicity_jk_v), Oost.Type="SMC"))

smcPlot <- ggplot(allWithSmc[allWithSmc$Oost.Type %in% c("I", "II", "III", "Oo-Int", "SMC"),], aes(x=Mean.RRab.Period, y=Metalicity, color=Oost.Type, shape=Oost.Type)) +
    geom_point() +
    geom_text_repel(aes(label=NGC), box.padding = 0.35, show_guide = FALSE) +
    xlab("Mean RRab Period (days)") + 
    ylab("Metalicity [Fe/H]") + 
    ggtitle("SMC Clusters plotted with Globular Clusters") +
    scale_color_manual(values=c("#f8766d", "#7cae00", "#00bfc4", "#c77cff", "#f7a32c")) +
    guides(shape=guide_legend(title="Oosterhoff Type"), color=guide_legend(title="Oosterhoff Type")) +
    theme_set(theme_gray(base_size = 14)) +
    scale_color_manual(values=c("#1b9e77", "#d95f02", "#e6ab02", "#e7298a", "#9b59b6"))

ggsave("../../reports/figures/globular_clusters/smc_clusters_with_globular_clusters.png", smcPlot, width=13, height=8)
