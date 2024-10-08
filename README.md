# EPRResources
A collection of resources, both papers and websites, that I've found useful when working with UK electronic patient records (EPR). 

<details>
<summary><b>Data Source Descriptions</b></summary>
  <details>
<summary><b><i>Demographics</i></b></summary>
    Scotland has a long history of electronic patient records (EPR) captured from birth through death using individual Community Health Index (CHI) numbers. CHI numbers allow for the unique identification and tracking of patients across NHS Scotland's services \citep{NHSDigChi2022}. The CHI number is the Scottish equivalent to England and Wales's NHS number. CHI numbers are assigned to each patient upon first registration with the system \citep{NHSChind}. CHI numbers are ten digits long, with the first six digits taken from the date of birth in two-digit format (<tt>DDMMYY</tt>), two random digits, a sex-based digit (i.e., even for women and odd for men), and an arithmetical check digit \citep{NHSDigChi2022}. 
    <br></br>
    The demographics data are collated from a collection of sources based on CHI numbers. The data made available within the dataset are acquired largely from NRS and records available to the NHS Safe Haven team. Demographic data include obfuscated date of birth (DOB), sex, and Scottish Index of Multiple Deprivation (SIMD).
    <br></br>
    <b>Date of Birth</b>
    The NHS Safe Haven team obfuscated the canonical DOB. In the <tt>YYYY-MM-DD</tt> date format, DOBs are uniformly obfuscated by setting the day part of the date to be the middle of the month while maintaining the month and year values. For example, a birthday of 1922-01-09 would be changed to 1922-01-15.
    <br></br>
    <b>Scottish Index of Multiple Deprivation (SIMD)</b>
    Scottish Index of Multiple Deprivation (SIMD) is an area-based measurement of socioeconomic deprivation assigned to residents of Scotland based on where they live. Scottish residents' SIMD 2012 status was calculated by the Scottish Government using thirty-one indicators from seven different aspects of deprivation: income, employment, health, education, housing, geographic access, and crime. The indicators are combined using a weighted sum to create a single index, providing a relative ranking for each small geographic area in Scotland. Areas average about 800 individuals \citep{Executive2012}. It is important to note that SIMD can only measure an area’s level of deprivation, not an individual’s level. The absence of deprivation should not necessarily be correlated with affluence. The terms most deprived or least deprived were used to refer to the areas and not to the individuals living in those areas \citep{Executive2012}. Other year's indexes are also available. 
    <br></br>
    <b>Sex</b> The Demographics \texttt{sex} field was taken as the authoritative version for an individual's sex. 
  </details>
    <details>
<summary><b><i>Deaths</i></b></summary>
      The deaths file is a Tier 1 dataset containing combined records of death from the General Register Office, sourcing data primarily from National Records Scotland deaths, though others can be used. Each record contains information including date of death (DOD), location of death, the underlying cause of death (COD), and space for up to 10 contributing <tt>COD</tt>. Since 1 January 2000, CODs are coded in accordance with the International Classification of Disease, 10th revision (ICD-10) \citep{NRS_DeathsBackground} (see [Section ICD-10](#sec-icd10) for an explanation of ICD-10).
    </details>
<details>
<summary><b><i>Scottish Morbidity Records (SMR)</i></b></summary>
Scottish Morbidity Records are Tier 1 datasets, meaning data are collated at a national level and contain information from everyday care. These datasets contain individual-level healthcare data for patients treated within Scotland. The type of record denotes the general type of healthcare received and/or the patient's medical status.
<br/><br/>
<details>
<summary>SMR00</summary>
  [!NOTE] Recommended to avoid using diagnostic or procedural information from SMR00
  SMR00 contains information on outpatient appointments, attendance, and procedures performed. A record is generated when a patient either has outpatient clinical interaction or where the \allowbreak patient meets with a healthcare provider responsible for care outwith an outpatient clinic session \citep{SMR00nd}. The value of \acrshort{smr00} lies in being able to track patient contact with a specialist. Unfortunately, this rarely includes information on diagnosis or procedures.
</details>
<details>
<summary>SMR01</summary>
SMR01 contains information regarding all general and acute inpatient and day cases from all NHS hospitals in Scotland. Each row of data corresponds to an episode of care. Patients receive a new episode of care each time they change specialty, significant facility[^1], or consultant for medical reasons.
  
[^1]: A division of medicine or density covering a specific area of clinical activity and identified within one of the Royal Colleges or Faculties

Each episode of care contains some demographic information about the patient, admission, discharge, procedures if performed, and diagnostic factor(s) contributing to the episode. The demographic information contained within each row is limited to ethnicity, age, and Scottish Index of Multiple Deprivation (SIMD) decile and quintile. Admission information covers admission date (<tt>ADMDATE</tt>), admission type (i.e., emergency, urgent, or routine in <tt>ADMTYPE</tt>), where the patient was admitted or transferred from (<tt>ADMTRANS</tt>), what specialty the patient was treated by (<tt>SPEC</tt>), and what hospital the patient was admitted to (<tt>HOSP</tt>). Discharge information covers discharge date (<tt>DISDATE</tt>), discharge type (e.g., regular discharge, death, or transfer in <tt>DISTYPE</tt>), and where the patient was discharged or transferred to (<tt>DISTRANS</tt>). 
Each record must have the first diagnostic position (<tt>DIAG1</tt>) populated, which defines the primary diagnosis or main problem treated within the episode of care, and may have up to five additional positions populated with diagnosis information classified using ICD-10 codes (see [Section ICD-10](#sec-icd10)). Data quality assurance assessments have suggested coding accuracy levels $\geq$88\% using the first 4 digits of the ICD-10 code for <tt>DIAG1</tt>, but accuracy declines for <tt>DIAG2</tt> - <tt>DIAG6</tt>, including under-reporting of common conditions such as heart failure and atrial fibrillation/flutter \citep{PHS2019, Khand2005, DataAccuractySMR012019}. However, coding may be more accurate for some conditions which have a large objective component to diagnosis (e.g., cancer, myocardial infarction), but much less accurate for those which have a large subjective component (e.g., heart failure), or where the problem is not considered a primary problem (e.g., atrial fibrillation \citep{Khand2005}.


Additionally, each record has space for up to four procedures (<tt>OPxA</tt> [where <tt>x</tt> is the procedure number 1 - 4]) with the potential for additional information (e.g., laterality, aborted, or unsuccessful are coded in <tt>OPxB</tt> [where <tt>x</tt> is the procedure number 1 - 4]) codes recorded using \acrfull{opcs} (see Section \ref{sec:opcs}). Where applicable, the procedure coded in <tt>OP1A</tt> is considered the primary or main procedure for that episode of care. As with diagnostic codes, duality assurance assessments have shown coding accuracy levels $\geq$94\% using the first four digits of the \acrshort{opcs} code, with $\geq$97\% of hospitals reporting codes \citep{PHS2019}. 

Useful links:
* SMR01 crib sheet:https://publichealthscotland.scot/media/24925/smr01_crib_270323.pdf
* Explanation of data collection and validation: https://www.publichealthscotland.scot/publications/acute-hospital-activity-and-nhs-beds-information-quarterly/acute-hospital-activity-and-nhs-beds-information-quarterly-quarter-ending-31-december-2019/data-quality/
</details>
<br/><br/>
<details>
<summary>SMR04</summary>
  Useful links:
  SMR04 crib sheet: https://publichealthscotland.scot/media/24927/smr04_crib_270323.pdf
</details>
<br/><br/>
<details>
<summary>SMR06</summary>
</details>
</details>
  <details>
  
  <summary><b><i>Prescribing Information System (PIS)</i></b></summary>
  [!NOTE] testing note
    <p>
  <img src="references/Total_presc_date.png", width=400 alt> 
  <img src="references/Total_disp_date.png", width=400 alt> 
      
<em>Spread of recorded prescription days (<tt>PRESC_DATE</tt>) across the month versus spread of recorded dispensing days (<tt>DISP_DATE</tt>), a reimbursement artefact.</em>
</p>
  </details>
</details>


</details>

<details>
<summary><b>Data classification</b></summary>
<details>
<summary><b><i>International Classification of Diseases, 10th revision</i></b></summary><a name="sec-icd10"></a>

</details>
<details>
<summary><b><i>Office of Population Censuses and Surveys Classification of Interventions and Procedures, version 4(OPCS-4)</i></b></summary><a name="sec-opcs"></a>
</details>
<details>
<summary><b><i>Read Codes</i></b></summary>
</details>
<details>
<summary><b><i>British National Formulary (BNF)</i></b></summary>
The first nine characters of the BNF code specify the chemical level of the medication. Within these nine characters, the first two characters indicate the chapter of the BNF that the medication is from. For example, drugs in BNF Chapter 2 (Cardiovascular System) will always begin with `02'. The code is then further subdivided into sections (e.g., Diuretics, contained within Chapter 2 Section 2 of the BNF, all begin with `0202'). The remaining six characters provide more detailed information about the medication, including whether the product is branded or generic, its strength, and its formulation (see below for a breakdown of a 9-character BNF code).
  <p>
  <img src="references/BNF Code_v2.png", width=400 alt>
  
  <em>A breakdown of the BNF code for a generic 40 mg tablet of furosemide. `AA` in the `Product` section always indicates that the medication is a generic version. The asterisk indicates that any code could be entered in this section.</em>
</p>
</details>
</details>  

