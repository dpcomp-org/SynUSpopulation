#
# Download the data from various sources and combine as necessary
#

# Note: Website appears to have a 'us' file that has the whole country in it.
#
STATES=ak al ar az ca co ct dc de fl ga hi ia id il in ks ky la ma md me mi mn mo ms mt nc nd ne nh nj nm nv ny oh ok or pa pr ri sc sd tn tx ut va vt wa wi wv wy
CENSUS=https://www2.census.gov/programs-surveys/acs/data/pums/2015/5-Year

all:
	make census-download
	make census-unzip


census-download:
	@echo Downloading ACS 2015 5-Year PUMS from US Census Website
	for HP in h p; do \
	    mkdir -p $${HP}; \
	    for STATE in ${STATES} ; do \
		echo checking for $${HP}/csv_$${HP}$${STATE}.zip; \
		if [ ! -f $${HP}/csv_$${HP}$${STATE}.zip ]; then \
	            wget ${CENSUS}/csv_$${HP}$${STATE}.zip ; \
	            mv csv_$${HP}$${STATE}.zip $${HP}; \
		fi; \
            done; \
	done

census-unzip:
	@echo Unzipping ACS 2015 5-Year PUMS from US Census Website
	for HP in h p; do \
	    for STATE in ${STATES} ; do \
	      ( cd $${HP}; if ! unzip -nq csv_$${HP}$${STATE}.zip ss15$${HP}$${STATE}.csv ; \
                                then mkdir -p badzip ; mv csv_$${HP}$${STATE}.zip badzip ; echo BADZIP ; \
                           fi) \
	    done; \
	done

census-makehashes:
	sha1deep -l h/*.csv p/*.csv > hashes.txt
