#!/usr/bin/python
#
# download the files from Census 
#

import numpy as np
import os
from multiprocessing import Pool
import time
import glob
from subprocess import call

def get_file(fname):
    #
    # Download the file if it isn't in the downloads directory
    # The unzip.
    # If the unzip fails, repeat
    #

    if os.path.exists(fname):
        print("{} ... already downloaded".format(fname))
        return                  # already got it.

    print("{} ... ".format(fname))
    url = config['DEFAULT']['url'] + "/" + fname
    print("{} {}".format(os.getpid(),url))
    if call(['wget','-q',url]):
        raise RuntimeError("Download {} failed".format(url))

    # Now unzip the file
    if call(['unzip','-o',fname]):
        print("Unzip {} failed. Deleting. Re-run download".format(fname))
        os.unlink(fname)
    os.unlink(glob.glob("ACS*_PUMS_README.pdf")[0])
                                                       


if __name__ == '__main__':
    from argparse import ArgumentParser,ArgumentDefaultsHelpFormatter
    from configparser import ConfigParser
    parser = ArgumentParser(description = "Download data from Census Bureau",
                            formatter_class = ArgumentDefaultsHelpFormatter)
    parser.add_argument("--debug",action='store_true')
    parser.add_argument("--config",help="config file")
    parser.add_argument("-j","--threads",type=int,default=1)
    args = parser.parse_args()
    config = ConfigParser()
    config.read(args.config)

    np.random.seed(config.getint('DEFAULT','seed'))
    
    # Make a list of every file to download

    os.chdir(config['DEFAULT']['download_dir']) 

    fnames = []
    for hp in ['h','p']:
        for state in config['DEFAULT']['states'].split(" "):
            fnames.append(config['DEFAULT']['fname'].replace('^HP',hp).replace('^STATE',state))
    with Pool(args.threads) as p:
        p.map(get_file,fnames)

        
    
