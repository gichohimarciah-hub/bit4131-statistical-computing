# BIT 4131: companion R implementation for the 23 concepts.
# Data are synthetic, generated with a fixed seed, and describe no real people.
set.seed(4131)
# Run from the project root with: Rscript src/analysis.R
root <- getwd()
dir.create(file.path(root, "data"), showWarnings = FALSE, recursive = TRUE)
dir.create(file.path(root, "results"), showWarnings = FALSE, recursive = TRUE)
dir.create(file.path(root, "figures"), showWarnings = FALSE, recursive = TRUE)
data_path <- file.path(root, "data", "synthetic_student_outcomes.csv")
if (!file.exists(data_path)) stop("Run the Python script first to create the shared dataset.")
dat <- read.csv(data_path)
required_columns <- c("student_id", "group", "treatment", "age", "study_hours", "attendance_pct", "score", "passed")
if (!all(required_columns %in% names(dat))) stop("The shared dataset is missing required columns.")
n <- nrow(dat)
res <- list()
saveplot <- function(name, expr) { png(file.path(root,"figures",name), width=900, height=600); force(expr); dev.off() }

# 1 Descriptive measures
x <- dat$score
res[["01_descriptive"]] <- c(n=length(x), mean=mean(x), median=median(x),
  variance=var(x), sd=sd(x), q1=quantile(x,.25), q3=quantile(x,.75),
  iqr=IQR(x), range=diff(range(x)))
saveplot("R_01_score_histogram.png", hist(x, breaks=25, main="Synthetic score distribution", xlab="Score", col="steelblue"))

# 2 Probability and conditional probability
ws <- dat$treatment == "Workshop"; pass <- dat$passed == 1
res[["02_probability"]] <- c(p_pass=mean(pass), p_workshop=mean(ws),
  p_pass_given_workshop=mean(pass[ws]), p_joint=mean(pass & ws))

# 3 Distributions
res[["03_distributions"]] <- c(binomial_pmf=dbinom(6,10,.5), binomial_cdf=pbinom(6,10,.5),
  fitted_normal_within_one_sd=pnorm(mean(x)+sd(x),mean(x),sd(x))-pnorm(mean(x)-sd(x),mean(x),sd(x)))

# 4 Sampling distributions and CLT
pop <- rnorm(100000,70,12); means <- replicate(2000, mean(sample(pop,40)))
res[["04_sampling_clt"]] <- c(population_mean=mean(pop), sampling_mean=mean(means),
  sampling_sd=sd(means), theoretical_se=sd(pop)/sqrt(40))
saveplot("R_04_clt.png", hist(means, breaks=30, main="Sampling distribution of mean (n=40)", xlab="Sample mean", col="seagreen"))

# 5 t confidence interval
res[["05_confidence_interval"]] <- t.test(x)$conf.int

# 6 Welch two-sample test
tt <- t.test(score ~ treatment, data=dat)
res[["06_hypothesis_test"]] <- c(workshop_mean=mean(dat$score[ws]), control_mean=mean(dat$score[!ws]),
  statistic=unname(tt$statistic), p_value=tt$p.value)

# 7 Correlation and covariance
complete <- na.omit(dat[c("study_hours","attendance_pct","score")])
res[["07_correlation_covariance"]] <- list(correlation=cor(complete), covariance=cov(complete))

# 8 Linear regression
reg <- na.omit(dat[c("score","study_hours","attendance_pct","age","treatment","group")])
fit <- lm(score ~ study_hours + attendance_pct + treatment + group, data=reg)
res[["08_linear_regression"]] <- list(coefficients=coef(fit), p_values=coef(summary(fit))[,4],
  r_squared=summary(fit)$r.squared, n=nobs(fit))
saveplot("R_08_residuals.png", { plot(fitted(fit),resid(fit),xlab="Fitted",ylab="Residual",main="OLS residual diagnostic"); abline(h=0) })

# 9 Matrix algebra least-squares solution
X <- model.matrix(~ study_hours + attendance_pct, data=reg); y <- reg$score
beta <- solve(crossprod(X), crossprod(X,y))
res[["09_matrix_algebra"]] <- list(dim=dim(X), determinant=det(crossprod(X)), beta=drop(beta))

# 10 Eigenvalues, eigenvectors and PCA
scaled_predictors <- scale(reg[c("study_hours","attendance_pct","age","score")])
pc <- prcomp(scaled_predictors, center=FALSE, scale.=FALSE)
res[["10_pca"]] <- list(eigenvalues=pc$sdev^2, variance_ratio=(pc$sdev^2)/sum(pc$sdev^2), rotation=pc$rotation)
saveplot("R_10_pca.png", plot(cumsum(pc$sdev^2/sum(pc$sdev^2)), type="b", xlab="Components", ylab="Cumulative variance", main="PCA variance"))

# 11 Numerical optimization
objective <- function(b) sum((y - (b[1]+b[2]*reg$study_hours))^2)
op <- optim(c(0,0), objective, method="BFGS")
res[["11_optimization"]] <- list(parameters=op$par, minimum=op$value, convergence_code=op$convergence)

# 12 Monte Carlo estimate of pi
u <- runif(500000,-1,1); v <- runif(500000,-1,1); p_in <- mean(u^2+v^2<=1)
res[["12_monte_carlo"]] <- c(draws=length(u), pi_estimate=4*p_in, approximate_se=4*sqrt(p_in*(1-p_in)/length(u)))

# 13 Read the monthly series created by the Python script
monthly_path <- file.path(root,"results","13_monthly_series.csv")
if (!file.exists(monthly_path)) stop("Run the Python script first to create the monthly series.")
monthly <- read.csv(monthly_path,check.names=FALSE)
series_dates <- as.Date(monthly[[1]])
series_values <- monthly[[2]]
series <- ts(series_values,start=c(as.integer(format(series_dates[1],"%Y")),
  as.integer(format(series_dates[1],"%m"))),frequency=12)
t <- seq_along(series)-1
res[["13_time_series"]] <- c(n=length(series), mean=mean(series), lag1=acf(series,plot=FALSE)$acf[2], slope=coef(lm(as.numeric(series)~t))[2])
saveplot("R_13_time_series.png", plot(series, main="Synthetic monthly enrollment series", ylab="Enrollment index"))

# 14 Statistical visualization
saveplot("R_14_scatter.png", { plot(dat$attendance_pct,dat$score,col=ifelse(dat$passed==1,"firebrick","navy"),
  xlab="Attendance (%)",ylab="Score",main="Score by attendance"); legend("topright",legend=c("Fail","Pass"),pch=1,col=c("navy","firebrick")) })
res[["14_visualization"]] <- list(observations=nrow(dat),encoding="attendance vs score; color denotes generated pass status")

# 15 Transformations and normalization
z <- as.numeric(scale(x)); mm <- (x-min(x))/(max(x)-min(x))
res[["15_transform_normalize"]] <- c(raw_mean=mean(x),raw_sd=sd(x),z_mean=mean(z),z_sd=sd(z),minmax_min=min(mm),minmax_max=max(mm))

# 16 ANOVA and Tukey comparisons
af <- aov(score~group,data=dat)
res[["16_anova"]] <- list(anova=summary(af), group_means=tapply(dat$score,dat$group,mean), tukey=TukeyHSD(af))

# 17 Chi-square categorical analysis
tab <- table(dat$group,dat$passed); ch <- chisq.test(tab)
res[["17_chi_square"]] <- list(table=tab,expected=ch$expected,statistic=unname(ch$statistic),df=unname(ch$parameter),p_value=ch$p.value)

# 18 Logistic regression, simple training/test split
lg <- na.omit(dat[c("passed","study_hours","attendance_pct","age")]); set.seed(4131)
train_id <- sample(seq_len(nrow(lg)),floor(.75*nrow(lg))); glmfit <- glm(passed~study_hours+attendance_pct+age,data=lg[train_id,],family=binomial())
prob <- predict(glmfit,newdata=lg[-train_id,],type="response"); class_pred <- as.integer(prob>=.5)
res[["18_logistic_regression"]] <- list(coefficients=coef(glmfit), odds_ratios=exp(coef(glmfit)),
  accuracy=mean(class_pred==lg$passed[-train_id]), confusion=table(actual=lg$passed[-train_id],predicted=class_pred))

# 19 Mann-Whitney non-parametric comparison
mw <- wilcox.test(score~treatment,data=dat,exact=FALSE)
res[["19_nonparametric"]] <- list(statistic=unname(mw$statistic),p_value=mw$p.value,
  medians=tapply(dat$score,dat$treatment,median))

# 20 Bootstrap mean and percentile interval
bs <- replicate(2000,mean(sample(x,length(x),replace=TRUE)))
res[["20_bootstrap"]] <- c(bootstrap_mean=mean(bs),bootstrap_se=sd(bs),quantile(bs,c(.025,.975)))
saveplot("R_20_bootstrap.png", hist(bs,breaks=30,main="Bootstrap distribution of mean score",xlab="Bootstrap mean",col="darkorange"))

# 21 Multivariate summaries, PCA and base-R k-means
set.seed(4131); km <- kmeans(scaled_predictors,centers=3,nstart=10)
res[["21_multivariate"]] <- list(covariance=cov(reg[c("study_hours","attendance_pct","age","score")]),
  pca2_variance=sum(pc$sdev[1:2]^2)/sum(pc$sdev^2),cluster_sizes=km$size)

# 22 Missing-data analysis and median imputation illustration
m <- dat[c("study_hours","attendance_pct")]; imp <- m
for (nm in names(imp)) imp[[nm]][is.na(imp[[nm]])] <- median(imp[[nm]],na.rm=TRUE)
before_after <- lapply(names(m), function(nm) list(before_mean=mean(m[[nm]],na.rm=TRUE),
  before_sd=sd(m[[nm]],na.rm=TRUE),after_mean=mean(imp[[nm]]),after_sd=sd(imp[[nm]])))
names(before_after) <- names(m)
res[["22_missing_data"]] <- list(missing_count=colSums(is.na(m)),missing_fraction=colMeans(is.na(m)),
  medians=sapply(m,median,na.rm=TRUE),complete_case_n=sum(complete.cases(m)),imputed_n=nrow(imp),method="median",
  before_after_mean_sd=before_after)

# 23 Reproducible reporting: write all topic results to readable CSV; console output is captured in Rscript log.
res[["23_reproducibility"]] <- list(random_seed=4131,synthetic_rows=n,synthetic_data_only=TRUE,
  data_file="data/synthetic_student_outcomes.csv",monthly_series_file="results/13_monthly_series.csv",
  output_files=c("results/R_summary.csv","results/R_all_results.txt","figures/R_*.png"))
flat <- data.frame(topic=names(res), result=vapply(res,function(z) paste(capture.output(str(z)),collapse=" "),character(1)))
write.csv(flat,file.path(root,"results","R_summary.csv"),row.names=FALSE)
capture.output(print(res),file=file.path(root,"results","R_all_results.txt"))
cat("Generated results for",length(res),"topics. Synthetic data only.\n")

