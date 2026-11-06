"""Analyze pilot results (stdlib only).

Usage:
  python3 analyze.py --in results/dictator_classic.jsonl
  python3 analyze.py --in results/ --all   # every .jsonl in the dir

Prints per-experiment summaries plus the three pass criteria from the
design doc: (1) direction matches the human baseline, (2) distribution
shape is comparable (not just the mean), (3) persona gradient exists
where theory predicts one (snow-shovel vs intervention leaning).
"""

import argparse
import glob
import json
import os
import statistics
import sys


def load(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            rows.append(json.loads(line))
    return [r for r in rows if r.get("parsed") is not None]


def summarize(path, rows=None):
    if rows is None:
        rows = load(path)
    if not rows:
        print(f"{path}: no parsed rows")
        return
    exp = rows[0]["experiment"]
    n = len(rows)
    print(f"\n== {exp} ({os.path.basename(path)}) n={n} ==")
    if exp == "dictator":
        gives = [r["parsed"]["give"] for r in rows]
        print(f"mean give={statistics.mean(gives):.1f} "
              f"median={statistics.median(gives):.0f} "
              f"pct give=0: {sum(g == 0 for g in gives) / n:.2f} "
              f"pct give=50: {sum(g == 50 for g in gives) / n:.2f}")
    elif exp == "ultimatum":
        offers = sorted({r["offer"] for r in rows})
        for o in offers:
            sub = [r for r in rows if r["offer"] == o]
            rej = sum(not r["parsed"]["accept"] for r in sub) / len(sub)
            print(f"offer={o}: n={len(sub)} rejection rate={rej:.2f}")
    elif exp == "endowment":
        for arm in ("owner", "buyer"):
            sub = [r["parsed"]["price"] for r in rows if r["arm"] == arm]
            if sub:
                print(f"{arm}: n={len(sub)} mean price={statistics.mean(sub):.1f}")
        wta = [r["parsed"]["price"] for r in rows if r["arm"] == "owner"]
        wtp = [r["parsed"]["price"] for r in rows if r["arm"] == "buyer"]
        if wta and wtp:
            print(f"WTA/WTP ratio={statistics.mean(wta) / statistics.mean(wtp):.2f}")
        ch = [r["parsed"]["choices"] for r in rows
              if r["arm"] == "chooser" and "choices" in r["parsed"]]
        if ch:
            # Implied valuation = midpoint of the bracket where the agent
            # first switches from mug to cash; never switching is censored
            # at 300 (scored 350, flagged below).
            amounts = [50, 100, 150, 200, 300]
            mids = [25, 75, 125, 175, 250, 350]
            vals, nonmono, censored = [], 0, 0
            for c in ch:
                picks = [c.get(str(a), c.get(a)) for a in amounts]
                first = next((i for i, v in enumerate(picks) if v == "cash"),
                             None)
                if first is None:
                    vals.append(350)
                    censored += 1
                else:
                    vals.append(mids[first])
                    if "mug" in picks[first + 1:]:
                        nonmono += 1
            print(f"chooser: n={len(ch)} mean implied value="
                  f"{statistics.mean(vals):.1f} median="
                  f"{statistics.median(vals):.0f} censored(>300)={censored} "
                  f"non-monotonic={nonmono}")
            for a in amounts:
                frac = sum(1 for c in ch
                           if c.get(str(a), c.get(a)) == "cash") / len(ch)
                print(f"  cash@{a}: choose cash {frac:.2f}")
    elif exp == "snow_shovel":
        unfair = sum(not r["parsed"]["fair"] for r in rows) / n
        print(f"pct unfair={unfair:.2f} (human baseline Kahneman 1986: 0.82)")
        for lean in range(1, 6):
            sub = [r for r in rows
                   if r["persona"]["intervention_leaning"] == lean]
            if sub:
                u = sum(not r["parsed"]["fair"] for r in sub) / len(sub)
                print(f"  leaning={lean} (1=pro-intervention, 5=pro-market): "
                      f"n={len(sub)} pct unfair={u:.2f}")
    elif exp == "status_quo":
        allocs = [(70, 30), (60, 40), (50, 50), (30, 70)]
        tot_sq, tot_n = 0, 0
        for sq in (70, 60, 50, 30):
            sub = [r for r in rows if r.get("sq") == sq]
            if not sub:
                continue
            sq_idx = allocs.index((sq, 100 - sq)) + 1
            p = sum(r["parsed"]["choice"] == sq_idx for r in sub) / len(sub)
            tot_sq += sum(r["parsed"]["choice"] == sq_idx for r in sub)
            tot_n += len(sub)
            print(f"  sq={sq}: n={len(sub)} pct choose SQ={p:.2f}")
        if tot_n:
            print(f"  overall pct choose SQ={tot_sq / tot_n:.2f} "
                  f"(chance baseline 0.25)")
    elif exp == "oprea":
        # Deviation sign convention: gains -> ce - EV; losses -> EV - ce
        # (ce = sure loss accepted). Fourfold predicts: gain_high <0,
        # gain_low >0, loss_high >0, loss_low <0, in both conditions.
        # Split by math-ability persona level when present.
        for math in sorted({r.get("math") or "none" for r in rows}):
            if len({r.get("math") or "none" for r in rows}) > 1:
                print(f"  [math={math}]")
            for cond in ("lottery", "mirror"):
                for cell in ("gain_high", "gain_low", "loss_high", "loss_low"):
                    sub = [r for r in rows if r.get("condition") == cond
                           and r.get("cell") == cell
                           and (r.get("math") or "none") == math]
                    if not sub:
                        continue
                    p = 0.9 if cell.endswith("high") else 0.1
                    prize = sub[0].get("prize") or 50
                    ev = prize * p
                    ces = [r["parsed"]["ce"] for r in sub]
                    if cell.startswith("gain"):
                        devs = [c - ev for c in ces]
                    else:
                        devs = [ev - c for c in ces]
                    print(f"  {cond} {cell}: n={len(sub)} EV={ev:.0f} "
                          f"mean ce={statistics.mean(ces):.1f} "
                          f"mean dev={statistics.mean(devs):+.1f}")
    elif exp == "volunteering":
        # Payoff-maximizing (modal) prediction per arm; identical in
        # both parameter sets (hauert N=5/r=3/sigma=1, semmann 6/x3.6):
        # c_dom -> D, d_dom -> L, l_dom -> C.
        predicted = {"c_dom": "D", "d_dom": "L", "l_dom": "C"}
        for pr in ("hauert", "semmann"):
            for sc in ("c_dom", "d_dom", "l_dom", "noinfo"):
                sub = [r for r in rows
                       if r.get("scenario") == sc
                       and (r.get("params") or "hauert") == pr]
                if not sub:
                    continue
                m = len(sub)
                shares = {a: sum(r["parsed"]["action"] == a for r in sub) / m
                          for a in ("C", "D", "L")}
                modal = max(shares, key=shares.get)
                pred = predicted.get(sc)
                mark = (f" predicted={pred} match={'YES' if modal == pred else 'no'}"
                        if pred else " (no-info baseline)")
                print(f"  {pr} {sc}: n={m} C={shares['C']:.2f} "
                      f"D={shares['D']:.2f} L={shares['L']:.2f} "
                      f"modal={modal}{mark}")
    elif exp == "carry":
        # Fama-consistent modal prediction: pos spread -> buy_cny,
        # inv spread -> buy_usd. High vol and controls should dampen
        # carry (more hold).
        predicted = {"pos": "buy_cny", "inv": "buy_usd"}
        for sp in ("inv", "pos"):
            for v in ("low", "high"):
                for c in ("none", "controlled"):
                    sub = [r for r in rows if r.get("spread") == sp
                           and r.get("vol") == v
                           and r.get("control") == c]
                    if not sub:
                        continue
                    m = len(sub)
                    shares = {a: sum(r["parsed"]["action"] == a for r in sub) / m
                              for a in ("buy_cny", "buy_usd", "hold")}
                    modal = max(shares, key=shares.get)
                    pred = predicted[sp]
                    print(f"  {sp} {v} {c}: n={m} buy_cny={shares['buy_cny']:.2f} "
                          f"buy_usd={shares['buy_usd']:.2f} "
                          f"hold={shares['hold']:.2f} modal={modal} "
                          f"predicted={pred} "
                          f"match={'YES' if modal == pred else 'no'}")
    elif exp == "settle":
        # Predicted: app -> higher settle_pct than dep; pos spread ->
        # higher than inv; dxy down -> higher than up.
        def mean_pct(sub):
            return statistics.mean(r["parsed"]["settle_pct"] for r in sub)
        for a in ("app", "dep"):
            for sp in ("inv", "pos"):
                for d in ("down", "up"):
                    sub = [r for r in rows if r.get("app") == a
                           and r.get("spread") == sp
                           and r.get("dxy") == d]
                    if not sub:
                        continue
                    m = len(sub)
                    shares = {t: sum(r["parsed"]["timing"] == t for r in sub) / m
                              for t in ("now", "hold", "tranche")}
                    print(f"  {a} {sp} {d}: n={m} mean_pct={mean_pct(sub):.1f} "
                          f"now={shares['now']:.2f} hold={shares['hold']:.2f} "
                          f"tranche={shares['tranche']:.2f}")
        for dim, levels in (("app", ("app", "dep")),
                            ("spread", ("pos", "inv")),
                            ("dxy", ("down", "up"))):
            hi = [r for r in rows if r.get(dim) == levels[0]]
            lo = [r for r in rows if r.get(dim) == levels[1]]
            if hi and lo:
                print(f"  effect {dim} {levels[0]}-vs-{levels[1]}: "
                      f"{mean_pct(hi):.1f} vs {mean_pct(lo):.1f} "
                      f"(diff {mean_pct(hi) - mean_pct(lo):+.1f})")
        for size in ("large", "medium", "small"):
            sub = [r for r in rows if r["persona"].get("firm_size") == size]
            if sub:
                print(f"  firm_size={size}: n={len(sub)} "
                      f"mean_pct={mean_pct(sub):.1f}")
        for risk in ("风险厌恶", "风险中性", "风险偏好"):
            sub = [r for r in rows if r["persona"].get("risk_attitude") == risk]
            if sub:
                print(f"  risk={risk}: n={len(sub)} "
                      f"mean_pct={mean_pct(sub):.1f}")
        cons = sum(
            (r["parsed"]["timing"] == "now" and r["parsed"]["settle_pct"] >= 90)
            or (r["parsed"]["timing"] == "hold"
                and r["parsed"]["settle_pct"] <= 10)
            or (r["parsed"]["timing"] == "tranche"
                and 10 < r["parsed"]["settle_pct"] < 90)
            for r in rows)
        print(f"  timing-pct consistency: {cons}/{len(rows)} = "
              f"{cons / len(rows):.2f}")
    elif exp == "fixing":
        # Two-pillar weights are identified from the balanced factorial:
        # w_close = (mean bp | close=up minus mean bp | close=down) / 80,
        # likewise w_basket. Predicted: ~0.5 each (Jermann et al. 2019).
        # Countercyclical prompt should dampen |bp|, esp. in the
        # depreciation-pressure arm (up/up).
        def mean_bp(sub):
            return statistics.mean(r["parsed"]["fixing_bp"] for r in sub)
        for c in ("up", "down"):
            for b in ("up", "down"):
                for cf in ("none", "active"):
                    sub = [r for r in rows if r.get("close") == c
                           and r.get("basket") == b
                           and r.get("cfix") == cf]
                    if not sub:
                        continue
                    m = len(sub)
                    shares = {t: sum(r["parsed"]["direction"] == t for r in sub) / m
                              for t in ("up", "down", "unchanged")}
                    print(f"  {c} {b} {cf}: n={m} mean_bp={mean_bp(sub):+.1f} "
                          f"up={shares['up']:.2f} down={shares['down']:.2f} "
                          f"unchanged={shares['unchanged']:.2f}")
        for dim, hi, lo in (("close", "up", "down"),
                            ("basket", "up", "down")):
            m_hi = mean_bp([r for r in rows if r.get(dim) == hi])
            m_lo = mean_bp([r for r in rows if r.get(dim) == lo])
            print(f"  weight {dim}: ({m_hi:+.1f} - {m_lo:+.1f}) / 80 = "
                  f"{(m_hi - m_lo) / 80:.2f} (predicted ~0.50)")
        abs_bp = lambda sub: statistics.mean(
            abs(r["parsed"]["fixing_bp"]) for r in sub)
        for cf in ("none", "active"):
            sub = [r for r in rows if r.get("cfix") == cf]
            print(f"  cfix={cf}: n={len(sub)} mean_|bp|={abs_bp(sub):.1f}")
        for c, b in (("up", "up"), ("down", "down")):
            for cf in ("none", "active"):
                sub = [r for r in rows if r.get("close") == c
                       and r.get("basket") == b and r.get("cfix") == cf]
                if sub:
                    print(f"  arm {c}/{b} cfix={cf}: mean_bp={mean_bp(sub):+.1f}")
        for risk in ("风险厌恶", "风险中性", "风险偏好"):
            sub = [r for r in rows if r["persona"].get("risk_attitude") == risk]
            if sub:
                print(f"  risk={risk}: n={len(sub)} "
                      f"mean_|bp|={abs_bp(sub):.1f}")
    elif exp == "hiring":
        for mw in ("none", "30"):
            sub = [r for r in rows if r.get("minwage") == mw]
            if not sub:
                continue
            pa = sum(r["parsed"]["hire"] == "A" for r in sub) / len(sub)
            wages = []
            for r in sub:
                eff_a = r["expask"] if mw == "none" else max(r["expask"], 30)
                eff_b = 25 if mw == "none" else 30
                wages.append(eff_a if r["parsed"]["hire"] == "A" else eff_b)
            print(f"  minwage={mw}: n={len(sub)} pct hire experienced(A)={pa:.2f} "
                  f"mean hired wage={statistics.mean(wages):.1f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()
    if args.all:
        # Group across files so multi-arm experiments (endowment owner /
        # buyer, ultimatum offers) summarize together.
        grouped = {}
        for p in sorted(glob.glob(os.path.join(args.inp, "*.jsonl"))):
            for r in load(p):
                grouped.setdefault(r["experiment"], []).append(r)
        for exp, rows in grouped.items():
            summarize(f"<all {exp}>", rows)
    else:
        summarize(args.inp)


if __name__ == "__main__":
    main()
