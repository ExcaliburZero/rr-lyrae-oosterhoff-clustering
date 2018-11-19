LMC_DATA_FILES = \
	data/raw/lmc/README \
	data/raw/lmc/RRab.dat \
	data/raw/lmc/RRc.dat \
	data/raw/lmc/RRd.dat \
	data/raw/lmc/aRRd.dat \
	data/raw/lmc/ident.dat \
	data/raw/lmc/phot.tar.gz \
	data/raw/lmc/phot/

LMC_INTERIM_FILES = \
	data/interim/lmc/RRab.csv \
	data/interim/lmc/RRc.csv \
	data/interim/lmc/RRd.csv \
	data/interim/lmc/aRRd.csv \
	data/interim/lmc/all.csv \
	data/interim/lmc/curves/ \
	data/interim/lmc/RRab_extracted.csv \
	data/interim/lmc/RRab_clustered.csv

SMC_DATA_FILES = \
	data/raw/smc/README \
	data/raw/smc/RRab.dat \
	data/raw/smc/RRc.dat \
	data/raw/smc/RRd.dat \
	data/raw/smc/aRRd.dat \
	data/raw/smc/ident.dat \
	data/raw/smc/phot.tar.gz \
	data/raw/smc/phot/

SMC_INTERIM_FILES = \
	data/interim/smc/RRab.csv \
	data/interim/smc/RRc.csv \
	data/interim/smc/RRd.csv \
	data/interim/smc/aRRd.csv \
	data/interim/smc/all.csv \
	data/interim/smc/curves/ \
	data/interim/smc/RRab_extracted.csv \
	data/interim/smc/RRab_clustered.csv

ANALYSIS = \
	reports/RRab_OGLE_IV_Clustering.pdf \
	reports/RRab_OGLE_IV_Clustering_files/ \
	data/processed/light_curve_observation_stats.txt \
	data/processed/type_statistics.csv \
	reports/figures/globular_clusters/globular_clusters_by_oosterhoff_type.png \
	reports/figures/globular_clusters/globular_clusters_by_location.png \
	reports/figures/globular_clusters/lmc_clusters_with_globular_clusters.png \
	reports/figures/globular_clusters/smc_clusters_with_globular_clusters.png \
	reports/Thesis.pdf

.PHONY: all

#all: $(LMC_DATA_FILES) $(LMC_INTERIM_FILES) $(SMC_DATA_FILES) $(SMC_INTERIM_FILES) $(ANALYSIS)
all: $(ANALYSIS)

############
# LMC Data #
############

data/raw/lmc/README:
	wget -P data/raw/lmc ftp://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/lmc/rrlyr/README

data/raw/lmc/RRab.dat:
	wget -P data/raw/lmc ftp://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/lmc/rrlyr/RRab.dat

data/raw/lmc/RRc.dat:
	wget -P data/raw/lmc ftp://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/lmc/rrlyr/RRc.dat

data/raw/lmc/RRd.dat:
	wget -P data/raw/lmc ftp://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/lmc/rrlyr/RRd.dat

data/raw/lmc/aRRd.dat:
	wget -P data/raw/lmc ftp://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/lmc/rrlyr/aRRd.dat

data/raw/lmc/ident.dat:
	wget -P data/raw/lmc ftp://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/lmc/rrlyr/ident.dat

data/raw/lmc/phot.tar.gz:
	wget -P data/raw/lmc ftp://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/lmc/rrlyr/phot.tar.gz

data/raw/lmc/phot/: data/raw/lmc/phot.tar.gz
	tar -zxvf data/raw/lmc/phot.tar.gz -C data/raw/lmc
	touch data/raw/lmc/phot/

data/interim/lmc/RRab.csv data/interim/lmc/RRc.csv data/interim/lmc/RRd.csv data/interim/lmc/aRRd.csv data/interim/lmc/all.csv: data/raw/lmc/RRab.dat data/raw/lmc/RRc.dat data/raw/lmc/RRd.dat data/raw/lmc/aRRd.dat src/data/lmc/process_dat_files.py
	mkdir -p data/interim/lmc
	python src/data/lmc/process_dat_files.py data/raw/lmc data/interim/lmc
	touch data/interim/lmc

data/interim/lmc/curves/: data/raw/lmc/phot/ src/data/lmc/process_light_curves.py
	python src/data/lmc/process_light_curves.py data/raw/lmc/phot data/interim/lmc/curves

data/interim/lmc/RRab_extracted.csv: src/data/feature_extraction.py data/interim/lmc/RRab.csv data/interim/lmc/curves/
	python src/data/feature_extraction.py data/interim/lmc/RRab.csv data/interim/lmc/curves/ data/interim/lmc/RRab_extracted.csv

############
# SMC Data #
############

data/raw/smc/README:
	wget -P data/raw/smc ftp://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/smc/rrlyr/README

data/raw/smc/RRab.dat:
	wget -P data/raw/smc ftp://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/smc/rrlyr/RRab.dat

data/raw/smc/RRc.dat:
	wget -P data/raw/smc ftp://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/smc/rrlyr/RRc.dat

data/raw/smc/RRd.dat:
	wget -P data/raw/smc ftp://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/smc/rrlyr/RRd.dat

data/raw/smc/aRRd.dat:
	wget -P data/raw/smc ftp://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/smc/rrlyr/aRRd.dat

data/raw/smc/ident.dat:
	wget -P data/raw/smc ftp://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/smc/rrlyr/ident.dat

data/raw/smc/phot.tar.gz:
	wget -P data/raw/smc ftp://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/smc/rrlyr/phot.tar.gz

data/raw/smc/phot/: data/raw/smc/phot.tar.gz
	tar -zxvf data/raw/smc/phot.tar.gz -C data/raw/smc
	touch data/raw/smc/phot/

data/interim/smc/RRab.csv data/interim/smc/RRc.csv data/interim/smc/RRd.csv data/interim/smc/aRRd.csv data/interim/smc/all.csv: data/raw/smc/RRab.dat data/raw/smc/RRc.dat data/raw/smc/RRd.dat data/raw/smc/aRRd.dat src/data/smc/process_dat_files.py
	mkdir -p data/interim/smc
	python src/data/smc/process_dat_files.py data/raw/smc data/interim/smc
	touch data/interim/smc

data/interim/smc/curves/: data/raw/smc/phot/ src/data/smc/process_light_curves.py
	python src/data/smc/process_light_curves.py data/raw/smc/phot data/interim/smc/curves

data/interim/smc/RRab_extracted.csv: src/data/feature_extraction.py data/interim/smc/RRab.csv data/interim/smc/curves/
	python src/data/feature_extraction.py data/interim/smc/RRab.csv data/interim/smc/curves/ data/interim/smc/RRab_extracted.csv

############
# Analysis #
############

reports/RRab_OGLE_IV_Clustering.pdf reports/RRab_OGLE_IV_Clustering_files/ data/interim/lmc/RRab_clustered.csv data/interim/smc/RRab_clustered.csv: notebooks/RRab_OGLE_IV_Clustering.ipynb data/interim/lmc/RRab_extracted.csv data/interim/smc/RRab_extracted.csv
	jupyter nbconvert --output-dir="./reports" --execute --to pdf notebooks/RRab_OGLE_IV_Clustering.ipynb

data/processed/light_curve_observation_stats.txt: src/tools/light_curve_observation_stats.py data/interim/lmc/curves/ data/interim/smc/curves/
	mkdir -p data/processed
	cd src/tools &&\
		python light_curve_observation_stats.py > ../../data/processed/light_curve_observation_stats.txt

data/processed/type_statistics.csv: src/tools/rr_lyrae_type_statistics.py data/interim/lmc/RRab.csv data/interim/lmc/RRc.csv data/interim/lmc/RRd.csv data/interim/lmc/aRRd.csv data/interim/smc/RRab.csv data/interim/smc/RRc.csv data/interim/smc/RRd.csv data/interim/smc/aRRd.csv
	mkdir -p data/processed
	cd src/tools &&\
		python rr_lyrae_type_statistics.py

reports/figures/light_curve_examples/: src/visualization/plot_light_curve_examples.py data/interim/lmc/curves/
	cd src/visualization &&\
		python plot_light_curve_examples.py

reports/figures/globular_clusters/oosterhoff_1939.png: src/visualization/plot_oosterhoff_1939.py data/raw/gc_oosterhoff/Oosterhoff_1939.csv
	mkdir -p reports/figures/globular_clusters/
	cd src/visualization &&\
		python plot_oosterhoff_1939.py

reports/figures/globular_clusters/globular_clusters_by_oosterhoff_type.png reports/figures/globular_clusters/globular_clusters_by_location.png: src/visualization/plot_globular_clusters.R data/raw/gc_oosterhoff/Collected\ Globular\ Cluster\ Information\ -\ Globular\ Clusters\ Summary.csv
	mkdir -p reports/figures/globular_clusters/
	cd src/visualization &&\
		Rscript plot_globular_clusters.R

reports/figures/globular_clusters/lmc_clusters_with_globular_clusters.png reports/figures/globular_clusters/smc_clusters_with_globular_clusters.png: src/visualization/plot_magellanic_clouds_with_gcs.R data/raw/gc_oosterhoff/Collected\ Globular\ Cluster\ Information\ -\ Globular\ Clusters\ Summary.csv data/interim/lmc/RRab_clustered.csv data/interim/smc/RRab_clustered.csv
	mkdir -p reports/figures/globular_clusters/
	cd src/visualization &&\
		Rscript plot_magellanic_clouds_with_gcs.R

reports/Thesis.pdf: reports/Thesis.tex reports/RRab_OGLE_IV_Clustering.pdf reports/figures/light_curve_examples/ reports/figures/globular_clusters/oosterhoff_1939.png reports/figures/globular_clusters/globular_clusters_by_oosterhoff_type.png reports/figures/globular_clusters/globular_clusters_by_location.png reports/figures/globular_clusters/lmc_clusters_with_globular_clusters.png reports/figures/globular_clusters/smc_clusters_with_globular_clusters.png
	cd reports &&\
		pdflatex Thesis.tex &&\
		bibtex Thesis &&\
		pdflatex Thesis.tex &&\
		pdflatex Thesis.tex
