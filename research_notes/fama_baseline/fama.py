"""Fama regression baseline for USD/CNY (experiment 10, RMB track).

Specification (Fama 1984):
    dlnS_{t+h} = alpha + beta * (i_t - i*_t) + eps
where S = CNY per USD (DEXCHUS, FRED, monthly end-of-month),
i = China 1Y LPR (verified history, see lpr_history.csv),
i* = US 1Y Treasury constant maturity (DGS1, FRED, monthly end-of-month).
UIP null: beta = 1. The forward-premium puzzle is beta << 1, often < 0.

Two horizons: h = 12 months (1Y rates match the horizon) and
h = 1 month (classic Fama form; differential scaled by 1/12).
Overlapping 12m changes -> Newey-West SEs, lag 11.
All inputs are free public data; see fama_baseline.md for provenance.
"""
import csv
import math
from datetime import date

import numpy as np

BASE = "/home/hatch/workspace/research_notes/fama_baseline"


def read_fred_monthly(path, col):
    """Daily FRED csv -> monthly end-of-month series (date -> value)."""
    out = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            v = row[col].strip()
            if v == "." or v == "":
                continue
            y, m, d = (int(x) for x in row["observation_date"].split("-"))
            out[(y, m)] = float(v)  # later rows overwrite -> month-end
    return out


def read_lpr(path):
    """LPR change dates -> monthly series (step function)."""
    changes = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            y, m, d = (int(x) for x in row["date"].split("-"))
            changes.append((date(y, m, d), float(row["lpr1y"])))
    changes.sort()
    out, cur, ci = {}, None, 0
    y, m = 2019, 8
    while (y, m) <= (2026, 10):
        while ci < len(changes) and changes[ci][0] <= date(y, m, 28):
            cur = changes[ci][1]
            ci += 1
        if cur is not None:
            out[(y, m)] = cur
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def ols_hac(x, y, lags):
    """OLS with Newey-West (Bartlett) standard errors."""
    X = np.column_stack([np.ones(len(x)), x])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    u = y - X @ beta
    n, k = X.shape
    XtX_inv = np.linalg.inv(X.T @ X)
    S = X.T @ (u[:, None] ** 2 * X)
    for lag in range(1, lags + 1):
        w = 1 - lag / (lags + 1)
        for t in range(lag, n):
            S += w * (np.outer(X[t], X[t - lag]) * u[t] * u[t - lag]
                      + np.outer(X[t - lag], X[t]) * u[t - lag] * u[t])
    cov = XtX_inv @ S @ XtX_inv
    se = np.sqrt(np.diag(cov))
    resid = y - X @ beta
    r2 = 1 - (resid ** 2).sum() / ((y - y.mean()) ** 2).sum()
    return beta, se, r2, n


def months_between(a, b):
    return (b[0] - a[0]) * 12 + (b[1] - a[1])


def add_months(ym, k):
    y, m = ym
    m += k
    return (y + (m - 1) // 12, (m - 1) % 12 + 1)


def main():
    s = read_fred_monthly(f"{BASE}/dexchus.csv", "DEXCHUS")
    us1 = read_fred_monthly(f"{BASE}/dgs1.csv", "DGS1")
    cn = read_lpr(f"{BASE}/lpr_history.csv")
    months = sorted(set(s) & set(us1) & set(cn))
    print(f"sample months: {months[0]} to {months[-1]} (n={len(months)})")
    lnS = {m: math.log(s[m]) for m in months}

    # current spread, Nov 2026 (last available)
    lm = months[-1]
    print(f"latest month {lm}: LPR {cn[lm]:.2f}%, US1Y {us1[lm]:.2f}%, "
          f"diff {(cn[lm]-us1[lm])*100:+.0f}bp, USD/CNY {s[lm]:.4f}")

    for h, lag in ((12, 11), (1, 3)):
        xs, ys, used = [], [], []
        for m in months:
            m2 = add_months(m, h)
            if m2 not in lnS:
                continue
            d = (cn[m] - us1[m]) / 100.0
            if h == 1:
                d = d / 12.0
            xs.append(d)
            ys.append(lnS[m2] - lnS[m])
            used.append(m)
        x, y = np.array(xs), np.array(ys)
        beta, se, r2, n = ols_hac(x, y, lag)
        t_beta1 = (beta[1] - 1) / se[1]
        t_beta0 = beta[1] / se[1]
        corr = np.corrcoef(x, y)[0, 1]
        print(f"\nh={h}m  n={n}  {used[0]}..{used[-1]}")
        print(f"  alpha={beta[0]:+.4f} (se {se[0]:.4f})")
        print(f"  beta ={beta[1]:+.3f} (se {se[1]:.3f})  "
              f"t(beta=0)={t_beta0:+.2f}  t(beta=1)={t_beta1:+.2f}")
        print(f"  R2={r2:.3f}  corr={corr:+.3f}")
        print(f"  mean diff={x.mean()*100:+.2f}%  "
              f"mean dlnS={y.mean()*100:+.2f}%")

    # recent window descriptives (2024-01 onward, 12m horizon)
    xs, ys = [], []
    for m in months:
        if m < (2024, 1):
            continue
        m2 = add_months(m, 12)
        if m2 not in lnS:
            continue
        xs.append((cn[m] - us1[m]) / 100.0)
        ys.append(lnS[m2] - lnS[m])
    if xs:
        print(f"\n2024+ window (12m horizon): n={len(xs)} "
              f"mean diff={np.mean(xs)*100:+.2f}% "
              f"mean dlnS={np.mean(ys)*100:+.2f}% "
              f"corr={np.corrcoef(xs, ys)[0,1]:+.3f}")


if __name__ == "__main__":
    main()
