# Run DefiningHospitalAdmissions.R first 

# The following includes code that I've found helpful when needing to define a continuous hospital admission within 
# Scottish Morbidity Records for general/acute inpatient and day cases (SMR01) or mental health inpatient and day cases (SMR04). It identifies the first/reference episode 
# of care within a continuous admission based on the logic outlined in the 'Identifying First Record of Stay' subsection of 'General Tips' -> 'Deriving Useful Variables'.

## Identifying the reference/first episode of care (reference_admission) within a continuous admission and assigning a binary flag to this episode, and assigning zero otherwise

### Step 1: Run DefiningHospitalAdmissions.R and load data.table 
#### This outputs smr01_all, which includes an additional column, hospital_stay_id, that identifies all episodes of care associated with a single, continuous admission. 
library(data.table)

### Step 2: Order the data table based on admission date (ADMDATE), admission/transfer location (ADMTRANS), admission type (ADMTYPE), discharge/transfer location (DISTRANS), 
### discharge date (DISDATE), and admission reason (ADMREAS)
setorder(smr01_all, ADMDATE, ADMTRANS, -ADMTYPE, -DISTRANS, DISDATE, ADMREAS, na.last = FALSE)

### Step 3: Add a row number (rn) per hospital_stay_id
smr01_all[, rn := seq_len(.N), by = hospital_stay_id]

### Step 4: Set the reference admission (reference_admission) using the first row number per hospital_stay_id
smr01_all[, reference_admission := ifesle(rn == 1, 1, 0)]

### Step 5: Drop rn, as unnecessary, and save to CSV 
smr01_all[, rn := NULL]

fwrite(smr01_all, "SMR01_with_derivedVars.csv")


