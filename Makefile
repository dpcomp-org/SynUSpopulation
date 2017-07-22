#
# Targets:
#
# all -- Generate fake people for all 50 states + DC and PR
# e2e -- Generate fake people for the 2018 End To End test (RI, WV and WA)

PYTHON=python3

all:
	$(PYTHON) bin/download.py --config=config.ini --threads=6


outputs/rep_counts_2014.csv:
	(cd outputs; python3.6 ../programs/gen_counts.py --output=rep_counts_2014.csv ../inputs/2014/p ../inputs/2014/h)

outputs/erial_idx_dict.p: outputs/rep_counts_2014.csv
	/bin/rm -f outputs/housing_rep/*.csv
	(cd outputs; python3.6 ../programs/rep_syn_housing.py --outdir housing_rep/ ../inputs/2014/h rep_counts_2014.csv)

check:
	mkdir -p checkdir
	python3.6 programs/gen_counts.py --maxstates=2 --output=checkdir/rep_counts-2states.csv inputs/p inputs/h	


e2e:
	(cd inputs;
