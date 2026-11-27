# BIT 4131 Statistical Computing and Reporting

This project covers the 23 topics listed in the assignment brief. It includes Python and R examples, a report, a synthetic dataset, and charts.

## Files

- `REPORT.md` explains the methods and gives the Python results.
- `src/analysis.py` runs the Python examples.
- `src/analysis.R` contains the R examples.
- `data/` contains the generated dataset.
- `results/` contains the result tables.
- `figures/` contains the charts.
- `PRESENTATION_OUTLINE.md` has a suggested presentation order.

## Run the Python examples

Install Python 3.10 or later, then run these commands from this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src/analysis.py
```

To run the R examples, open this folder in a terminal with R installed and run:

```sh
Rscript src/analysis.R
```

## About the data

I did not use real student records. The scripts make 1,200 rows for practice. They include an A/B/C category, a treatment label, age, study hours, attendance, scores, and pass status. Study hours and attendance each have 8% missing values so I can show how missing data are handled.

The results describe only the made-up data. They should not be used to make claims about real students or teaching methods. If I receive real data, I should replace this dataset and rerun the analysis.
