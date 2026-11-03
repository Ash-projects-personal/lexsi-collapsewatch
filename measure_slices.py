#!/usr/bin/env python3
"""CollapseWatch — internal-consistency measurement, finetune slices.

Lexsi Hackathon Track A. Build-window code, written 2026-11-02.

Compares the SAME five CollapseWatch metrics on the two deterministic
5,000-row fine-tune slices exported by curator_pipeline.py (seed 42):

  finetune_raw_5k.jsonl   - CuratorKIT-curated train split, no collapse gate
  finetune_gated_5k.jsonl - CuratorKIT-curated train split + CollapseWatch gate

Answers the question: does the gated slice show lower collapse markers
than the raw slice at the same row budget? No model training, no HF
traffic, no synthetic data. Numbers are whatever metrics.measure says.

Output (in this directory):
  collapse_slices_5k.json  raw vs gated metric comparison
"""

import json
import os
import sys

SYS_LIB = os.path.expanduser("~/workspace/hackathons/collapsewatch")
if SYS_LIB not in sys.path:
    sys.path.insert(0, SYS_LIB)

from collapsewatch import metrics  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def load_jsonl(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                obj = json.loads(line)
                rows.append({"prompt": obj["prompt"], "response": obj["response"]})
    return rows


SLIM_KEYS = [
    "rows",
    "exact_dup_rows",
    "exact_dup_rate",
    "near_dup_rows",
    "near_dup_rate",
    "template_clusters",
    "top1_template_share",
    "top3_template_share",
    "vocab_top50_coverage",
    "type_token_ratio",
    "answer_repetition",
    "length_modal_share",
    "length_modal_bucket_tokens",
]


def main():
    raw = load_jsonl(os.path.join(HERE, "finetune_raw_5k.jsonl"))
    gated = load_jsonl(os.path.join(HERE, "finetune_gated_5k.jsonl"))
    print("raw rows:", len(raw), "| gated rows:", len(gated))

    m_raw = metrics.measure(raw)
    m_gated = metrics.measure(gated)

    slim_raw = {k: m_raw[k] for k in SLIM_KEYS}
    slim_gated = {k: m_gated[k] for k in SLIM_KEYS}
    slim_raw["response_length_mean"] = m_raw["response_length"]["mean"]
    slim_gated["response_length_mean"] = m_gated["response_length"]["mean"]

    comparison = {
        "generated": "2026-11-02",
        "seed": 42,
        "raw_slice": {"path": "finetune_raw_5k.jsonl", "metrics": slim_raw},
        "gated_slice": {"path": "finetune_gated_5k.jsonl", "metrics": slim_gated},
    }
    out = os.path.join(HERE, "collapse_slices_5k.json")
    with open(out, "w") as f:
        json.dump(comparison, f, indent=2, ensure_ascii=False)

    fmt = "| {k:38s} | {r:>12} | {g:>12} |"
    print(fmt.format(k="metric", r="raw 5k", g="gated 5k"))
    for k in SLIM_KEYS + ["response_length_mean"]:
        print(fmt.format(k=k, r=str(slim_raw[k]), g=str(slim_gated[k])))
    print("wrote", out)


if __name__ == "__main__":
    main()
