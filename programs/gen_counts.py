#!/usr/bin/env python2.7 
# gen_counts.py
# William Sexton
# Last Modified: 3/30/2017

#inputs: argv[1] - raw ACS person files (in a directory?)
#        argv[2] - raw ACS housing files (in a directory)

#imports
import pandas as pd
import numpy as np
import sys
import csv
import glob
import os.path
import logging
from firstpass import process_housing_chunk
from firstpass import process_person_chunk
import acs

def set_alpha_h(df, count_dict, yearCode, alpha_h):
    """df is a pandas dataframe containing a chunk of data from the raw ACS housing data
    count_dict, yearCode,defined elsewhere in code for bookkeeping purposes
    alpha_h stores prior probabilities for Dirichlet distribution over records of housing data"""
    df=df[df["TYPE"]==1] #Filter out group quarters.
    if df.empty:
        return alpha_h #ie do nothing if chunk contains no housing units.
    df["ADJINC"]=df["ADJINC"].map(yearCode) #convert ADJINC to year.
    #convert year to count_dict key for housing units
    df["ADJINC"]=df["ADJINC"].map({2010:"n2010h",2011:"n2011h",2012:"n2012h",2013:"n2013h",2014:"n2014h"})
    df["ADJINC"]=df["ADJINC"].map(count_dict) #convert year key to count
        
    alpha_h.extend((df["WGTP"]*df["ADJINC"]/count_dict["weight_h"]).tolist())
    return alpha_h

def set_alpha_g(df, count_dict, yearCode, alpha_g):
    """df is a pandas dataframe containing a chunk of data from the raw ACS person data
    count_dict, yearCode,defined elsewhere in code for bookkeeping purposes
    alpha_g stores prior probabilities for Dirichlet distribution over records of group quarters data"""
    df=df[(df["RELP"]==16) | (df["RELP"]==17)] #Filter to only include group quarters records. See data dictionary for RELP description.
    if df.empty:
        return alpha_g #ie do nothing if chunk contains no group quarters records.
    df["ADJINC"]=df["ADJINC"].map(yearCode) #convert ADJINC to year
    #convert year to count_dict key for group quarters
    df["ADJINC"]=df["ADJINC"].map({2010:"n2010g",2011:"n2011g",2012:"n2012g",2013:"n2013g",2014:"n2014g"})
    df["ADJINC"]=df["ADJINC"].map(count_dict) #convert year to count
        
    alpha_g.extend((df["PWGTP"]*df["ADJINC"]/count_dict["weight_g"]).tolist())
    return alpha_g






def main(persondir,housingdir):
    """Builds synthetic population using Bayesian bootstrapping process on ACS housing records and then populating
    each housing unit/group quarters unit with person records from the ACS person data files"""     
    
    """Configure log"""
    #Change filename with each run (if desired) otherwise info will append to same log.
    logging_level = logging.DEBUG if args.debug else logging.INFO

    logging.basicConfig(filename='gen_counts.log',format='%(asctime)s %(message)s', level=logging_level)
    logging.info('Started')
    
    
    # Get the files form the provided directories
    # Notes that glob.glob() filenames are sorted. Strictly there is no reason to do this, but it makes debugging easier.
    filenames_person = sorted( glob.glob(os.path.join(persondir,"*.csv"))) #list of four person files
    logging.debug("filenames_person: {}".format(filenames_person))
    
    filenames_housing = sorted( glob.glob(os.path.join(housingdir,"*.csv"))) #list of four housing files
    logging.debug("filenames_housing: {}".format(filenames_housing))
    
    """Bookkeeping"""
    yearCode={1094136:2010,1071861:2011,1041654:2012,1024037:2013,1008425:2014} #See data dictionary for ADJINC
    
    count_dict={"total_h":0, "n2010h":0, "n2011h":0, "n2012h":0, "n2013h":0, "n2014h":0, "weight_h":0, #n%yr%h is number of observed housing records in yr 
                "total_g":0, "n2010g":0, "n2011g":0, "n2012g":0, "n2013g":0, "n2014g":0,"weight_g":0} #n%yr%g is number of observed group quarters in yr
    
        
    """First pass of housing files to collect aggregate counts and store serial numbers of households"""
    #Files processed in chunks to reduce memory footprint.
    #This approach requires multiple read ins of the data to complete the Bayesian bootstrapping
    #but it works. If there is a better way of doing this, I'd love to see it.

    serials_h=[]
    for f in filenames_housing:
        logging.info("reading housing "+f)
        for chunk in pd.read_csv(f,usecols=[acs.SERIALNO,"ADJINC","TYPE","WGTP"],chunksize=100000): #Restrict to necessary columns
            count_dict,serials_h=process_housing_chunk(chunk,count_dict,yearCode,serials_h)
            
    """First pass at person files to collect aggregate counts and store serial numbers of group quarters records"""
    serials_g=[]
    for f in filenames_person:
        logging.info("reading persons "+f)
        for chunk in pd.read_csv(f,usecols=[acs.SERIALNO,"ADJINC","PWGTP","RELP"],chunksize=100000): #Restrict to necessary columns
            count_dict,serials_g=process_person_chunk(chunk,count_dict,yearCode,serials_g)
            
    """Next pass at housing is to define the prior parameter alpha for the dirichlet distribution over households."""
    alpha_h=[]
    for f in filenames_housing:
        for chunk in pd.read_csv(f,usecols=[acs.SERIALNO,"ADJINC","TYPE","WGTP"],chunksize=100000):
            alpha_h=set_alpha_h(chunk,count_dict,yearCode,alpha_h)
    """Next pass at person is to define the prior parameter alpha for the dirichlet distribution over group quarters."""
    alpha_g=[]
    for f in filenames_person:
        for chunk in pd.read_csv(f,usecols=[acs.SERIALNO,"ADJINC","RELP","PWGTP"],chunksize=100000):
            alpha_g=set_alpha_g(chunk,count_dict,yearCode,alpha_g)
    
    logging.debug(len(alpha_g)==count_dict['total_g']) #sanity checks
    logging.debug(len(alpha_h)==count_dict['total_h'])
    
    
    
    """Bayesian bootstrap simulation of households using dirichlet-Multinomial model"""
    N_h=132598198 #target size is number of housing units for 2012.
    theta_h=np.random.dirichlet(alpha_h) #Draw Multinomial probabilities from prior.
    counts_h=np.random.multinomial(N_h,theta_h) #Draw N sample from Multinomial.
    counts_h=pd.DataFrame({'Count':counts_h},index=serials_h) #Dataframe with housing serialno's as index of the count column

    """Bayesian bootstrap simulation of group quarters using dirichlet-Multinomial model"""
    N_g=8015581 #target size is group quarters population for 2012.
    theta_g=np.random.dirichlet(alpha_g) #Draw Multinomial probabilities from prior.
    counts_g=np.random.multinomial(N_g,theta_g) #Draw N sample from Multinomial.
    counts_g=pd.DataFrame({'Count':counts_g},index=serials_g) #Dataframe with group quarters serialno's as index of the count column
    
    counts=pd.concat([counts_h,counts_g])
    counts.to_csv(args.output)
    logging.info('Finished')
    

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--debug",action='store_true')
    parser.add_argument("--output",help="output file",default="rep_counts.csv")
    parser.add_argument("persondir",help="directory for person ACS files")
    parser.add_argument("housingdir",help="directory for person ACS files")
    args = parser.parse_args()

    np.random.seed(1138) #To facilitate replication.
    main(args.persondir,args.housingdir)
    
