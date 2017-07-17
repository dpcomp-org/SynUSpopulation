all:
	(cd inputs;make all)

outputs/rep_counts.csv:
	python3.6 programs/gen_counts.py --output=outputs/rep_counts.csv inputs/p inputs/h

check:
	mkdir -p checkdir
	python3.6 programs/gen_counts.py --maxstates=2 --output=checkdir/rep_counts-2states.csv inputs/p inputs/h	
