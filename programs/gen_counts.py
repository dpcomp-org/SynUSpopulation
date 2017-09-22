#!/usr/bin/env python3.5
# gen_counts.py
# William Sexton
# Last Modified: 9/17/2017
""" Generate counts over serialno's """
#inputs: argv[1] - raw ACS person files (in a directory?)
#        argv[2] - raw ACS housing files (in a directory)

#imports
import os.path
import logging
import glob
import pandas as pd
import numpy as np
import acs

def process_chunk(df, cnt_dict, serials, unitType):
    """ """
    # map serialno to year, first 4 digits of serialno are the year.   
    df["YEAR"] = df[acs.SERIALNO].map(lambda serialno: serialno[:4]) 
    
    if unitType == "GQ":
        df = df[(df["RELP"] == 16) | (df["RELP"] == 17)] # filter to GQ type
        cnt_dict["weight"] += df["PWGTP"].sum()
    else:
        df = df[df["TYPE"] == 1] # filter to housing unit
        cnt_dict["weight"] += df["WGTP"].sum()

    cnt_dict["total"] += len(df.index)
    serials.extend(df[acs.SERIALNO].tolist())

    # counting group quarters by year
    cnt = df.groupby("YEAR").size() 
    for key in cnt_dict:
        cnt_dict[key] += cnt.get(key, 0)
    return cnt_dict, serials

def set_alpha(df, cnt_dict, alpha, unitType):
    """df is a pandas dataframe containing a chunk of data
       from the raw ACS housing data.
       count_dict, year_code,defined elsewhere in code for bookkeeping purposes.
       alpha_h stores prior probabilities for Dirichlet distribution
       over records of housing data."""
    df["YEAR"] = df[acs.SERIALNO].map(lambda serialno: serialno[:4]) 
    
    df["YEARCNT"] = df["YEAR"].map(cnt_dict)
    if unitType == "GQ":
        df = df[(df["RELP"] == 16) | (df["RELP"] == 17)] # filter to GQ
        alpha.extend((df["PWGTP"]*df["YEARCNT"]/cnt_dict["weight"]).tolist())
    else:
        df = df[df["TYPE"] == 1] # filter to housing units
        alpha.extend((df["WGTP"]*df["YEARCNT"]/count_dict["weight"]).tolist())
    return alpha

def main(persondir,housingdir):
    """Builds synthetic population using Bayesian bootstrapping process
       on ACS housing records and then populating each
       housing unit/group quarters unit with person records
       from the ACS person data files."""     
    """1. Configure log"""
    # Change filename with each run (if desired) otherwise info
    # will append to same log.
    logging_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(filename='gen_counts.log',
            format='%(asctime)s %(message)s', level=logging_level)
    logging.info('Started')
    # Get the files form the provided directories
    # Notes that glob.glob() filenames are sorted.
    # Strictly there is no reason to do this, but it makes debugging easier.
    filenames_person = sorted(glob.glob(os.path.join(persondir,"*.csv")))
    logging.debug("filenames_person: {}".format(filenames_person))
    filenames_housing = sorted(glob.glob(os.path.join(housingdir,"*.csv")))
    logging.debug("filenames_housing: {}".format(filenames_housing))
    """2. Set up Bookkeeping"""
    #
    # count_dict is a single place where we keep track of the count,
    # for each year, of households & group quarters.
    #
    # index: n{YEAR}[h|g]  where YEAR is the 4 digit year
    # and h|g is household or group quarters.
    #
    cnt_GQ = {"total":0, "2010":0, "2011":0, "2012":0,
                  "2013":0, "2014":0, "weight":0} 
    cnt_HH = {"total":0, "2010":0, "2011":0, "2012":0,
                  "2013":0, "2014":0, "weight":0}

    """First pass of housing files to collect aggregate counts
       and store serial   numbers of households"""
    # Files processed in chunks to reduce memory footprint.
    # This approach requires multiple read ins of the data to complete
    # the Bayesian bootstrapping but it works. If there is a better way
    # of doing this, I'd love to see it.

    # serials_HH is the array of serial numbers of households
    serials_HH = []
    for f in filenames_housing[0:args.maxstates]:
        logging.info("computing serials_h reading housing "+f)
        for chunk in pd.read_csv(f,
                                 usecols=[acs.SERIALNO,"TYPE","WGTP"],
                                 chunksize=100000):
            cnt_HH, serials_HH = process_housing_chunk(chunk,
                                                          cnt_HH,
                                                          serials_HH,
                                                          "HH")
    """First pass at person files to collect aggregate counts
       and store serial numbers of group quarters records"""
    # serials_GQ is an array of the serial numbers of group quarters
    serials_GQ = []
    for f in filenames_person[0:args.maxstates]:
        logging.info("computing serials_g reading persons "+f)
        for chunk in pd.read_csv(f,
                                 usecols=[acs.SERIALNO,"PWGTP","RELP"],
                                 chunksize=100000):
            cnt_GQ, serials_GQ = process_person_chunk(chunk,
                                                         count_GQ, 
                                                         serials_GQ,
                                                         "GQ")
    """Next pass at housing is to define the prior parameter alpha
       for the dirichlet distribution over households."""
    # alpha_HH is the array of weights of households
    alpha_HH = []
    for f in filenames_housing[0:args.maxstates]:
        logging.info("computing alpha_h reading housing "+f)
        for chunk in pd.read_csv(f,
                                 usecols=[acs.SERIALNO, "TYPE", "WGTP"],
                                 chunksize=100000):
            alpha_h = set_alpha_h(chunk, count_dict, alpha_h)
    """Next pass at person is to define the prior parameter alpha
       for the dirichlet distribution over group quarters."""
    # alpha_g is the array of weights of group quarters
    alpha_g = []
    for f in filenames_person[0:args.maxstates]:
        logging.info("computing alpha_g reading persons "+f)
        for chunk in pd.read_csv(f,
                                 usecols=[acs.SERIALNO, "RELP", "PWGTP"],
                                 chunksize=100000):
            alpha_g = set_alpha_g(chunk, count_dict, alpha_g)
    # Verify that the number of weights for households and group quarters
    # matches the number of labels. 
    assert len(serials_g) == len(alpha_g)
    assert len(serials_g) == count_dict['total_g']
    assert len(serials_h) == len(alpha_g)
    assert len(alpha_h) == count_dict['total_h']
    
    """Bayesian bootstrap simulation of households using
       dirichlet-Multinomial model"""
    N_h = 132598198 #target size is number of housing units for 2012.
    theta_h  = np.random.dirichlet(alpha_h) # Draw Multinomial probabilities
                                            # from prior.
    counts_h = np.random.multinomial(N_h, theta_h) # Draw N sample from
                                                   # Multinomial.
    counts_h = pd.DataFrame({'Count':counts_h}, index=serials_h) # Dataframe
                      # with housing serialno's as index of the count column.

    """Bayesian bootstrap simulation of group quarters using
       dirichlet-Multinomial model"""
    N_g = 8015581 #target size is group quarters population for 2012.
    theta_g = np.random.dirichlet(alpha_g) # Draw Multinomial probabilities
                                           # from prior.
    counts_g = np.random.multinomial(N_g, theta_g) # Draw N sample from
                                                   # Multinomial.
    counts_g = pd.DataFrame({'Count':counts_g}, index=serials_g) # Dataframe
               # with group quarters serialno's as index of the count column.
    counts = pd.concat([counts_h, counts_g])
    counts.to_csv(args.output)
    logging.info('Wrote output to {}. Finished'.format(args.output))

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--debug",action='store_true')
    parser.add_argument("--output",help="output file",default="rep_counts.csv")
    parser.add_argument("--maxstates",default=100,type=int,help="Maximum number of states to compute")
    parser.add_argument("persondir",help="directory for person ACS files")
    parser.add_argument("housingdir",help="directory for person ACS files")
    args = parser.parse_args()

    np.random.seed(1138) #To facilitate replication.
    main(args.persondir, args.housingdir)
