"""Runner for the behavioral validation pilot. Stdlib only.

Real calls use the DeepSeek OpenAI-compatible endpoint:
  POST https://api.deepseek.com/v1/chat/completions

Authentication goes through the registered connection `custom.deepseek`:
the helper below attaches a surrogate that Muse swaps for the real
credential on an approved request to api.deepseek.com. No key is ever
read from the environment, written to a file, or printed; only the model
name and temperature are logged.

Usage:
  python3 run.py --dry-run --n 8            # no API call, parser smoke test
  python3 run.py --experiment dictator --n 200 --variant classic
  python3 run.py --experiment endowment --n 200 --arm owner
  python3 run.py --experiment ultimatum --n 200 --offer 20
"""

import argparse
import json
import os
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from personas import sample_personas, persona_text  # noqa: E402
from experiments import EXPERIMENTS  # noqa: E402

PROVIDERS = {
    "deepseek": {
        "url": "https://api.deepseek.com/v1/chat/completions",
        "connector": "custom.deepseek",
        "hosts": ["api.deepseek.com"],
        "default_model": "deepseek-chat",
    },
    "gemini": {
        "url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
        "connector": "custom.gemini",
        "hosts": ["generativelanguage.googleapis.com"],
        "default_model": "gemini-3.8-flash",
    },
}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise RuntimeError("redirect refused, verify the endpoint")


def call_model(prompt, model, temperature, provider, timeout=120):
    cfg = PROVIDERS[provider]
    sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
    from dynamic_credentials import add_surrogate_to_request
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
    }).encode("utf-8")
    req = urllib.request.Request(
        cfg["url"], data=body,
        headers={"Content-Type": "application/json"})
    add_surrogate_to_request(req, cfg["connector"],
                             allowed_hosts=cfg["hosts"])
    opener = urllib.request.build_opener(NoRedirect())
    with opener.open(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def call_with_retry(prompt, model, temperature, provider, attempts=3):
    """Call once, retrying transient errors (429/5xx/network) with
    backoff. Returns "" if all attempts fail, so one bad call costs
    one record instead of killing a multi-hour run."""
    last_err = None
    for i in range(attempts):
        try:
            return call_model(prompt, model, temperature, provider)
        except Exception as e:  # noqa: BLE001 - retried, then counted
            last_err = e
            time.sleep(2 * (2 ** i))
    sys.stderr.write(f"call failed after {attempts} attempts: {last_err}\n")
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--experiment", default="dictator",
                    choices=list(EXPERIMENTS))
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--variant", default="classic",
                    choices=["classic", "novel", "adversarial", "noanchor"])
    ap.add_argument("--arm", default="owner",
                    choices=["owner", "buyer", "chooser"])
    ap.add_argument("--offer", type=int, default=20)
    ap.add_argument("--sq", default="60", choices=["70", "60", "50", "30"])
    ap.add_argument("--cell", default="gain_high",
                    choices=["gain_high", "gain_low", "loss_high", "loss_low"])
    ap.add_argument("--condition", default="lottery",
                    choices=["lottery", "mirror"])
    ap.add_argument("--minwage", default="none", choices=["none", "30"])
    ap.add_argument("--expask", default="26", choices=["26", "30", "34"])
    ap.add_argument("--scenario", default="c_dom",
                    choices=["c_dom", "d_dom", "l_dom", "noinfo"])
    ap.add_argument("--params", default="hauert",
                    choices=["hauert", "semmann"])
    ap.add_argument("--spread", default="inv", choices=["inv", "pos"])
    ap.add_argument("--app", default="app", choices=["app", "dep"])
    ap.add_argument("--dxy", default="down", choices=["down", "up"])
    ap.add_argument("--close", default="up", choices=["up", "down"])
    ap.add_argument("--basket", default="up", choices=["up", "down"])
    ap.add_argument("--cfix", default="none", choices=["none", "active"])
    ap.add_argument("--vol", default="low", choices=["low", "high"])
    ap.add_argument("--control", default="none",
                    choices=["none", "controlled"])
    ap.add_argument("--provider", default="deepseek",
                    choices=list(PROVIDERS))
    ap.add_argument("--model", default=None,
                    help="default: provider default model")
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--seed", type=int, default=20261105)
    ap.add_argument("--math", default="none", choices=["none", "strong", "weak"],
                    help="math-ability persona clause appended to the "
                         "persona text (Oprea mirror test)")
    ap.add_argument("--prize", type=int, default=50,
                    help="prize amount in yuan for the Oprea experiment "
                         "(default 50; 47 makes the EV non-integer)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--workers", type=int, default=1,
                    help="concurrent API calls (default 1 = sequential). "
                         "Safe: prompts are independent and results are "
                         "written back in persona order.")
    ap.add_argument("--out", default=None)
    ap.add_argument("--results-dir", default="results")
    args = ap.parse_args()
    if args.model is None:
        args.model = PROVIDERS[args.provider]["default_model"]

    spec = EXPERIMENTS[args.experiment]
    personas = sample_personas(args.n, seed=args.seed)
    suffix = f"_{args.variant}"
    if args.experiment == "endowment":
        suffix += f"_{args.arm}"
    if args.experiment == "ultimatum":
        suffix += f"_offer{args.offer}"
    if args.experiment == "status_quo":
        suffix += f"_sq{args.sq}"
    if args.experiment == "oprea":
        suffix += f"_{args.condition}_{args.cell}"
    if args.experiment == "hiring":
        suffix += f"_min{args.minwage}_exp{args.expask}"
    if args.experiment == "volunteering":
        suffix += f"_{args.params}_{args.scenario}"
    if args.experiment == "carry":
        suffix += f"_{args.spread}_{args.vol}_{args.control}"
    if args.experiment == "settle":
        suffix += f"_{args.app}_{args.spread}_{args.dxy}"
    if args.experiment == "fixing":
        suffix += f"_{args.close}_{args.basket}_{args.cfix}"
    if args.math != "none":
        suffix += f"_math{args.math}"
    if args.experiment == "oprea" and args.prize != 50:
        suffix += f"_prize{args.prize}"
    out_path = args.out or os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        args.results_dir, f"{args.experiment}{suffix}.jsonl")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    def run_one(p):
        kw = {}
        if args.experiment == "ultimatum":
            kw["offer"] = args.offer
        if args.experiment == "endowment":
            kw["arm"] = args.arm
        if args.experiment == "status_quo":
            kw["sq"] = int(args.sq)
        if args.experiment == "oprea":
            kw["cell"] = args.cell
            kw["condition"] = args.condition
            kw["prize"] = args.prize
        if args.experiment == "hiring":
            kw["minwage"] = args.minwage
            kw["expask"] = int(args.expask)
        if args.experiment == "volunteering":
            kw["scenario"] = args.scenario
            kw["params"] = args.params
        if args.experiment == "carry":
            kw["spread"] = args.spread
            kw["vol"] = args.vol
            kw["control"] = args.control
        if args.experiment == "settle":
            kw["spread"] = args.spread
            kw["app"] = args.app
            kw["dxy"] = args.dxy
            kw["firm_size"] = p["firm_size"]
        if args.experiment == "fixing":
            kw["close"] = args.close
            kw["basket"] = args.basket
            kw["control"] = args.cfix
        prompt = spec["prompt"](persona_text(p, math=args.math),
                               variant=args.variant, **kw)
        if args.dry_run:
            key = ("sample_" + args.arm if args.experiment == "endowment"
                   else "sample")
            response = spec.get(key, spec["sample"])
        else:
            response = call_with_retry(prompt, args.model, args.temperature,
                                       args.provider)
        return {
            "experiment": args.experiment,
            "variant": args.variant,
            "persona": p,
            "offer": args.offer if args.experiment == "ultimatum" else None,
            "arm": args.arm if args.experiment == "endowment" else None,
            "sq": int(args.sq) if args.experiment == "status_quo" else None,
            "cell": args.cell if args.experiment == "oprea" else None,
            "condition": args.condition if args.experiment == "oprea" else None,
            "minwage": args.minwage if args.experiment == "hiring" else None,
            "expask": int(args.expask) if args.experiment == "hiring" else None,
            "scenario": args.scenario if args.experiment == "volunteering" else None,
            "params": args.params if args.experiment == "volunteering" else None,
            "spread": args.spread if args.experiment in ("carry", "settle")
                      else None,
            "vol": args.vol if args.experiment == "carry" else None,
            "control": args.control if args.experiment == "carry" else None,
            "app": args.app if args.experiment == "settle" else None,
            "dxy": args.dxy if args.experiment == "settle" else None,
            "close": args.close if args.experiment == "fixing" else None,
            "basket": args.basket if args.experiment == "fixing" else None,
            "cfix": args.cfix if args.experiment == "fixing" else None,
            "math": args.math,
            "prize": args.prize if args.experiment == "oprea" else None,
            "provider": args.provider,
            "model": args.model,
            "temperature": args.temperature,
            "parsed": spec["parse"](response),
            "response": response,
            "dry_run": args.dry_run,
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }

    if args.workers and args.workers > 1:
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(
                max_workers=args.workers) as ex:
            records = list(ex.map(run_one, personas))
    else:
        records = [run_one(p) for p in personas]
    n_ok = sum(r["parsed"] is not None for r in records)
    n_fail = len(records) - n_ok
    with open(out_path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"wrote {out_path}: parsed_ok={n_ok} parse_fail={n_fail}")


if __name__ == "__main__":
    main()
