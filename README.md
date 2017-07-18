# Synthetic population housing and person records for the United States

Constructs a population that is meant to be representative of the 2012 US population using Census ACS 5-year PUMS.

- Author: William Sexton

## Modification Log:
- William Sexton - Created, March 2017
- Simson Garfinkel - Added automation, July 2017


# Project Design

## Inputs
The synthetic population was generated from the 2010-2014 ACS PUMS housing and person files, released in 2015. 

Citation:

    United States Department of Commerce. Bureau of the Census. (2017-03-06).
    American Community Survey 2010-2014 ACS 5-Year PUMS File [Data set].
    Ann Arbor, MI: Inter-university Consortium of Political and Social
    Research [distributor]. http://doi.org/10.3886/E100486V1

Direct Download: https://www2.census.gov/programs-surveys/acs/data/pums/2015/5-Year

However, the data that we have was built from copies of the data obtained from ICPSR/OpenICPSR
 * Persistent URL:      http://doi.org/10.3886/E100486V1
 * See also Data Lumos: http://doi.org/10.3886/E100521V1

 * https://www.openicpsr.org/datalumos/project/100521/version/V1/view;jsessionid=E4FA2D6C9A6003487790F2127C15B3DB

### Reference for this work:
Synthetic population housing and person records for the United States
Principal Investigator(s):  William Sexton, Cornell University; 
                            John M. Abowd, Cornell University; 
                            Ian M. Schmutte, University of Georgia; 
                            Lars Vilhuber, Cornell University
Version: V1
 * https://www.openicpsr.org/openicpsr/project/100274/version/V1/view?path=/openicpsr/100274/fcr:versions/V1/data


## Outputs
There are 17 housing files
- repHus0.csv, repHus1.csv, ... repHus16.csv
and 32 person files
- rep_recode_ACSpus0.csv, rep_recode_ACSpus1.csv, ... rep_recode_ACSpus31.csv.

Files are split to be roughly equal in size. The files contain data for the entire country. Files are not split along any demographic characteristic. The person files and housing files must be concatenated to form a complete person file and a complete housing file, respectively.

If desired, person and housing records should be merged on 'id'. Variable description is below.

See [README2.md](README2.md) for data dictionary and information on additional variables. 

# Project Status:

## Testing
Stress testing to determine whether these data can actually reproduce accurate statistics for 2012 is still underway.

# Acknowledgements 
## Funding support
This work is supported under  Grant G-2015-13903 from the Alfred P. Sloan Foundation on "[The Economics of Socially-Efficient Privacy and Confidentiality Management for Statistical Agencies](https://www.ilr.cornell.edu/labor-dynamics-institute/research/project-19)" (PI: John M. Abowd)

