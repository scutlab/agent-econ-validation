"""Side-by-side comparison of two providers' pilot results (stdlib only).

Usage:
  python3 compare.py --a results --b results_qwen

Loads every .jsonl in each dir (real runs only; dry-run rows are skipped),
groups by experiment, and prints DeepSeek vs Qwen summaries plus a
replication verdict per experiment. Verdicts are descriptive, not
significance tests: with n=200/agent-arm, treat small gaps as noise and
only large, systematic gaps as model-dependence evidence.
"""

import argparse
import glob
import json
import os
import statistics


def load_dir(d):
    rows = []
    for p in sorted(glob.glob(os.path.join(d, "*.jsonl"))):
        with open(p, encoding="utf-8") as f:
            for line in f:
                r = json.loads(line)
                if r.get("parsed") is not None and not r.get("dry_run"):
                    rows.append(r)
    grouped = {}
    for r in rows:
        grouped.setdefault(r["experiment"], []).append(r)
    return grouped


def s_dictator(rows):
    g = [r["parsed"]["give"] for r in rows]
    return (f"mean={statistics.mean(g):.1f} median={statistics.median(g):.0f} "
            f"pct0={sum(x == 0 for x in g) / len(g):.2f} "
            f"pct50={sum(x == 50 for x in g) / len(g):.2f}")


def s_ultimatum(rows):
    parts = []
    for o in sorted({r["offer"] for r in rows}):
        sub = [r for r in rows if r["offer"] == o]
        rej = sum(not r["parsed"]["accept"] for r in sub) / len(sub)
        parts.append(f"offer{o}: rej={rej:.2f}")
    return " ".join(parts)


def s_endowment(rows):
    wta = [r["parsed"]["price"] for r in rows if r["arm"] == "owner"]
    wtp = [r["parsed"]["price"] for r in rows if r["arm"] == "buyer"]
    if not wta or not wtp:
        return "missing an arm"
    return (f"WTA={statistics.mean(wta):.1f} WTP={statistics.mean(wtp):.1f} "
            f"ratio={statistics.mean(wta) / statistics.mean(wtp):.2f}")


def s_snow(rows):
    unfair = sum(not r["parsed"]["fair"] for r in rows) / len(rows)
    grad = []
    for lean in range(1, 6):
        sub = [r for r in rows if r["persona"]["intervention_leaning"] == lean]
        if sub:
            grad.append(sum(not r["parsed"]["fair"] for r in sub) / len(sub))
    grad_s = " ".join(f"{g:.2f}" for g in grad)
    mono = all(grad[i] >= grad[i + 1] for i in range(len(grad) - 1)) or \
        all(grad[i] <= grad[i + 1] for i in range(len(grad) - 1))
    return f"unfair={unfair:.2f} gradient(lean1..5)={grad_s} monotonic={mono}"


SUMMARIZERS = {
    "dictator": s_dictator,
    "ultimatum": s_ultimatum,
    "endowment": s_endowment,
    "snow_shovel": s_snow,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", default="results")
    ap.add_argument("--b", default="results_qwen")
    args = ap.parse_args()
    ga = load_dir(args.a)
    gb = load_dir(args.b)
    for exp in sorted(set(ga) | set(gb)):
        print(f"\n== {exp} ==")
        fn = SUMMARIZERS.get(exp)
        if fn is None:
            print("no summarizer")
            continue
        ra, rb = ga.get(exp, []), gb.get(exp, [])
        la = ra[0].get("provider", "a") if ra else "a"
        lb = rb[0].get("provider", "b") if rb else "b"
        print(f"  {la} (n={len(ra)}): {fn(ra) if ra else 'no data'}")
        print(f"  {lb} (n={len(rb)}): {fn(rb) if rb else 'no data'}")


if __name__ == "__main__":
    main()
