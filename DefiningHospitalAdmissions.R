# The following includes code that I've found helpful when needing to define a continuous hospital admission within 
# Scottish Morbidity Records for general/acute inpatient and day cases (SMR01) or mental health inpatient and day cases (SMR04).
# This is done as admission and discharge events do not include time information, so transfers with a discharge before midnight 
# and the associated admission after midnight will have non-overlapping dates. 

# !NOTE! Ensure all admission (ADMDATE) and discharge (DISDATE) dates are populated and not null. 

##Identifying nested episodes of care within a continuous admission and assigning a unique hospitalStayID per admission

### Step 1: Load libraries and set up the environment
library(tidyverse)
library(data.table)

smr01All <- fread("SMR01.csv")

#### Step 1a: If the SMR01 data does not have a unique row ID, add one
smr01All[, row_id := .I]

### Step 2: Update data types & subset to necessary columns
smr01All$SafeHavenID <- as.factor(smr01All$SafeHavenID)
smr01All$ADMDATE <- as.Date(smr01All$ADMDATE)
smr01All$DISDATE <- as.Date(smr01All$DISDATE)

##### Subset away to only pertinent information 
smr01 <- smr01All[, c("SafeHavenID", "ADMDATE", "DISDATE", "row_id")]

###Step 3: Order smr01 by SafeHavenID, admission date (ADMDATE), and discharge date (DISDATE) in ascending order
setorder(smr01, SafeHavenID, ADMDATE, DISDATE)

### Step 4: Create a flag to indicate the start of a new admission series. 
#### 1 indicates the start of a new admission series, while 0 indicates a continuation of the admission
smr01[, series := 1]

### Step 5: Identify row_ids of nested episodes of care
rows_to_flag <- smr01[, {
  # Define variables
  flagged <- integer(0)
  ## Most recent, maximum, discharge date seen so far set to the first by default
  max_disdate <- DISDATE[1]
  
  # If a SafeHavenID has more than 1 episode of care, enter the if statement
  if (.N > 1){
    
    # For all episodes of care:
    for (i in 2L:.N){
      # If the current admission date (ADMDATE) is within 1 day of the maximum discharge date (max_disdate), store the row_id with 0
      if(!is.na(ADMDATE[i]) && ! is.na(max_disdate) && as.numeric(ADMDATE[i] -max_disdate) <= 1){
        flagged <- c(flagged, row_id[i])
      }
      # Also, if the current discharge date (DISDATE) is greater than the maximum seen discharge date (max_disdate), update max_disdate
      if(!is.na(DISDATE[i]) && DISDATE[i] > max_disdate) {
        max_disdate <- DISDATE[i]
      }
    }
    
  }
  .(row_id = flagged)
}, by = SafeHavenID]

### Step 6: Update series to 0 where the row_id was identified during Step 4
smr01[row_id %in% rows_to_flag$row_id, series := 0]

### Step 7: Create and assign a unique hospital_stay_id per continuous admission
#### Increment hospital_stay_id at every 1, and remain the same for every 0 in the series 
smr01[, hospital_stay_id := 0L]
smr01[, hospital_stay_id := cumsum(series == 1)]

### Step 8: Merge hospital_stay_id back onto smr01
smr01 <- smr01[,c("row_id", "hospital_stay_id")]
smr01All <- merge(smr01All, smr01, by= "row_id", all= TRUE)
