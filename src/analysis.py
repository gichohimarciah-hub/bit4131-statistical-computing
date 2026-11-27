"""Reproducible examples for the 23 BIT 4131 statistical computing topics.

All records are synthetic and generated with a fixed seed. They are for
teaching only and do not describe real students or institutions.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats, optimize
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for reproducible script runs.
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA, RESULTS, FIGURES = ROOT / "data", ROOT / "results", ROOT / "figures"
SEED = 4131


def make_data(n: int = 1200) -> pd.DataFrame:
    """Create a deterministic, documented synthetic student-outcomes dataset."""
    rng = np.random.default_rng(SEED)
    group = rng.choice(["A", "B", "C"], n, p=[.34, .33, .33])
    treatment = rng.choice(["Control", "Workshop"], n)
    age = np.clip(rng.normal(21.5, 2.4, n), 17, 35)
    hours = np.clip(rng.gamma(3.0, 2.0, n), .2, 30)
    attendance = np.clip(rng.normal(78, 13, n), 20, 100)
    effect = np.where(treatment == "Workshop", 3.0, 0.0)
    group_effect = pd.Series(group).map({"A": 0, "B": 2, "C": -1}).to_numpy()
    score = np.clip(32 + 1.3 * hours + .22 * attendance + effect + group_effect + rng.normal(0, 8, n), 0, 100)
    passed = (score >= 50).astype(int)
    frame = pd.DataFrame({"student_id": np.arange(1, n + 1), "group": group,
                          "treatment": treatment, "age": age.round(1),
                          "study_hours": hours.round(2), "attendance_pct": attendance.round(1),
                          "score": score.round(2), "passed": passed})
    # Deliberately introduce 8% missing values in two predictors for the missing-data exercise.
    for col in ("study_hours", "attendance_pct"):
        frame.loc[rng.choice(n, int(.08 * n), replace=False), col] = np.nan
    DATA.mkdir(parents=True, exist_ok=True)
    frame.to_csv(DATA / "synthetic_student_outcomes.csv", index=False)
    return frame


def savefig(name: str) -> None:
    plt.tight_layout()
    plt.savefig(FIGURES / name, dpi=160, bbox_inches="tight")
    plt.close()


def run() -> dict:
    RESULTS.mkdir(parents=True, exist_ok=True); FIGURES.mkdir(parents=True, exist_ok=True)
    d = make_data(); rng = np.random.default_rng(SEED)
    out: dict[str, object] = {}
    x = d["score"].dropna()

    # 1. Measures of central tendency and dispersion
    q = x.quantile([.25, .5, .75])
    out["01_descriptive"] = {"n": int(x.size), "mean": float(x.mean()), "median": float(x.median()),
        "mode_rounded": float(x.round(0).mode().iloc[0]), "variance_sample": float(x.var()),
        "sd_sample": float(x.std()), "q1": float(q.loc[.25]), "q3": float(q.loc[.75]),
        "iqr": float(q.loc[.75]-q.loc[.25]), "range": float(x.max()-x.min())}
    plt.hist(x, bins=25, color="#4472C4", edgecolor="white"); plt.xlabel("Score"); plt.ylabel("Count"); plt.title("Synthetic score distribution"); savefig("01_score_histogram.png")
    plt.boxplot(x, orientation="horizontal"); plt.xlabel("Score"); plt.title("Score boxplot"); savefig("01_score_boxplot.png")

    # 2. Probability and conditional probability, including a reproducible simulation
    event = d["passed"].eq(1); workshop = d["treatment"].eq("Workshop")
    out["02_probability"] = {"P(pass)": float(event.mean()), "P(workshop)": float(workshop.mean()),
       "P(pass_given_workshop)": float(d.loc[workshop, "passed"].mean()),
       "P(workshop_and_pass)": float((workshop & event).mean()),
       "simulated_two_heads_2_flips": float((rng.integers(0, 2, (100000, 2)).sum(axis=1) == 2).mean())}

    # 3. Probability distributions: binomial and normal examples
    out["03_distributions"] = {"binomial_n10_p0.5_P(X=6)": float(stats.binom.pmf(6, 10, .5)),
       "binomial_n10_p0.5_P(X<=6)": float(stats.binom.cdf(6, 10, .5)),
       "normal_mu70_sigma10_P(60<X<80)": float(stats.norm.cdf(80, 70, 10)-stats.norm.cdf(60, 70, 10))}
    xx = np.linspace(35, 100, 300); plt.hist(x, bins=25, density=True, alpha=.45, label="Scores");
    plt.plot(xx, stats.norm.pdf(xx, x.mean(), x.std()), label="Fitted normal density"); plt.legend(); plt.title("Score distribution and normal reference"); savefig("03_distribution.png")

    # 4. Sampling distributions and Central Limit Theorem
    population = rng.normal(70, 12, 100000); means = np.array([rng.choice(population, 40).mean() for _ in range(2000)])
    out["04_sampling_clt"] = {"population_mean": float(population.mean()), "sample_mean_average": float(means.mean()),
        "sample_mean_sd": float(means.std(ddof=1)), "theoretical_se": float(population.std(ddof=1)/np.sqrt(40))}
    plt.hist(means, bins=30, color="#70AD47"); plt.title("Sampling distribution of mean (n=40)"); plt.xlabel("Sample mean"); savefig("04_clt.png")

    # 5. Confidence interval for mean score
    ci = stats.t.interval(.95, len(x)-1, loc=x.mean(), scale=stats.sem(x))
    out["05_confidence_interval"] = {"confidence": .95, "mean": float(x.mean()), "lower": float(ci[0]), "upper": float(ci[1])}

    # 6. Hypothesis test: workshop vs control, Welch two-sample t-test
    a = d.loc[d.treatment.eq("Workshop"), "score"]; b = d.loc[d.treatment.eq("Control"), "score"]
    tt = stats.ttest_ind(a, b, equal_var=False)
    out["06_hypothesis_test"] = {"H0": "equal population means", "H1": "different population means",
        "test": "Welch two-sample t-test", "workshop_mean": float(a.mean()), "control_mean": float(b.mean()),
        "t": float(tt.statistic), "p_value": float(tt.pvalue), "alpha": .05,
        "decision": "reject H0" if tt.pvalue < .05 else "fail to reject H0"}

    # 7. Correlation and covariance
    pair = d[["study_hours", "attendance_pct", "score"]].dropna()
    out["07_correlation_covariance"] = {"correlation": pair.corr().round(4).to_dict(), "covariance": pair.cov().round(4).to_dict()}
    plt.scatter(pair.study_hours, pair.score, alpha=.35); plt.xlabel("Study hours"); plt.ylabel("Score"); plt.title("Study hours and score"); savefig("07_correlation.png")

    # 8. Ordinary least squares regression
    reg = d.dropna(subset=["study_hours", "attendance_pct"])
    fit = smf.ols("score ~ study_hours + attendance_pct + C(treatment) + C(group)", data=reg).fit()
    out["08_linear_regression"] = {"formula": "score ~ study_hours + attendance_pct + treatment + group",
        "coefficients": fit.params.to_dict(), "p_values": fit.pvalues.to_dict(), "r_squared": float(fit.rsquared),
        "n": int(fit.nobs), "interpretation_note": "Associations in synthetic data; not causal estimates."}
    plt.scatter(fit.fittedvalues, fit.resid, alpha=.35); plt.axhline(0, color="black", lw=1); plt.xlabel("Fitted score"); plt.ylabel("Residual"); plt.title("OLS residual diagnostic"); savefig("08_regression_residuals.png")

    # 9. Matrix algebra in statistics
    X = np.column_stack([np.ones(len(reg)), reg.study_hours, reg.attendance_pct]); y = reg.score.to_numpy()
    beta = np.linalg.solve(X.T @ X, X.T @ y)
    out["09_matrix_algebra"] = {"design_shape": list(X.shape), "XTX_determinant": float(np.linalg.det(X.T@X)),
        "ols_beta_intercept_hours_attendance": beta.tolist(), "max_abs_difference_from_statsmodels": float(np.max(np.abs(beta - sm.OLS(y, X).fit().params)))}

    # 10. Eigenvalues, eigenvectors and PCA
    predictors = reg[["study_hours", "attendance_pct", "age", "score"]]
    scaled = StandardScaler().fit_transform(predictors); pca = PCA().fit(scaled)
    out["10_pca"] = {"explained_variance_ratio": pca.explained_variance_ratio_.tolist(), "components": pca.components_.tolist(),
        "eigenvalues": pca.explained_variance_.tolist()}
    plt.plot(np.arange(1, 5), np.cumsum(pca.explained_variance_ratio_), marker="o"); plt.ylim(0, 1.05); plt.xlabel("Components"); plt.ylabel("Cumulative explained variance"); plt.title("PCA scree summary"); savefig("10_pca_variance.png")

    # 11. Numerical optimization: fit a straight line by minimizing squared error
    def objective(theta): return float(np.sum((y - (theta[0] + theta[1]*reg.study_hours.to_numpy()))**2))
    opt = optimize.minimize(objective, np.array([0., 0.]), method="BFGS")
    out["11_optimization"] = {"objective": "sum of squared residuals", "intercept_slope": opt.x.tolist(),
        "minimum_sse": float(opt.fun), "converged": bool(opt.success), "message": str(opt.message)}

    # 12. Random numbers and Monte Carlo estimation
    u = rng.uniform(-1, 1, 500000); v = rng.uniform(-1, 1, 500000); inside = u*u+v*v <= 1
    out["12_monte_carlo"] = {"method": "uniform points in square [-1,1]^2", "draws": len(u),
        "pi_estimate": float(4*inside.mean()), "approx_se": float(4*np.sqrt(inside.mean()*(1-inside.mean())/len(u)))}

    # 13. Time-series analysis: synthetic monthly enrollment with trend and seasonality
    dates = pd.date_range("2021-01-01", periods=60, freq="MS"); t = np.arange(60)
    ts = pd.Series(200 + 1.8*t + 15*np.sin(2*np.pi*t/12) + rng.normal(0, 5, 60), index=dates, name="enrollment")
    ts.to_csv(RESULTS / "13_monthly_series.csv", header=True)
    ac1 = float(ts.autocorr(1)); out["13_time_series"] = {"n_months": len(ts), "mean": float(ts.mean()), "lag1_autocorrelation": ac1,
        "linear_trend_slope_per_month": float(np.polyfit(t, ts.values, 1)[0]), "note": "Synthetic series; no real forecast claims."}
    ts.plot(); plt.title("Synthetic monthly enrollment series"); plt.ylabel("Enrollment index"); savefig("13_time_series.png")

    # 14. Statistical data visualization
    points = plt.scatter(d.attendance_pct, d.score, c=d.passed, cmap="coolwarm", alpha=.4, vmin=0, vmax=1)
    colorbar = plt.colorbar(points, ticks=[0, 1]); colorbar.set_label("Generated pass status"); colorbar.set_ticklabels(["Fail", "Pass"])
    plt.xlabel("Attendance (%)"); plt.ylabel("Score"); plt.title("Score by attendance"); savefig("14_scatter.png")
    out["14_visualization"] = {"chart": "scatter plot", "scatter_observations": int(len(d)),
        "visual_encoding": "attendance vs score; color denotes generated pass status"}

    # 15. Data transformation and normalization
    raw = d["score"]; z = (raw - raw.mean())/raw.std(ddof=0); mm = (raw-raw.min())/(raw.max()-raw.min())
    out["15_transform_normalize"] = {"raw_mean_sd": [float(raw.mean()), float(raw.std(ddof=0))],
        "zscore_mean_sd": [float(z.mean()), float(z.std(ddof=0))], "minmax_range": [float(mm.min()), float(mm.max())]}
    plt.hist(raw, bins=25, alpha=.55, label="Raw score"); plt.hist(z, bins=25, alpha=.55, label="Z score"); plt.legend(); plt.title("Raw and standardized score"); savefig("15_normalization.png")

    # 16. One-way ANOVA and Tukey post-hoc comparisons
    an = smf.ols("score ~ C(group)", data=d).fit(); av = sm.stats.anova_lm(an, typ=2)
    from statsmodels.stats.multicomp import pairwise_tukeyhsd
    tukey = pairwise_tukeyhsd(d.score, d.group)
    out["16_anova"] = {"table": av.reset_index().to_dict(orient="records"), "tukey_summary": str(tukey),
        "group_means": d.groupby("group").score.mean().to_dict()}

    # 17. Chi-square test for categorical association
    tab = pd.crosstab(d.group, d.passed); chi = stats.chi2_contingency(tab, correction=False)
    out["17_chi_square"] = {"contingency_table": tab.to_dict(), "expected": chi.expected_freq.tolist(),
        "chi_square": float(chi.statistic), "df": int(chi.dof), "p_value": float(chi.pvalue)}

    # 18. Logistic regression and held-out classification summary
    features = d.dropna(subset=["study_hours", "attendance_pct"])
    XX = features[["study_hours", "attendance_pct", "age"]]; yy = features.passed
    Xtr, Xte, ytr, yte = train_test_split(XX, yy, test_size=.25, random_state=SEED, stratify=yy)
    logit = LogisticRegression(max_iter=1000).fit(Xtr, ytr); pred = logit.predict(Xte)
    out["18_logistic_regression"] = {"features": list(XX.columns), "coefficients": dict(zip(XX.columns, logit.coef_[0].tolist())),
        "intercept": float(logit.intercept_[0]), "accuracy": float(accuracy_score(yte, pred)),
        "confusion_matrix_labels_0_1": confusion_matrix(yte, pred, labels=[0,1]).tolist(), "test_n": len(yte)}

    # 19. Non-parametric method: Mann-Whitney U for two independent groups
    mw = stats.mannwhitneyu(a, b, alternative="two-sided")
    out["19_nonparametric"] = {"test": "Mann-Whitney U", "U": float(mw.statistic), "p_value": float(mw.pvalue),
        "workshop_median": float(a.median()), "control_median": float(b.median())}

    # 20. Bootstrap resampling for mean and percentile interval
    vals = x.to_numpy(); bs = np.array([rng.choice(vals, len(vals), replace=True).mean() for _ in range(2000)])
    out["20_bootstrap"] = {"resamples": len(bs), "bootstrap_mean": float(bs.mean()), "bootstrap_se": float(bs.std(ddof=1)),
        "percentile_95_interval": np.quantile(bs, [.025, .975]).tolist()}
    plt.hist(bs, bins=30, color="#ED7D31"); plt.axvline(x.mean(), color="black", label="Observed mean"); plt.legend(); plt.title("Bootstrap distribution of mean score"); savefig("20_bootstrap.png")

    # 21. Multivariate summaries, covariance, PCA scores and clustering
    Z = StandardScaler().fit_transform(predictors); p2 = PCA(n_components=2).fit_transform(Z)
    clusters = KMeans(n_clusters=3, random_state=SEED, n_init=10).fit_predict(Z)
    out["21_multivariate"] = {"covariance": predictors.cov().round(4).to_dict(), "pca2_variance_ratio": PCA(n_components=2).fit(Z).explained_variance_ratio_.tolist(),
        "cluster_sizes": pd.Series(clusters).value_counts().sort_index().to_dict()}
    plt.scatter(p2[:,0], p2[:,1], c=clusters, cmap="viridis", s=12); plt.xlabel("PC1"); plt.ylabel("PC2"); plt.title("K-means groups in first two PCs"); savefig("21_multivariate.png")

    # 22. Missing-data summary and median imputation comparison
    miss = d[["study_hours", "attendance_pct"]]; imp = SimpleImputer(strategy="median").fit_transform(miss)
    out["22_missing_data"] = {"missing_count": miss.isna().sum().to_dict(), "missing_fraction": miss.isna().mean().to_dict(),
        "method": "median imputation", "imputed_medians": dict(zip(miss.columns, SimpleImputer(strategy="median").fit(miss).statistics_.tolist())),
        "complete_case_n": int(miss.dropna().shape[0]), "imputed_n": int(len(imp)),
        "caution": "Imputation is illustrative; assumptions and sensitivity should be assessed for real data."}

    # 23. Reproducible reporting metadata
    out["23_reproducibility"] = {"random_seed": SEED, "synthetic_rows": int(len(d)),
        "python": "Python 3; see requirements.txt for package list", "data_file": "data/synthetic_student_outcomes.csv",
        "output_files": ["results/all_results.json", "results/summary.csv", "figures/*.png"],
        "synthetic_data_only": True}

    # 23. Reproducible reporting: machine-readable results and a compact report table
    (RESULTS / "all_results.json").write_text(json.dumps(out, indent=2, default=lambda o: float(o)), encoding="utf-8")
    rows = [{"topic": k, "result": json.dumps(v, default=lambda o: float(o))} for k, v in out.items()]
    pd.DataFrame(rows).to_csv(RESULTS / "summary.csv", index=False)
    return out


if __name__ == "__main__":
    results = run()
    print(f"Generated {len(results)} topic result sections.")
    print(f"Results: {RESULTS}")
