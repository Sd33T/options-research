"""
Reusable significance-testing toolkit for OptionOmega backtest analysis.

Generalized from the ad-hoc script used to check whether the RIC 0DTE's
VIX 20-25 bucket was a real effect (2026-09-07) — it wasn't; see
strategies/spx-ric-0dte/findings.yaml for the full writeup. That episode is
the reason this exists: a bucket looked bad, a causal story got built around
it, and only a proper significance test (plus multiple-comparison correction)
caught that it was noise from scanning 5 buckets and picking the worst one.

Use this any time a new strategy idea is "X subgroup of trades looks worse/
better than the rest." Before writing that up as a finding, run it through
here.

Usage
-----
    import pandas as pd
    from significance_testing import compare_groups, bonferroni

    df = pd.read_csv("some_backtest_export.csv")
    df.columns = [c.strip() for c in df.columns]

    group_a = df[df["SomeCondition"]]["P/L"].values
    group_b = df[~df["SomeCondition"]]["P/L"].values

    result = compare_groups(group_a, group_b, label_a="condition met",
                             label_b="condition not met")
    print(result)

    # If this comparison was one of several scanned post-hoc (e.g. one of
    # N buckets), correct before trusting any p-value:
    corrected = bonferroni([result["fisher_p"], result["permutation_p"]], n_comparisons=5)

Design notes
------------
- Win-rate comparisons use Fisher's exact test (exact, no large-sample
  assumption — appropriate for the trade counts typical of an OO export).
- Avg P/L comparisons run three ways on purpose: Welch's t-test (parametric,
  fast, but assumes near-normal residuals), Mann-Whitney U (rank-based,
  robust to skew/outliers — P/L distributions from defined-risk debit
  structures are usually right-skewed), and a permutation test (no
  distributional assumption at all, just resampling under the null). When
  these three disagree, that disagreement is itself informative — see the
  VIX 20-25 case, where the t-test and Mann-Whitney nominally cleared p<0.05
  but the permutation test didn't (p=0.07-0.09). Trust the permutation test
  over the parametric ones when P/L is skewed, which for options premium is
  most of the time.
- ALWAYS ask "was this comparison chosen after looking at the data?" before
  reporting a p-value. If a bucket/condition was picked because it looked
  like the extreme of several scanned (worst of 5 VIX buckets, best of N
  entry-time windows, etc.), that is a look-elsewhere problem and the
  p-values must be Bonferroni-corrected (or better, use a pre-registered
  hypothesis instead of scanning after the fact). This is not optional —
  it's exactly what the VIX 20-25 case got wrong the first time.
- A statistically significant result on a small n (this backtest data is
  often n<50 per bucket) can still be underpowered garbage in the other
  direction — check power_for_proportions / power_for_means before
  concluding "no effect" too. Absence of significance with low power is not
  evidence of absence.
"""

import numpy as np
from scipy import stats


def compare_groups(a, b, label_a="group A", label_b="group B", n_iter=100_000, seed=42):
    """
    Compare two arrays of per-trade P/L (or any numeric outcome).

    Returns a dict with win-rate comparison (Fisher's exact), avg-outcome
    comparison (Welch t-test, Mann-Whitney U, permutation test), and basic
    descriptive stats for both groups. Does NOT apply multiple-comparison
    correction — call bonferroni() separately once you know how many
    comparisons you're making across the whole analysis.
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    rng = np.random.default_rng(seed)

    n_a, n_b = len(a), len(b)
    wins_a, wins_b = int((a > 0).sum()), int((b > 0).sum())

    # Win rate: Fisher's exact test
    table = [[wins_a, n_a - wins_a], [wins_b, n_b - wins_b]]
    odds_ratio, fisher_p = stats.fisher_exact(table)

    # Avg outcome: permutation test (2-sided)
    obs_diff = a.mean() - b.mean()
    combined = np.concatenate([a, b])
    diffs = np.empty(n_iter)
    for i in range(n_iter):
        perm = rng.permutation(combined)
        diffs[i] = perm[:n_a].mean() - perm[n_a:].mean()
    permutation_p = float((np.abs(diffs) >= abs(obs_diff)).mean())

    # Parametric / rank-based cross-checks
    t_stat, welch_p = stats.ttest_ind(a, b, equal_var=False)
    u_stat, mannwhitney_p = stats.mannwhitneyu(a, b, alternative="two-sided")

    return {
        "label_a": label_a, "label_b": label_b,
        "n_a": n_a, "n_b": n_b,
        "win_pct_a": round(wins_a / n_a * 100, 1) if n_a else None,
        "win_pct_b": round(wins_b / n_b * 100, 1) if n_b else None,
        "fisher_odds_ratio": round(odds_ratio, 3),
        "fisher_p": round(fisher_p, 4),
        "mean_a": round(a.mean(), 2), "mean_b": round(b.mean(), 2),
        "mean_diff": round(obs_diff, 2),
        "permutation_p": round(permutation_p, 4),
        "welch_t": round(t_stat, 3), "welch_p": round(welch_p, 4),
        "mannwhitney_p": round(mannwhitney_p, 4),
    }


def omnibus_chi_square(df, group_col, outcome_bool_col):
    """
    Chi-square test of independence across >2 groups at once (e.g. all 5 VIX
    buckets simultaneously, not just the worst one vs. the rest). Run this
    BEFORE drilling into any single bucket — if the omnibus test doesn't
    reject independence, a significant-looking single-bucket comparison is
    very likely to be a look-elsewhere false positive.
    """
    import pandas as pd
    ct = pd.crosstab(df[group_col], df[outcome_bool_col])
    chi2, p, dof, expected = stats.chi2_contingency(ct)
    return {"chi2": round(chi2, 3), "dof": dof, "p": round(p, 4), "contingency_table": ct,
            "expected_counts": expected,
            "note": "Low expected cell counts (<5) make this unreliable; prefer Fisher's exact "
                    "pairwise tests in that case."}


def bonferroni(p_values, n_comparisons=None):
    """
    Bonferroni-correct a list of p-values. n_comparisons defaults to
    len(p_values) but should be set explicitly to the TOTAL number of
    comparisons scanned (e.g. 5, if you looked at 5 VIX buckets and are only
    now reporting the p-value for the worst-looking one).
    """
    n = n_comparisons or len(p_values)
    return [min(p * n, 1.0) for p in p_values]


def power_for_proportions(p1, p2, n1, ratio=1.0, alpha=0.05):
    """
    Statistical power to detect a difference between two proportions
    (e.g. win rates) given the actual sample sizes observed. Use this to
    sanity-check a "no significant difference" conclusion — if power is
    low (<0.5-0.6), the honest read is "underpowered to tell," not "no
    effect."
    """
    from statsmodels.stats.power import NormalIndPower
    from statsmodels.stats.proportion import proportion_effectsize
    effect = proportion_effectsize(p1, p2)
    power = NormalIndPower().power(effect_size=effect, nobs1=n1, ratio=ratio, alpha=alpha)
    return {"effect_size_h": round(effect, 3), "power": round(power, 3)}


if __name__ == "__main__":
    print(__doc__)
