# EPRResources
A collection of resources, both papers and websites, that I've found useful when working with UK electronic patient records (EPR). 

<details>
<summary><b>Data Source Descriptions</b></summary>
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
Each episode of care contains some demographic information about the patient, admission, discharge, procedures if performed, and diagnostic factor(s) contributing to the episode. The demographic information contained within each row is limited to ethnicity, age, and \acrshort{simd} decile and quintile. Admission information covers admission date (\texttt{ADMDATE}), admission type (i.e., emergency, urgent, or routine in \texttt{ADMTYPE}), where the patient was admitted or transferred from (\texttt{ADMTRANS}), what specialty the patient was treated by (\texttt{SPEC}), and what hospital the patient was admitted to (\texttt{HOSP}). Discharge information covers discharge date (\texttt{DISDATE}), discharge type (e.g., regular discharge, death, or transfer in \texttt{DISTYPE}), and where the patient was discharged or transferred to (\texttt{DISTRANS}). 
Each record must have the first diagnostic position (\texttt{DIAG1}) populated, which defines the primary diagnosis or main problem treated within the episode of care, and may have up to five additional positions populated with diagnosis information classified using \acrshort{icd10} codes (see Section \ref{sec:icd10}). Data quality assurance assessments have suggested coding accuracy levels $\geq$88\% using the first 4 digits of the \acrshort{icd10} code for \texttt{DIAG1}, but accuracy declines for \texttt{DIAG2} \hyp{} \texttt{DIAG6}, including under\hyp{}reporting of common conditions such as \acrshort{hf} and \acrshort{af/afl} \citep{PHS2019, Khand2005, DataAccuractySMR012019}. However, coding may be more accurate for some conditions which have a large objective component to diagnosis (e.g., cancer, \acrshort{mi}), but much less accurate for those which have a large subjective component (e.g., \acrshort{hf}), or where the problem is not considered a primary problem (e.g., AF \citep{Khand2005}.
\end{sloppy}

Additionally, each record has space for up to four procedures (\texttt{OPxA} [where \texttt{x} is the procedure number 1 \hyp{} 4]) with the potential for additional information (e.g., laterality, aborted, or unsuccessful are coded in \texttt{OPxB} [where \texttt{x} is the procedure number 1 \hyp{} 4]) codes recorded using \acrfull{opcs} (see Section \ref{sec:opcs}). Where applicable, the procedure coded in \texttt{OP1A} is considered the primary or main procedure for that episode of care. As with diagnostic codes, duality assurance assessments have shown coding accuracy levels $\geq$94\% using the first four digits of the \acrshort{opcs} code, with $\geq$97\% of hospitals reporting codes \citep{PHS2019}. 

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
  
  <summary>Prescribing Information System (PIS)</summary>
  [!NOTE] testing note
  </details>
</details>


</details>

<details>
<summary>Data classification </summary>
<details>
<summary>International Classification of Diseases, 10th revision</summary>


</details>
<details>
<summary>Office of Population Censuses and Surveys Classification of Interventions and Procedures, version 4(OPCS-4)</summary>
</details>
<details>
<summary>Read Codes</summary>
</details>
<details>
<summary>British National Formulary (BNF)</summary>
The first nine characters of the BNF code specify the chemical level of the medication. Within these nine characters, the first two characters indicate the chapter of the BNF that the medication is from. For example, drugs in BNF Chapter 2 (Cardiovascular System) will always begin with `02'. The code is then further subdivided into sections (e.g., Diuretics, contained within Chapter 2 Section 2 of the BNF, all begin with `0202'). The remaining six characters provide more detailed information about the medication, including whether the product is branded or generic, its strength, and formulation (see Figure \ref{fig:bnfCode} for a breakdown of a 9-character BNF code).
</details>
</details>  

