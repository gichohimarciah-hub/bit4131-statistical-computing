# BIT 4131 Statistical Computing and Reporting

**Languages:** Python and R  
**Data:** Made-up data created for this project

## Introduction

I use Python and R to cover the 23 topics in the assignment brief. The brief did not include a dataset, so I use a made-up dataset for practice. The results and charts show how the methods work. They do not tell me anything about real students or schools.

## Data

The Python script makes 1,200 rows. Each row has an A/B/C category, a treatment label, age, study hours, attendance, a score, and a pass result. The score is made from study hours, attendance, the labels, and random noise. A score of 50 or more is marked as a pass. The script sets 8% of the study-hours values and 8% of the attendance values to missing.

The treatment label in this example is part of the data generator. It does not represent a real workshop or experiment. Any difference between the two labels is only a result from these made-up values.

## Results from the Python run

The results below came from the Python script with random seed 4131. The complete values are in `results/all_results.json` and `results/summary.csv`.

- The 1,200 scores had a mean of 59.19, a median of 58.86, a standard deviation of 9.56, and an interquartile range of 12.97.
- The pass rate was 83.6%. Among rows marked Workshop, it was 89.0%. These are rates in the generated data only.
- For the Binomial(10, 0.5) example, the probability of exactly 6 successes was 0.205. The chance of 6 or fewer was 0.828.
- For 2,000 samples of size 40, the standard deviation of the sample means was 1.925. The expected standard error was 1.900.
- The 95% confidence interval for the mean score was 58.65 to 59.73.
- The Workshop mean was 60.95 and the Control mean was 57.50. Welch's t-test gave a p-value of 0.000000000264. At the 5% level, the code rejects the equal-means hypothesis for this generated sample.
- Score had a correlation of 0.397 with study hours and 0.238 with attendance.
- In the multiple regression, the study-hours coefficient was 1.118 and the model's R-squared was 0.284. These are associations built into the simulated data.
- The matrix solution and the OLS calculation gave almost identical coefficients. Their largest difference was about 0.00000000000045.
- The first two PCA components explained 36.1% and 26.9% of the variation, or 63.0% together.
- The optimization example found a line with an intercept of 52.68 and a slope of 1.077.
- The Monte Carlo estimate of pi was 3.1434 from 500,000 random points. Its estimated simulation error was 0.00232.
- The made-up 60-month series had a trend of 1.636 units per month and lag-one autocorrelation of 0.949.
- The Python script made 12 charts. They show score distributions, group relationships, model residuals, PCA, a time series, a bootstrap sample, and clusters.
- The score z-scores had a mean near 0 and a standard deviation of 1. Min-max scaling changed the scores to a range from 0 to 1.
- The group ANOVA gave F=15.02 and p=0.000000362. Tukey's comparisons found differences between A and B, and between B and C.
- The chi-square test gave 8.914 with 2 degrees of freedom and p=0.0116. Expected counts were above 5 in every cell.
- The logistic model had 83.1% accuracy on its test sample. Its confusion matrix shows that it predicted almost every row as a pass, so accuracy alone gives a misleading picture.
- The Mann-Whitney test gave U=216,487.5 and p=0.00000000113. The medians were 60.52 for Workshop and 57.31 for Control.
- The bootstrap standard error for the mean was 0.276. Its 95% interval was 58.67 to 59.73.
- K-means made three clusters with 415, 217, and 382 rows. These groups are just a result of this calculation; they have not been checked against real categories.
- Study hours and attendance each had 96 missing values. There were 1,014 complete rows. The example fills missing values with each column's median.
- The fixed seed was 4131. The Python run produced 23 result sections, 12 charts, and the CSV and JSON files in this repository.

## Methods by topic

### 1. Measures of centre and spread

The mean is the total of the values divided by the number of values. The median is the middle value after sorting. The range is the maximum minus the minimum. The interquartile range is \(Q_3-Q_1\); it covers the middle half of the data. We calculate these values for scores and draw a histogram and boxplot.

### 2. Probability

For events A and B, conditional probability is \(P(A\mid B)=P(A\cap B)/P(B)\), when \(P(B)>0\). We calculate pass rates and the share of Workshop rows that passed. We also simulate two coin flips. The simulated chance of two heads should be close to 0.25, but it can vary a little.

### 3. Probability distributions

For a binomial variable, \(P(X=k)=\binom{n}{k}p^k(1-p)^{n-k}\). We use it to find the chance of exactly 6 successes out of 10 when \(p=0.5\), and the chance of 6 or fewer. We also calculate a normal-distribution probability between 60 and 80 for a mean of 70 and standard deviation of 10. The fitted normal curve on the score chart is a guide; it does not prove the scores are normally distributed.

### 4. Sampling distributions and the Central Limit Theorem

A sample mean changes from sample to sample. Its standard error is about \(\sigma/\sqrt{n}\). We take 2,000 samples of 40 values from a simulated population and plot their means. The sample means form a roughly bell-shaped distribution, and their spread is close to the standard error formula.

### 5. Confidence intervals

For the mean, the t interval is \(\bar{x}\pm t^*s/\sqrt{n}\). We use a 95% interval for the generated scores. The interval gives a range of reasonable values for the mean under the model assumptions. It is not a statement that there is a 95% chance this one interval contains a fixed mean.

### 6. Hypothesis testing

Welch's two-sample t-test compares two means without assuming their variances are equal. The null hypothesis says the means are equal. The alternative says they differ. The script reports the group means, t statistic, and p-value. The p-value is compared with 0.05. The result only describes our generated data.

### 7. Correlation and covariance

Covariance shows whether two variables tend to move together. Correlation puts that relationship on a scale from -1 to 1. We calculate both for study hours, attendance, and score using rows with complete values. The scatterplot shows study hours and score. Correlation does not show that one variable caused the other.

### 8. Linear regression and least squares

Linear regression fits a line or plane to predict an outcome. Least squares chooses coefficients that minimize \(\sum_i(y_i-\hat{y}_i)^2\). Our model uses study hours, attendance, treatment label, and group to predict score. We report the coefficients, p-values, R-squared, and a residual plot. The coefficients describe relationships in the simulated data.

### 9. Matrix algebra

The least-squares coefficients can be found by solving \((X^TX)\hat{\beta}=X^Ty\). We use this equation for a model with an intercept, study hours, and attendance. We compare the result with the OLS calculation from statsmodels. The very small difference shows that both calculations give the same result here.

### 10. Eigenvalues, eigenvectors, and PCA

Principal component analysis (PCA) turns several related measures into new combined measures. Each component explains part of the overall variation. We standardize study hours, attendance, age, and score, then calculate the components and their explained variation. The first two components explain 62.0% of the variation in this example.

### 11. Numerical optimization

Optimization finds the parameter values that make a chosen result as small or large as possible. We use the BFGS method to find a straight line that minimizes the sum of squared errors when predicting score from study hours. The script reports the line and whether the optimizer reached a solution.

### 12. Random numbers and Monte Carlo

Monte Carlo methods use random samples to estimate a value. We draw points in a square and count how many fall inside a circle. The circle-to-square area ratio gives the estimate \(\hat{\pi}=4M/N\), where M is the number inside and N is the total number drawn. More draws usually make the estimate steadier.

### 13. Time-series analysis

A time series is a set of values recorded in time order. We create 60 monthly values with an upward trend, yearly pattern, and random noise. The chart shows the pattern. We also calculate the trend per month and the relationship between nearby months. This is an example series, not a forecast for a real service.

### 14. Statistical charts

Charts help us see patterns in the data. The project includes histograms, boxplots, scatterplots, a regression residual plot, PCA and cluster plots, a bootstrap histogram, and a time-series plot. Each chart labels its axes. The charts describe the simulated values only.

### 15. Data transformation and normalization

A z-score is \(z=(x-\bar{x})/s\). It shows how far a value is from the mean in standard-deviation units. Min-max scaling changes values to a range from 0 to 1. We calculate both versions of score and compare their summaries and charts.

### 16. ANOVA and experimental design

One-way ANOVA compares the means of three or more groups. Its test statistic is \(F=MS_{between}/MS_{within}\). We compare scores in groups A, B, and C. If the ANOVA finds a difference, Tukey's test checks pairs of groups. The group labels are made up, so this is not a real experiment.

### 17. Chi-square and categorical data

The chi-square test checks whether two categories are related. It compares the observed counts with counts expected if the categories were independent: \(\chi^2=\sum(O-E)^2/E\). We use a table of group and pass status. Expected counts are all above 5 in this run, which supports using the test's usual approximation.

### 18. Logistic regression

Logistic regression estimates the chance of a yes/no outcome. It models the log odds as \(\log[p/(1-p)]=\beta_0+X\beta\). We use study hours, attendance, and age to predict pass status. We report coefficients, accuracy, and a confusion matrix. The model predicts almost everyone as a pass, so its accuracy hides its errors on students marked as not passing.

### 19. Non-parametric methods

The Mann-Whitney test compares the ranks of values in two independent groups. It does not require the same normal-distribution assumption as a t-test. We use it to compare the two treatment labels and report the test statistic, p-value, and medians. The result still depends on having independent rows.

### 20. Bootstrap and resampling

The bootstrap repeatedly draws new samples from the observed data, allowing the same row to be selected more than once. We calculate the mean score for 2,000 resamples. The spread of those means estimates the standard error, and their 2.5th and 97.5th percentiles give an interval.

### 21. Multivariate analysis

Multivariate analysis looks at several variables at once. We calculate a covariance matrix, use PCA to reduce the number of measures, and use k-means to form three groups. K-means places similar rows together based on distance. The clusters are exploratory and do not have confirmed real-world meanings.

### 22. Missing data

We first count missing values and compare complete-case rows with the full dataset. Then we fill the missing study-hours and attendance values with each column's median. This is a simple example. For real data, we would need to understand why values are missing and check whether the choice of method changes the results.

### 23. Statistical reporting and reproducibility

The scripts use a fixed random seed so the Python example can be repeated. Python saves results as JSON and CSV. R saves a text summary and CSV. Both scripts save charts and data. Keeping the code, data, and results together lets the group repeat the same analysis later.

## Conclusion

This project shows how to calculate and explain the 23 methods in the brief. The results come from made-up data, so they are only examples. We would need a real dataset before drawing conclusions about students, schools, or teaching methods.

## Source

BIT 4131 Statistical Computing and Reporting Group Work brief supplied for this assignment.
