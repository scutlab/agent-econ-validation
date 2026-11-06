"""Top-up for the Gemini prize-47 mirror loss_low rows that failed
with HTTP 429. Re-runs ONLY the rows whose `parsed` is null, using
the persona stored in each row, and writes the results back into
the same file in place (order and the good rows untouched).

Usage: python3 topup_gemini_prize47.py [--gap SECONDS]
Default gap is 2 s; after a 429 the gap should be widened (6-10 s)
instead of retrying at the same interval.

Failed calls log the full HTTP status, response body, timestamp and
row index to topup_errors.log beside the output file, so the quota
that was hit can be identified later (status alone does not say
whether it is a per-minute limit or a daily quota).
"""
import argparse
import json
import time
import urllib.error

from personas import persona_text
from experiments import EXPERIMENTS
from run import call_model

PATH = ("results_gemini_oprea_prize47/"
        "oprea_classic_mirror_loss_low_prize47.jsonl")
ERR_LOG = "results_gemini_oprea_prize47/topup_errors.log"
MODEL = "gemini-3.8-flash"


def call_with_log(prompt, row_idx, attempts=3):
    """Call once, retrying transient errors with backoff. Logs the
    full error (status, body, timestamp, row) on every failure and
    returns "" if all attempts fail."""
    last_err = None
    for i in range(attempts):
        try:
            return call_model(prompt, MODEL, 1.0, "gemini")
        except urllib.error.HTTPError as e:
            try:
                body = e.read().decode("utf-8", "replace")[:2000]
            except Exception:
                body = "<unreadable>"
            last_err = f"HTTP {e.code}: {body}"
        except Exception as e:  # noqa: BLE001 - retried, then counted
            last_err = repr(e)
        ts = time.strftime("%Y-%m-%dT%H:%M:%S")
        line = f"{ts} row {row_idx} attempt {i + 1}/{attempts}: {last_err}\n"
        print(line, end="", flush=True)
        with open(ERR_LOG, "a", encoding="utf-8") as f:
            f.write(line)
        time.sleep(2 * (2 ** i))
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gap", type=float, default=2,
                    help="seconds between calls (widen after a 429)")
    args = ap.parse_args()
    with open(PATH, encoding="utf-8") as f:
        rows = [json.loads(line) for line in f]
    missing = [i for i, r in enumerate(rows) if r.get("parsed") is None]
    print(f"total rows: {len(rows)}, missing: {len(missing)}, "
          f"gap: {args.gap}s")
    spec = EXPERIMENTS["oprea"]
    for k, i in enumerate(missing):
        r = rows[i]
        prompt = spec["prompt"](persona_text(r["persona"], math="none"),
                                variant="classic", cell="loss_low",
                                condition="mirror", prize=47)
        resp = call_with_log(prompt, i)
        r["response"] = resp
        r["parsed"] = spec["parse"](resp)
        r["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        print(f"[{k + 1}/{len(missing)}] row {i} -> {r['parsed']}",
              flush=True)
        time.sleep(args.gap)
    with open(PATH, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    n_ok = sum(r["parsed"] is not None for r in rows)
    print(f"done: parsed_ok={n_ok} parse_fail={len(rows) - n_ok} "
          f"(gap {args.gap}s)")


if __name__ == "__main__":
    main()
