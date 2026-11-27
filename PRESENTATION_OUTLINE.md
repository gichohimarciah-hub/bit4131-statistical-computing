# Presentation outline

The brief requests a presentation and asks groups to share the implementation/data-analysis link (items 3-6) during the presentation. This outline is a speaking aid, not a finished slide deck. Replace the group placeholders and link before presenting.

## Suggested order

1. **Title and team** - BIT 4131, project title, group members and registration numbers.
2. **Aim and dataset** - explain that the included dataset is synthetic, why it was generated, the variables, missingness, sample size, and fixed seed.
3. **Probability and distributions (topics 1-4)** - descriptive summaries, probability, distributions, sampling distribution/CLT; show selected output and histogram.
4. **Inference and association (topics 5-7, 16-17, 19-20)** - confidence interval, Welch test, correlation, ANOVA, chi-square, rank test, bootstrap; explain assumptions and how to read p-values/intervals.
5. **Models and computation (topics 8-12, 18)** - OLS, matrix solution, PCA/eigenvalues, optimization, Monte Carlo, logistic regression; explain outputs and diagnostics.
6. **Time, visualization and data preparation (topics 13-15, 21-22)** - synthetic series, plots, normalization, multivariate exploration, missing-data summary/imputation.
7. **Reproducible reporting (topic 23)** - show folder layout, fixed seeds, Python/R implementations, and how to reproduce outputs.
8. **Limitations and conclusion** - synthetic data cannot support claims about actual students or interventions; summarize demonstrated methods.
9. **Repository link** - insert the GitHub URL once the repository has been created and pushed.

## Suggested live demo

From the repository root, run `python src/analysis.py`. Point to `results/summary.csv` and two or three figures. If R is available, run `Rscript src/analysis.R` as the second-language implementation. Do not claim outputs from a dataset the group has not actually analyzed.
