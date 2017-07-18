#
# Download the data from various sources and combine as necessary
#

# Note: Website appears to have a 'us' file that has the whole country in it.
#
STATES=ak al ar az ca co ct dc de fl ga hi ia id il in ks ky la ma md me mi mn mo ms mt nc nd ne nh nj nm nv ny oh ok or pa pr ri sc sd tn tx ut va vt wa wi wv wy
YEAR=2014
ACS=https://www2.census.gov/programs-surveys/acs/data/pums/${YEAR}/5-Year

DOWNLOAD=${ACS_2014}

all:
	make census-download
	make census-unzip


census-download:
	@echo Downloading ACS ${YEAR} 5-Year PUMS from US Census Website
	for HP in h p; do \
	    mkdir -p ${YEAR}/$${HP}; \
	    for STATE in ${STATES} ; do \
	        FILE=csv_$${HP}$${STATE}.zip; \
                ZIP=${YEAR}/$${HP}/$${FILE}; \
		echo checking for $${ZIP}; \
		if [ ! -f $${ZIP} ]; then \
	            /bin/rm -f $${FILE} && wget ${ACS}/$${FILE}  && mv $${FILE} $${ZIP}; \
		fi; \
            done; \
	done

census-unzip:
	@echo Unzipping ACS ${YEAR} 5-Year PUMS from US Census Website
	for HP in h p; do \
	    for STATE in ${STATES} ; do \
	      ( cd ${YEAR}/$${HP}; if ! unzip -nq csv_$${HP}$${STATE}.zip ; then \
                                       mkdir -p badzip ; mv csv_$${HP}$${STATE}.zip badzip ; echo BADZIP ; \
                                   fi ; \
				   /bin/rm -f ACS*README.pdf) \
	    done; \
	done

census-makehashes:
	sha1deep -l h/*.csv p/*.csv > hashes.txt
