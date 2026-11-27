# Statistical Computing and Reporting: 23 Worked Topics

**Course:** BIT 4131 Statistical Computing and Reporting  
**Group members:** Add the group members' names and registration numbers here.  
**Implementation:** Python and R  
**Data:** Reproducible synthetic teaching data; no real student records were used.

## Abstract

This project implements the 23 statistical-computing topics listed in the assignment brief. A fixed-seed generator creates a synthetic dataset with 1,200 rows and numeric, categorical, outcome, time-series, and missing-data examples. Python and R scripts demonstrate the corresponding calculations and produce tables and figures. Since the data are artificial, numerical findings are useful only to explain the methods; they cannot support conclusions about actual students, courses, or interventions.

## Data and method

The data generator creates an illustrative score from study hours, attendance, an assigned label called treatment, group offsets, and random error. Study hours and attendance are each made missing in approximately eight percent of rows. The binary outcome `passed` is set to one for generated scores of at least 50. A separate synthetic monthly series is generated for time-series methods. The fixed random seed makes each language's run reproducible, although Python and R random-number generators differ and therefore do not produce row-for-row identical samples.

The treatment label was randomly assigned by the generator without modeling a trial design or real treatment process. Its estimated difference is descriptive of this artificial construction, not a causal effect. Other p-values and model metrics are likewise demonstrations, not evidence about a population.

## Observed Python results (seed 4131)

The following are actual outputs from the included Python run on the generated dataset. They are rounded for readability; the full precision values and remaining outputs are in `results/all_results.json` and `results/summary.csv`.

1. **Descriptive measures:** 1,200 generated scores had mean 59.19, median 58.86, sample SD 9.56, and IQR 12.97.
2. **Probability:** The generated pass proportion was 0.836; among workshop-labeled rows it was 0.890. The simulated two-heads probability was 0.248 for 100,000 pairs (exact value 0.25).
3. **Distributions:** For Binomial(10, 0.5), the computed point probability at 6 was 0.205 and the cumulative probability through 6 was 0.828. The Normal(70, 10) probability from 60 to 80 was 0.683.
4. **Sampling/CLT:** Across 2,000 samples of size 40, the sample-mean SD was 1.925 versus theoretical SE 1.900.
5. **Confidence interval:** The 95% t interval for the synthetic mean was [58.65, 59.73].
6. **Hypothesis test:** Workshop mean 60.95 versus control mean 57.50; Welch t=6.373, p=2.64e-10. The script's rule rejects equal means at .05. This reflects the constructed synthetic data only.
7. **Correlation:** Score correlated 0.397 with study hours and 0.238 with attendance among complete cases. These are simulated associations.
8. **Regression:** The adjusted OLS coefficient for study hours was 1.118 score units per generated hour; model \(R^2=0.284\) using 1,014 complete records. It is not a real educational effect.
9. **Matrix solution:** Direct normal-equation coefficients agreed with the statsmodels OLS fit to a maximum absolute difference of about \(4.5\times10^{-13}\) for the two-predictor model.
10. **PCA:** The first two standardized components explained 36.1% and 26.9% of variance (62.0% cumulatively).
11. **Optimization:** The BFGS line fit converged to intercept 52.68 and slope 1.077 for its unadjusted score-on-hours objective.
12. **Monte Carlo:** 500,000 random points produced \(\hat\pi=3.1434\), with approximate Monte Carlo SE 0.00232.
13. **Time series:** The generated 60-month series had estimated trend 1.636 units/month and lag-one autocorrelation 0.949. The series is deliberately trending and seasonal.
14. **Visualization:** The Python run generated 12 PNG figures; the topic 14 scatterplot covers 1,200 rows and colors points by generated pass status.
15. **Normalization:** The score z-scores had mean approximately 0 and SD 1; min-max scores ranged from 0 to 1.
16. **ANOVA:** The group test returned F=15.02, p=3.62e-7. Tukey comparisons flagged A-B and B-C; this is a consequence of the generator's group offsets.
17. **Chi-square:** Group and pass status gave \(\chi^2=8.914\), df=2, p=0.0116. Expected cell counts were all above 5 in this run.
18. **Logistic regression:** Held-out accuracy was 0.831, but the confusion matrix shows the model predicted almost every test record as passed. Accuracy alone therefore hides poor classification of failures.
19. **Non-parametric test:** Mann-Whitney U=216,487.5, p=1.13e-9; generated medians were 60.52 (Workshop) and 57.31 (Control).
20. **Bootstrap:** 2,000 resamples gave mean 59.19, bootstrap SE 0.276, and percentile 95% interval [58.67, 59.73].
21. **Multivariate analysis:** K-means with k=3 returned cluster sizes 415, 217, and 382. Clusters are exploratory groupings, not validated categories.
22. **Missing data:** There were 96 missing values each in study hours and attendance (8%); complete cases numbered 1,014. Median imputation was shown as an illustration only.
23. **Reproducibility:** Python seed 4131 produced 1,200 synthetic records, 23 topic result sections, 12 figures, and the CSV/JSON outputs in this repository.

## Topic explanations, worked analyses, and interpretation

### 1. Measures of central tendency and dispersion

The mean is \(\bar{x}=\sum_i x_i/n\), the median is the middle ordered value, and the mode is the most frequent value. Sample variance is \(s^2=\sum_i(x_i-\bar{x})^2/(n-1)\), with standard deviation \(s=\sqrt{s^2}\). Quartiles and the interquartile range \(IQR=Q_3-Q_1\) describe spread robustly. The scripts calculate these for `score` and save a histogram and boxplot. Interpret the mean and median as summaries of generated scores; the IQR describes the middle half of that artificial distribution.

### 2. Probability and conditional probability

For events \(A,B\), \(P(A\mid B)=P(A\cap B)/P(B)\) when \(P(B)>0\). The analysis estimates the generated pass proportion, workshop proportion, joint proportion, and pass proportion among workshop-labeled rows. A simulation estimates the probability of two heads in two fair coin flips. Compare the conditional and overall proportions as empirical descriptions; simulation error means the coin estimate need not equal its exact value of one quarter.

### 3. Probability distributions

For \(X\sim Binomial(n,p)\), \(P(X=k)=\binom nkp^k(1-p)^{n-k}\). A normal variable has density \(f(x)=\{\sigma\sqrt{2\pi}\}^{-1}\exp[-(x-\mu)^2/(2\sigma^2)]\). The code evaluates a binomial point probability and cumulative probability, plus a normal interval probability, and plots the generated score histogram with a fitted normal reference curve. The curve is a visual reference; it does not establish that scores follow a normal distribution.

### 4. Sampling distributions and the Central Limit Theorem

For independent observations with finite variance, the sample mean has standard error approximately \(\sigma/\sqrt n\), and its standardized sampling distribution tends toward normality as \(n\) grows. Repeated samples of size 40 are drawn from a simulated normal population. The histogram of sample means and the empirical standard error are compared with the theoretical standard error. This controlled simulation illustrates the sampling distribution, not uncertainty in a real survey.

### 5. Confidence intervals

For a mean with unknown variance under independent normal sampling, a two-sided t interval is \(\bar{x}\pm t_{1-\alpha/2,n-1}s/\sqrt n\). The scripts report a 95% t interval for generated scores. In repeated use under the model assumptions, 95% of such intervals would cover the population mean; it is not a 95% probability statement about this one fixed interval.

### 6. Hypothesis testing

The Welch two-sample statistic is \(t=(\bar{x}_1-\bar{x}_2)/\sqrt{s_1^2/n_1+s_2^2/n_2}\), with degrees of freedom estimated from the sample variances. The null is equal population means; the two-sided alternative is a difference. The code reports group means, statistic, p-value, and a decision at \(\alpha=.05\). “Reject” means the data would be relatively unusual under the null and assumptions; it does not prove a practical or causal effect.

### 7. Correlation and covariance

Sample covariance is \(s_{xy}=\sum_i(x_i-\bar{x})(y_i-\bar{y})/(n-1)\), and Pearson correlation is \(r=s_{xy}/(s_xs_y)\). The analysis reports matrices for study hours, attendance, and score among complete cases and plots study hours against score. Correlation measures linear association and can be affected by outliers; it does not imply causation.

### 8. Linear regression and least squares

The linear model is \(y=X\beta+\epsilon\); ordinary least squares minimizes \(\sum_i(y_i-\hat y_i)^2\), giving \(\hat\beta=(X^TX)^{-1}X^Ty\) when the inverse exists. The fitted model predicts score using hours, attendance, treatment label, and group. The code reports coefficients, p-values, \(R^2\), and a residual-versus-fitted plot. A coefficient is a conditional association in this synthetic model; interpretation relies on model form and error assumptions.

### 9. Matrix algebra in statistics

The design matrix stores observations by rows and predictors by columns. The least-squares normal equations are \(X^TX\hat\beta=X^Ty\). The code solves this system directly for an intercept, study hours, and attendance, and compares the coefficients with the statsmodels OLS solution. A nearly singular \(X^TX\) would make the direct inverse/solve numerically unstable; the determinant and coefficient comparison are included as diagnostics.

### 10. Eigenvalues, eigenvectors, and PCA

For a centered/scaled data matrix with covariance matrix \(S\), PCA finds eigenvectors \(v_j\) and eigenvalues \(\lambda_j\) satisfying \(Sv_j=\lambda_jv_j\). The proportion of variance explained by component \(j\) is \(\lambda_j/\sum_k\lambda_k\). The code standardizes four numeric variables, reports components and variance ratios, and plots cumulative explained variance. Component signs are arbitrary, and principal components are combinations of the input measures rather than new causal factors.

### 11. Numerical optimization

Optimization seeks \(\theta^*=\arg\min_\theta f(\theta)\). The example minimizes the sum of squared errors for a line predicting score from study hours, using the BFGS numerical optimizer. It reports parameters, minimized objective, convergence status, and optimizer message. The method can reach local optima for non-convex objectives; this least-squares objective is convex in its two parameters.

### 12. Random numbers and Monte Carlo methods

For points drawn uniformly from the square \([-1,1]^2\), the fraction inside the unit circle estimates the area ratio \(\pi/4\). Thus \(\hat\pi=4M/N\), with approximate standard error \(4\sqrt{\hat p(1-\hat p)/N}\). The scripts use 500,000 draws and report this estimate and its Monte Carlo standard error. A different seed or draw count yields a slightly different estimate.

### 13. Time-series analysis

A time series \(Y_t\) is ordered by time; trend, seasonality, and serial dependence should be considered before modeling. Lag-one autocorrelation is \(\hat\rho_1=\widehat{Cov}(Y_t,Y_{t-1})/\hat{Var}(Y_t)\). A synthetic monthly series combines linear trend, annual sinusoidal seasonality, and noise. The code plots it, estimates a linear slope, and reports lag-one autocorrelation. It does not make a forecast because no real operational series was supplied.

### 14. Statistical data visualization

Plots encode observations to make distribution, association, group differences, or time patterns easier to inspect. The project includes histograms, boxplots, scatterplots, a residual plot, PCA variance plot, bootstrap distribution, and a time plot. Axes and units are labeled. Visual patterns are descriptive and should be read together with sample size and model assumptions.

### 15. Data transformation and normalization

Z-score standardization is \(z_i=(x_i-\bar{x})/s\), while min-max normalization is \((x_i-x_{min})/(x_{max}-x_{min})\). Log or other transformations can address skew only when suitable for the variable and analysis. The code compares the raw score distribution with its z-scores and reports range and moments. Standardization changes scale, not the underlying information, and min-max values depend on sample extremes.

### 16. ANOVA and experimental design

One-way ANOVA tests whether all group means are equal using \(F=MS_{between}/MS_{within}\). The code fits score by group, reports an ANOVA table, means, and Tukey pairwise comparisons. Independence, approximately normal within-group errors, and comparable variances are standard assumptions. The categories here are generated labels, not a real experimental design; a significant result would only describe this simulation.

### 17. Chi-square and categorical data analysis

For a contingency table, expected cell counts under independence are \(E_{ij}=row_i\ total\times col_j\ total/N\). Pearson's statistic is \(\chi^2=\sum_{ij}(O_{ij}-E_{ij})^2/E_{ij}\). The code cross-tabulates group by pass status and reports expected counts, statistic, degrees of freedom, and p-value. The approximation can be poor when expected counts are small; check them before interpreting.

### 18. Logistic regression

For binary \(Y\), logistic regression models \(log[p/(1-p)]=\beta_0+X\beta\). Exponentiated coefficients are conditional odds ratios per unit increase, given the other predictors. The Python implementation reports coefficients, held-out accuracy, and a confusion matrix; the R script reports coefficients, odds ratios, and held-out accuracy. Accuracy depends on class balance and threshold and is not a complete evaluation; results are from synthetic labels.

### 19. Non-parametric statistical methods

The Mann-Whitney U (Wilcoxon rank-sum) test compares rank distributions between two independent groups. Under similarly shaped distributions it is often interpreted as a location comparison, but it is not generally a test of medians alone. The code reports the U statistic, p-value, and sample medians for the two generated treatment labels. Independence and correct group definition remain necessary.

### 20. Bootstrap and resampling

The nonparametric bootstrap repeatedly samples \(n\) observations with replacement and recomputes a statistic. The standard deviation of bootstrap estimates estimates its standard error; percentile quantiles provide an interval. The project uses 2,000 resamples for the mean score and plots the bootstrap distribution. Bootstrap validity depends on the sample representing the target population and can be weak for dependent or highly sparse data.

### 21. Multivariate statistical analysis

Multivariate methods consider several variables jointly. The example reports a covariance matrix, retains the first two PCA components, and applies k-means to standardized numeric measures. K-means minimizes within-cluster squared Euclidean distance and requires choosing \(k\). Cluster labels are arbitrary; clusters are exploratory summaries and should not be treated as natural or validated groups without external evaluation.

### 22. Missing-data analysis and imputation

Missingness should first be summarized by variable and pattern. Complete-case analysis discards incomplete rows; median imputation replaces a missing value with the observed median. The scripts report counts/fractions, complete-case size, and imputed values. Single imputation understates uncertainty and can bias associations, so real studies should justify assumptions (MCAR/MAR/MNAR), consider multiple imputation where appropriate, and perform sensitivity analysis.

### 23. Statistical reporting and reproducibility

Reproducible reporting keeps data definitions, code, random seeds, software requirements, outputs, and interpretation together. Python writes JSON and CSV results; R writes a text summary and CSV; both scripts generate figures and synthetic data. Record the runtime versions used for an actual presentation and retain the exact source dataset (with appropriate privacy safeguards) if replacing the synthetic example.

## Conclusion

The scripts demonstrate a broad set of statistical calculations and reporting workflows in Python and R. The generated numerical results validate the examples only within the simulation design. No real-data conclusion can be drawn until the group selects a real topic-specific dataset, checks its quality and provenance, reruns the methods, and rewrites the interpretation accordingly.

## References

1. BIT 4131 Statistical Computing and Reporting Group Work brief supplied with the assignment. Topic sequence and expected outputs in this report follow that brief.
2. Package documentation for the specific software versions used should be cited in the final presentation if required by the lecturer. No external dataset or factual claim is used in this synthetic demonstration.
