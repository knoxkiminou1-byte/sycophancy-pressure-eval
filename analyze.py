#!/usr/bin/env python3
"""Reproduce all statistics in this repo's README/WRITEUP from the raw trial data.

Usage: python analyze.py
Reads:  data/raw/trials.json
Writes: data/processed/results.json, web/results.json (for the dashboard)
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).parent
RAW = ROOT / "data" / "raw" / "trials.json"
OUT_PROCESSED = ROOT / "data" / "processed" / "results.json"
OUT_WEB = ROOT / "web" / "results.json"


def wilson_interval(successes: int, n: int, z: float = 1.96):
    if n == 0:
        return (0.0, 0.0)
    p = successes / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    margin = (z / denom) * math.sqrt((p * (1 - p) / n) + (z**2 / (4 * n**2)))
    lo = max(0.0, center - margin)
    hi = min(1.0, center + margin)
    return (lo, hi)


def summarize(trials, key_fn):
    groups = {}
    for t in trials:
        groups.setdefault(key_fn(t), []).append(t)
    out = {}
    for k, ts in groups.items():
        n = len(ts)
        flips = sum(1 for t in ts if t["flip"])
        lo, hi = wilson_interval(flips, n)
        out[k] = {
            "n": n,
            "flips": flips,
            "flip_rate": flips / n,
            "flip_rate_ci95": [round(lo, 4), round(hi, 4)],
        }
    return out


def main():
    data = json.loads(RAW.read_text())
    trials = data["trials"]

    overall = summarize(trials, lambda t: "overall")["overall"]
    by_probe = summarize(trials, lambda t: t["probe_type"])
    by_model = summarize(trials, lambda t: t["model"])
    by_model_probe = summarize(trials, lambda t: f"{t['model']}__{t['probe_type']}")

    results = {
        "n_total_trials": len(trials),
        "overall": overall,
        "by_probe_type": by_probe,
        "by_model": by_model,
        "by_model_and_probe": by_model_probe,
        "trials": trials,
    }

    OUT_PROCESSED.parent.mkdir(parents=True, exist_ok=True)
    OUT_WEB.parent.mkdir(parents=True, exist_ok=True)
    OUT_PROCESSED.write_text(json.dumps(results, indent=2))
    OUT_WEB.write_text(json.dumps(results, indent=2))

    print(f"Total trials: {results['n_total_trials']}")
    print(f"Overall flip rate: {overall['flip_rate']*100:.1f}% "
          f"(95% CI: {overall['flip_rate_ci95'][0]*100:.1f}%-{overall['flip_rate_ci95'][1]*100:.1f}%)")
    print("\nBy probe type:")
    for k, v in by_probe.items():
        print(f"  {k}: {v['flips']}/{v['n']} flips, 95% CI upper bound {v['flip_rate_ci95'][1]*100:.1f}%")
    print(f"\nWrote {OUT_PROCESSED} and {OUT_WEB}")


if __name__ == "__main__":
    main()
