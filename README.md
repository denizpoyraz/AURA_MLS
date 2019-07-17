# AURA_MLS

ReadMLS: read the MLS file format and write it into a csv file
Skim_MLSData: the second code of the MLS analysis, make an dataframe of MLS that matches with the Uccle dates.
The closest data in distance is selected, no selection applied for time period (noon or night). Therefore for each matched date 
there are two data one for the noon time and the other for night time.
ReadUccleData: write the interpolated Uccle data to a df that matches with MLS and also the ADif and RDif data

Plot_Dif_PerYear/Season: make the final MLS-Uccle plots per season or year
