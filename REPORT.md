# BIT 4131 Statistical Computing and Reporting

I use Python and R to cover the 23 topics in the assignment brief. The brief did not include a dataset, so I use made-up data for the examples. The Python script creates 1,200 rows with an A/B/C category, a treatment label, age, study hours, attendance, score, and pass status. Study hours and attendance each have 8% missing values. No real student records are used.

The score is calculated from study hours, attendance, the category and treatment labels, and random noise. Scores of 50 or more count as passes. The treatment label does not represent a real workshop or experiment. All results below describe only the generated data.

## Topics and results

### 1. Measures of centre and spread

The mean is the total divided by the number of values. The median is the middle value after sorting. The interquartile range is \(Q_3-Q_1\), which covers the middle half of the data. For the 1,200 generated scores, the mean was 59.19, the median was 58.86, the standard deviation was 9.56, and the interquartile range was 12.97. The histogram and boxplot show the score distribution.

### 2. Probability

Conditional probability is \(P(A\mid B)=P(A\cap B)/P(B)\), when \(P(B)>0\). The pass rate was 83.6%, and the pass rate among rows labeled Workshop was 89.0%. A simulation of 100,000 pairs of coin flips gave a two-heads rate of 0.248, close to the exact value of 0.25.

### 3. Probability distributions

For a binomial variable, \(P(X=k)=\binom{n}{k}p^k(1-p)^{n-k}\). With \(n=10\) and \(p=0.5\), the chance of exactly 6 successes was 0.205, and the chance of 6 or fewer was 0.828. For a normal distribution with mean 70 and standard deviation 10, the chance of a value between 60 and 80 was 0.683. The normal curve on the score chart is a comparison, not proof that scores follow a normal distribution.

### 4. Sampling distributions and the Central Limit Theorem

The standard error of a sample mean is about \(\sigma/\sqrt{n}\). I took 2,000 samples of 40 values from a simulated population. The standard deviation of the sample means was 1.925; the theoretical standard error was 1.900. The chart shows the sampling distribution of those means.

### 5. Confidence intervals

A t interval for the mean is \(\bar{x}\pm t^*s/\sqrt{n}\). The 95% interval for the generated mean score was 58.65 to 59.73. Under the model assumptions, this method would capture the population mean in about 95% of repeated samples.

### 6. Hypothesis testing

Welch's two-sample t-test compares two means without assuming equal variances. The generated Workshop mean was 60.95 and the Control mean was 57.50. The p-value was 0.000000000264, so the test rejects equal means at the 5% level for this sample. This is a result from the data generator, not evidence about a real workshop.

### 7. Correlation and covariance

Correlation measures the direction and strength of a linear relationship on a scale from -1 to 1. Among complete rows, score correlated 0.397 with study hours and 0.238 with attendance. Correlation does not show that one variable caused another.

### 8. Linear regression and least squares

Least squares chooses coefficients that minimize \(\sum_i(y_i-\hat{y}_i)^2\). I used study hours, attendance, and the two labels to predict score. The study-hours coefficient was 1.118, and the model's R-squared was 0.284 for 1,014 complete rows. These are relationships in the simulated data. The residual plot is included to help inspect the model.

### 9. Matrix algebra

The least-squares coefficients can be found by solving \((X^TX)\hat{\beta}=X^Ty\). I used this equation for a model with an intercept, study hours, and attendance. The largest difference between this result and the OLS calculation from statsmodels was about \(4.5\times10^{-13}\), so the two calculations agree for this example.

### 10. Eigenvalues, eigenvectors, and PCA

Principal component analysis (PCA) combines several measures into new components. Each component explains some of the variation in the data. After standardizing study hours, attendance, age, and score, the first two components explained 36.1% and 26.9% of the variation, or 63.0% together.

### 11. Numerical optimization

Optimization finds parameter values that minimize or maximize a chosen function. I used the BFGS method to find a line that minimizes squared prediction errors for score and study hours. It converged to an intercept of 52.68 and a slope of 1.077.

### 12. Random numbers and Monte Carlo

Monte Carlo methods use random samples to estimate a value. I drew 500,000 points in a square and counted how many fell inside a circle. The estimate \(\hat{\pi}=4M/N\) was 3.1434, with an estimated simulation error of 0.00232.

### 13. Time-series analysis

A time series is a set of values recorded in time order. I made a 60-month series with an upward trend, a yearly pattern, and random noise. Its estimated trend was 1.636 units per month, and its lag-one autocorrelation was 0.949. This example is not a forecast for a real service.

### 14. Statistical charts

The project contains 12 charts: score histograms and boxplots, a distribution curve, a sampling-distribution chart, scatterplots, a regression residual plot, a PCA chart, a time-series chart, a normalization chart, a bootstrap chart, and a cluster chart. The charts describe the generated data.

### 15. Data transformation and normalization

A z-score is \(z=(x-\bar{x})/s\). It measures how far a value is from the mean in standard-deviation units. Min-max scaling changes values to a range from 0 to 1. In this example, the z-scores had a mean near 0 and a standard deviation of 1; the scaled scores ranged from 0 to 1.

### 16. ANOVA and experimental design

One-way ANOVA compares the means of three or more categories. Its test statistic is \(F=MS_{between}/MS_{within}\). For categories A, B, and C, the test gave F=15.02 and p=0.000000362. Tukey's follow-up test found differences between A and B, and between B and C. The labels are made up, so this is not a real experiment.

### 17. Chi-square and categorical data

The chi-square test checks whether two categories are related. It compares observed counts with counts expected if the categories were independent: \(\chi^2=\sum(O-E)^2/E\). The category-by-pass test gave 8.914 with 2 degrees of freedom and p=0.0116. Expected counts were above 5 in every cell.

### 18. Logistic regression

Logistic regression estimates the chance of a yes/no outcome using \(\log[p/(1-p)]=\beta_0+X\beta\). I used study hours, attendance, and age to predict pass status. Accuracy on the test sample was 83.1%, but the confusion matrix shows the model predicted almost every row as a pass. Accuracy alone therefore hides its mistakes on rows marked as not passing.

### 19. Non-parametric methods

The Mann-Whitney test compares ranks in two independent categories. It does not use the same normal-distribution assumption as a t-test. For the two treatment labels, U was 216,487.5 and the p-value was 0.00000000113. The medians were 60.52 for Workshop and 57.31 for Control.

### 20. Bootstrap and resampling

The bootstrap repeatedly draws samples from the data, allowing a row to be selected more than once. I calculated the mean score for 2,000 resamples. The bootstrap standard error was 0.276, and the 95% percentile interval was 58.67 to 59.73.

### 21. Multivariate analysis

Multivariate analysis looks at several variables at once. I calculated a covariance matrix, used PCA, and applied k-means to form three clusters. The cluster sizes were 415, 217, and 382 rows. These clusters are exploratory and have not been checked against real categories.

### 22. Missing data

Study hours and attendance each had 96 missing values, or 8%. There were 1,014 rows with complete values for both measures. I filled missing values with each column's median as a simple example. With real data, I would first investigate why values are missing and check whether the chosen method changes the results.

### 23. Statistical reporting and reproducibility

The scripts use random seed 4131 so the Python results can be repeated. Python saves the results as JSON and CSV. The R script saves a text summary and CSV. Both scripts save data and charts. The complete Python results are in `results/all_results.json` and `results/summary.csv`.

## Source

BIT 4131 Statistical Computing and Reporting assignment brief.
