# BIT 4131 Statistical Computing and Reporting

This repository contains reproducible teaching examples for all 23 concepts shown in the group-work topic table. Each example includes a mathematical idea, code in Python and R, and an output section. All records in the included dataset are **synthetic**; they do not describe actual students, a university, or a real intervention. The results are demonstrations of methods, not evidence about a real population.

## Assignment requirements covered

The brief asks for theoretical explanations, mathematical formulation, worked code, dataset analysis, statistical output, interpretation, and visualizations where useful. `REPORT.md` provides the explanations and interpretation guide, including observed example results. `src/analysis.py` and `src/analysis.R` generate the analysis and plots. `data/` contains generated data, `results/` contains numerical output, and `figures/` contains visualizations. The user should replace the synthetic dataset and rerun the analysis before making claims about a real subject.

## Reproduce the Python analysis

Python 3.10 or later is recommended.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src/analysis.py
```

On macOS/Linux, activate with `source .venv/bin/activate` instead. The Python run creates the dataset, plots, `results/all_results.json`, `results/summary.csv`, and a monthly-series CSV.

## Reproduce the R analysis

Run from this directory with R 4.1 or later:

```sh
Rscript src/analysis.R
```

The R script uses base R and writes its own synthetic data, plots, and result summaries. Python and R use the same data-generating design but separate random-number implementations, so their numeric outputs need not match exactly.

## Synthetic data dictionary

| Variable | Meaning | Generation |
|---|---|---|
| `student_id` | Synthetic row identifier | Sequential integer |
| `group` | Illustrative category A/B/C | Randomly sampled |
| `treatment` | Illustrative Control/Workshop label | Randomly sampled |
| `age` | Age-like numeric measure | Clipped normal draw |
| `study_hours` | Study-hours-like measure | Clipped gamma draw; 8% missing |
| `attendance_pct` | Attendance percentage-like measure | Clipped normal draw; 8% missing |
| `score` | Generated numeric outcome | Formula plus random noise, clipped to 0-100 |
| `passed` | Indicator for score >= 50 | Derived from generated score |

The score formula intentionally includes study hours, attendance, a small generated workshop offset, and group offsets. Although the labels resemble an educational setting, all rows and values are artificial. Random assignment of a label in this simulation does not model a real randomized experiment, and analysis of the generated association should not be presented as a causal finding.

## Scope and interpretation notes

The topic numbering follows the assignment's table. The first page's phrase “Each topic done to have the following” is implemented here across every listed topic because the request was to cover everything in the screenshots. Some outputs (for example, p-values, confidence intervals, accuracy, and clusters) depend on the generated sample and are not universal facts. Use the assumptions and caveats in `REPORT.md` when explaining them.

## Repository and presentation

Before presenting, add group member names and course details to `REPORT.md`, rerun both implementations, inspect the generated figures, and include the final public GitHub repository URL in the presentation. Do not claim a GitHub push has happened until a remote repository has actually received the commit.
