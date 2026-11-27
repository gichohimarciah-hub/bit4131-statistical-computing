# BIT 4131 Statistical Computing and Reporting

This project covers the 23 topics listed in the assignment brief. It includes Python and R examples, a report, a synthetic dataset, and charts.

## Files

- `REPORT.md` explains the methods and gives the Python results.
- `src/analysis.py` runs the Python examples.
- `src/analysis.R` contains the R examples.
- `requirements.txt` lists the Python packages used by the script.
- `data/` contains the generated dataset.
- `results/` contains the result tables.
- `figures/` contains the charts.

## Running the analyses

Install the Python packages listed in `requirements.txt`, then run the Python script from this folder first. It creates the shared dataset and monthly series. Run the R script from the same folder afterward so both scripts use the same data.

## About the data

I used synthetic data because no real student records were provided, and this lets me demonstrate the methods without exposing private information. The scripts make 1,200 rows for practice. They include an A/B/C category, a treatment label, age, study hours, attendance, scores, and pass status. Study hours and attendance each have 8% missing values so I can show how missing data are handled.

The results describe only the made-up data. They should not be used to make claims about real students or teaching methods. If I receive real data, I should replace this dataset and rerun the analysis.
