# SDoH-Copy-
CB_Data: (Imports pandas and censusdata)
Creates and populates a table with data from the Census Bureau’s American Community Survey. The following are the variables that define the table:
State number (from the ACS).
Level of granularity, i.e., country or census tract.
Measures to be pulled from the ACS with the corresponding codes, i.e. poverty percentage : DP03-0119PE.
The table created will have rows corresponding to the geographic location at the level of granularity selected.

DB_Upload: (Imports pandas and sqlalchemy )
Connects and uploads data table to given database, with the following variables:
Name for the table to be created or rewritten in the database.
Data table to be uploaded.

Pull_Main:
Is a demo of the how CB_Data and DB_Upload work.

In collaboration and under the supervision of Mr. Trip Humphrey and Dr. Omid Shabestari.
