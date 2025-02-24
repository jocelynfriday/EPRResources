#The following includes code that I found helpful when needing to subset and label medication classes of interest within the Prescribing Information System (PIS)

## Subsetting and labelling medications
""" The following was originally developed for SQL Server and then adapted to Python. """
import csv
import pandas as pd
import numpy as np
import sqlite3

#### Step 1: Read in the lookup table specifying the medications.  These are prepared by: 
""" a) Preparing British National Formulary (BNF) code lists using OpenCodeLists (https://www.opencodelists.org/), 
    b) Downloading the definition 
    c) Edit the definition file as a text file to add ',classification' where classification is the medication class (e.g., thiazides or loop diuretics) 
    d) Do this for each medication class of interest (note, BNF codes may well be named more than once; this is fine and expected) 
    e) Create one master lookup table by appending these definitions, one after the other.  Only keep one header row, which should look like the following:
        'code,term,is_included,classification'
lookuptbl = pd.read_csv('file path.csv', encoding = 'latin1', sep = ',')

#### Step 2: Split the lookup table into codes used to define medications to be included (lookupTblInc) and those that will be excluded (lookupTblExc). 
lookupTblInc = lookuptbl[lookuptbl['is_included'] == '+']
lookupTblExc = lookuptbl[lookuptbl['is_included'] == '-']

#### Step 3: Only import the columns that you want to routinely look at specified in usecols
""" Note: RowID is a custom column that I ask for/add, which generates a unique row ID per dataset and helps with cleaning and tracking down any issues that may appear down the line """
pis = pd.read_csv('file path.csv', encoding = 'latin1', \
usecols = ['SafeHavenID', 'PRESC_DATE', 'DISP_DATE', 'PI_BNF_Item_Code', 'PI_BNF_Item_Description',
'Dispensed_Quantity', 'RowID']) 

#### Step 4: Convert to more accurate data types to improve efficiency and save space
pis['PRESC_DATE'] = pd.to_datetime(pis['PRESC_DATE'])
pis['DISP_DATE'] = pd.to_datetime(pis['DISP_DATE'])
pis[['PI_BNF_ITEM_description']] = pis[['PI_BNF_ITEM_description']].astype('category')
pis[['Dispensed_Quantity']] = pis[[Dispensed_Quantity']].astype('category')
""" depending on if the number of SafeHavenIDs and RowIDs can be represented using float32, convert these columns to float32 """
pis[pis.seleect_dtypes(np.float64).columns] = pis.select_dtypes(np.float64).astype(np.float)

#### Step 5: Remove duplicate records, defined as records which have the same SafehavenID, PRESC_DATE, DISP_DATE, PI_BNF_Item_Code, PI_BNF_Item_Description, and Dispensed_Quantity 
""" Could modify the original DataFrame in place by adding inplace=True """
droppedPis = pis.drop_duplicates(subset = ['SafeHavenID', 'PRESC_DATE', 'DISP_DATE', 'PI_BNF_Item_Code', 'PI_BNF_Item_Description', 'Dispensed_Quantity'])

#### Step 6: Create a SQL connection and add droppedPis and the lookup tables as separate tables
connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

""" Depending on the size of your droppedPis, use the following function to chunk it up and add it to the SQL table. 
    Note: the chunk size in this example divided the number of rows evenly to be safe """
def chunker(seq, size):
  for pos in range(0, len(seq), size):
    yield seq.iloc[pos:pos+size]

chunk_size = 2320
for i in chunker(droppedPis, chunk_size):
  i.to_sql('PIS', con = connection, schema = None, if_exists ='append')

lookupTblInc.to_sql(name = 'included', con = connection)
lookupTblExc.to_sql(name = "excluded', con = connection)

#### Step 7: Create a table to hold the initial inner join of PIS and included
sql = """ CREATE TABLE medicationAll as 
          SELECT p.SafeHavenID as SafeHavenID, p.PRESC_DATE as PRESC_DATE, p.DISP_DATE as DISP_DATE, 
          i.classification as classification, p.PI_BNF_Item_Code as PI_BNF_Item_Code, 
          p.PI_BNF_Item_Description as PI_BNF_Item_Description, p.Dispensed_Quantity, p.RowID as RowID
          FROM PIS p INNER JOIN included i on substr(p.PI_BNF_Item_Code, 0, length(i.code)+1) = i.code"""

cursor.execute(sql)

#### Step 8: Create a table to hold all medications after removing the excluded based on BNF code and classification
sql = """ CREATE TABLE medication as 
          SELECT p.SafeHavenID as SafeHavenID, p.PRESC_DATE as PRESC_DATE, p.DISP_DATE as DISP_DATE, 
          p.classification as classification, p.PI_BNF_Item_Code as PI_BNF_Item_Code, 
          p.PI_BNF_Item_Description as PI_BNF_Item_Description, p.Dispensed_Quantity, p.RowID as RowID
          FROM medicationAll p WHERE NOT EXISTS 
            (SELECT 1 FROM excluded ex WHERE 
              substr(p.PI_BNF_Item_Code, 0, length(ex.code)+1) = ex.code AND ex.classification = p.classification"""
cursor.execute(sql)
connection.commit()

#### Step 9: Save labelled and subset PIS records to a CSV
cursor.execute("SELECT * FROM medication")

with open('out file path.csv', 'w', newline = '') as out_csv_file:
  csv_out = csv.writer(out_csv_file)
  csv_out.writerow(d[0] for d in cursor.description])
  for row in cursor:
    csv_out.writerow(row)

connection.commit()

#### Step 9: Clean up
connection.close()





