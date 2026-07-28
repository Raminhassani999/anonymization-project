# Diabetology Synthetic Dataset

`diabetology-synthetic-dataset.xlsx` — a fully synthetic longitudinal dataset of
type-2 diabetes outpatient follow-up. It mirrors the structure of the real
working file so that ingestion, validation and analysis code can be developed and
tested without touching sensitive data.

## Contents

| Sheet | Rows | Columns | Grain |
|---|---|---|---|
| `DM` | 1337 | 103 | one row per patient visit |
| `missing Static - per patient` | 300 | 11 | one row per patient with missing static fields |
| `missing Dynamic - per visit` | 1337 | 12 | one row per visit with missing dynamic fields |

300 patients, 1–8 visits each, spanning 2018 onwards.

## Main sheet — `DM`

Column groups, in order:

- **Identity** (1–7): `patient` (progressive id, filled only on the patient's first
  visit), `Patient Code`, `Surname`, `First Name`, `Birth Date`, `Tax Code`,
  `Assessment Date`.
- **Anthropometrics & vitals** (8–16): `Sex`, `Age At Assessment`, `Height`,
  `Weight`, `BMI`, `Obesity`, blood pressure, `Hypertension`.
- **Diagnoses** (17–20): diabetes and renal-failure diagnosis years, `Dyslipidemia`,
  `Renal Failure`.
- **Laboratory** (21–47): haematology (`PLT`, `RBC`, `WBC`, differential, `Hb`,
  `MCV`), renal (`Urine Albumin`, `Creatinine`, `eGFR (CKD-EPI)`), metabolic
  (`Blood Glucose`, `HbA1c`, `Insulin (#71)`, `C-Peptide`), lipids, liver
  (`GOT/AST`, `GPT/ALT`, `GGT`) and the derived scores `FIB-4` and `NFS`.
- **Complications** (48–55): cardio-cerebro-vascular events and their date,
  `Doppler TSA`, ocular / renal / peripheral-vessel / neurological complications,
  `Diabetic Foot`.
- **Antihypertensive therapy** (56–69): diuretic classes, Ca antagonists,
  beta-blockers, `ACE Inhibitors`, `Sartans`, `Alpha-Blockers`, and others.
- **Antidiabetic therapy** (70–81): `Insulin (#129)`, `Metformin`, `GLP-1ra`,
  `DPP-4`, `SGLT2i`, `Pioglitazone`, each paired with its start year.
- **Lipid-lowering therapy** (82–87): `Omega 3`, `Ezetimibe`, `Statin`,
  `Statin Molecule`.
- **Other therapies** (88–103): `Antipsychotics`, `PPI`, `Antiplatelets`,
  `Anticoagulants`, osteoporosis, vitamin D, iron, folic acid, corticosteroids,
  potassium chelators.

## Conventions

- Column names are in English; person names are Italian.
- Binary flags are `1.0` / `0.0` floats; blank means not recorded.
- `Sex`: `1` = male, `2` = female.
- `Birth Date` is a `dd/mm/yy` string; `Assessment Date` is a `YYYY-MM-DD` string;
  `CSV Event Year` is a `YYYY-MM-DD 00:00:00` string. These mixed formats are
  intentional — they reproduce the real file and exercise date parsing.
- Static attributes (identity, therapy start years, diagnoses) are repeated
  unchanged on every visit row of a patient.
- `C-Peptide`, `TTS Patches` and `Treatment Type` are empty in every row, as in the
  source layout.
- Derived fields are internally consistent: `BMI` from height/weight, `Obesity`
  from `BMI >= 30`, `Age At Assessment` from birth and assessment dates.

## Missing-data sheets

Both sheets repeat the patient identity columns plus the fields under audit, and end
with a `Needs` column listing the missing items as comma-separated tokens.

- **Static, per patient** — tokens `DM_diag`, `Insulin_start`, `GLP1_start`,
  `SGLT2_start`.
- **Dynamic, per visit** — tokens `PS`, `PD`, `Ins71`, `Doppler` (systolic pressure,
  diastolic pressure, `Insulin (#71)`, `Doppler TSA`).

## Provenance and confidentiality

Every cell is randomly generated; no row-level value comes from the real dataset.

- Surnames and given names are drawn from lists of common Italian names and randomly
  recombined; they match no record in the source (verified: zero overlap on
  surname + first name + birth date).
- Tax codes are codice-fiscale-shaped but use an `X###` place code, which does not
  exist in the official Belfiore catalogue, so no generated value can be a valid
  real identifier. Patient codes use an `F` prefix. Both verified as disjoint from
  the source.
- Numeric ranges, missing-data rates and the statin vocabulary were calibrated on
  aggregate statistics of the source (min/max, null rates, category frequencies) so
  that downstream code behaves realistically. No individual record is recoverable
  from these aggregates.
- Unlike the real file, this dataset contains no data-entry outliers — all values
  fall within plausible clinical ranges.
