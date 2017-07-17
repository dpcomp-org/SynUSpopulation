all:
	(cd inputs;make all)

outputs/rep_counts.csv:
	python3.6 programs/gen_counts.py --output=outputs/rep_counts.csv inputs/p inputs/h
