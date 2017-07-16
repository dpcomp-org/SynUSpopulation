#
# Download the data from various sources and combine as necessary
#

STATES=ak al ar az ca co ct dc de fl ga hi ia id il in ks ky la ma md me mi mn mo ms mt nc nd ne nh nj nm nv ny oh ok or pa pr ri sc sd tn tx us ut va vt wa wi wv wy
CENSUS=https://www2.census.gov/programs-surveys/acs/data/pums/2015/5-Year

download-census:
	@echo Downloading ACS 2015 5-Year PUMS from US Census Website
	for HP in h p; do \
	    for STATE in ${STATES} ; do \
	        wget ${CENSUS}/csv_$${HP}$${STATE}.zip ; \
            done; \
	done

