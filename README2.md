## Data Dictionary
See [2010-2014 ACS PUMS data dictionary](http://doi.org/10.3886/E100486V1). All variables from the ACS PUMS housing files are present in the synthetic housing files and all variables from the ACS PUMS person files are present in the synthetic person files. Variables have not been modified in any way. Theoretically, variables like `person weight` no longer have any use in the synthetic population.

## Additional variables.
- `id`: Both the synthetic housing and person files include this variable. It is meant as an extension/recode of the existing `serialno` variable.  Each housing/group quarters unit in the synthetic population gets a unique `id` and each person in the synthetic population gets linked to exactly one housing/group quarter unit by `id`.
`id` takes values from 0 to 140613778.

- Race recode in person files. Variable names are straightforward but somewhat cumbersome. They are composed of `tokens` as follows:

  - WHT - white
  - BLK - black or African American
  - AIAN - American indian or Alaskan native
  - ASN - Asian
  - NHPI - native Hawaiian or pacific islander
  - SOR - some other race

**** There are 63 race recode variables. Each take on 0/1 values. No further description beyond name is required ****

- isWHT
- isBLK
- isAIAN
- isASN
- isNHPI
- isSOR
- isWHTandBLK
- isWHTandAIAN
- isWHTandASN
- isWHTandNHPI
- isWHTandSOR
- isBLKandAIAN
- isBLKandASN
- isBLKandNHPI
- isBLKandSOR
- isAIANandASN
- isAIANandNHPI
- isAIANandSOR
- isASNandNHPI
- isASNandSOR
- isNHPIandSOR
- isWHTandBLKandAIAN
- isWHTandBLKandASN
- isWHTandBLKandNHPI
- isWHTandBLKandSOR
- isWHTandAIANandASN
- isWHTandAIANandNHPI
- isWHTandAIANandSOR
- isWHTandASNandNHPI
- isWHTandASNandSOR
- isWHTandNHPIandSOR
- isBLKandAIANandASN
- isBLKandAIANandNHPI
- isBLKandAIANandSOR
- isBLKandASNandNHPI
- isBLKandASNandSOR
- isBLKandNHPIandSOR
- isAIANandASNandNHPI
- isAIANandASNandSOR
- isAIANandNHPIandSOR
- isASNandNHPIandSOR
- isWHTandBLKandAIANandASN
- isWHTandBLKandAIANandNHPI
- isWHTandBLKandAIANandSOR
- isWHTandBLKandASNandNHPI
- isWHTandBLKandASNandSOR
- isWHTandBLKandNHPIandSOR
- isWHTandAIANandASNandNHPI
- isWHTandAIANandASNandSOR
- isWHTandAIANandNHPIandSOR
- isWHTandASNandNHPIandSOR
- isBLKandAIANandASNandNHPI
- isBLKandAIANandASNandSOR
- isBLKandAIANandNHPIandSOR
- isBLKandASNandNHPIandSOR
- isAIANandASNandNHPIandSOR
- isWHTandBLKandAIANandASNandNHPI
- isWHTandBLKandAIANandASNandSOR
- isWHTandBLKandAIANandNHPIandSOR
- isWHTandBLKandASNandNHPIandSOR
- isWHTandAIANandASNandNHPIandSOR
- isBLKandAIANandASNandNHPIandSOR
- isWHTandBLKandAIANandASNandNHPIandSOR

