#!/usr/bin/env python3
"""CollapseWatch regrounded — Stage 1: CuratorKIT curation + collapse gate.

Lexsi Hackathon Track A, problem statement #2. Build-window code,
written 2026-11-01.

Chain: local dolly-15k parquet
  -> dolly_raw.jsonl (alpaca format, instruction/input/output)
  -> CuratorKIT (schema gate, exact + minhash dedup, 90/10 train/eval split)
  -> CollapseWatch gate (fix.fix_rows: exact drops, near-dup drops at
     5-gram Jaccard >= 0.8, template cap at 10% of rows)
  -> gated slices for the fine-tune comparison:
     finetune_raw_5k.jsonl vs finetune_gated_5k.jsonl (seed 42, same budget)

The pipeline records one JSON manifest with every number so the paper
can cite the exact row counts at each stage. Uses only files already on
disk; no Hub access.

Usage:
    <venv-python> curator_pipeline.py
"""

import glob
import json
import os
import random
import subprocess
import sys

SYS_LIB = os.path.expanduser("~/workspace/hackathons/collapsewatch")
if SYS_LIB not in sys.path:
    sys.path.insert(0, SYS_LIB)

from collapsewatch import fix  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DOLLY_PARQUET = os.path.expanduser(
    "~/workspace/goals/free-ai-hackathon-wins/hidden_files/lexsi-prep/datasets/dolly-15k.parquet"
)
VENV_PY = os.path.expanduser(
    "~/workspace/goals/free-ai-hackathon-wins/hidden_files/lexsi-prep/venv/bin/python"
)
CURATOR_OUT = os.path.join(HERE, "curator_out")
FINETUNE_BUDGET = 5000
SEED = 42
GATE_TEMPLATE_SHARE = 0.10


def dolly_to_jsonl(path):
    import pyarrow.parquet as pq

    table = pq.read_table(DOLLY_PARQUET).to_pandas()
    n = 0
    with open(path, "w", encoding="utf-8") as f:
        for _, r in table.iterrows():
            f.write(
                json.dumps(
                    {
                        "instruction": str(r["instruction"]),
                        "input": str(r["context"]) if str(r["context"]).strip() else "",
                        "output": str(r["response"]),
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            n += 1
    return n


def read_alpaca(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            prompt = obj.get("instruction", "")
            if obj.get("input"):
                prompt = prompt + "\n\n" + obj["input"]
            rows.append({"prompt": prompt, "response": obj.get("output", "")})
    return rows


def write_rows(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    manifest = {"seed": SEED, "gate_template_share": GATE_TEMPLATE_SHARE}

    # Step 0: parquet -> JSONL (alpaca shape, local only).
    raw_jsonl = os.path.join(HERE, "dolly_raw.jsonl")
    manifest["dolly_rows"] = dolly_to_jsonl(raw_jsonl)
    print("dolly_raw.jsonl rows:", manifest["dolly_rows"])

    # Step 1: CuratorKIT curation (its own dedup; CollapseWatch is separate).
    subprocess.run(
        [
            VENV_PY,
            "-m",
            "curatorkit.cli",
            "run",
            os.path.join(HERE, "curator_config.yaml"),
            "--output-dir",
            CURATOR_OUT,
        ],
        cwd=HERE,
        check=True,
    )
    produced = sorted(glob.glob(os.path.join(CURATOR_OUT, "**", "*.jsonl"), recursive=True))
    print("CuratorKIT outputs:", produced)
    manifest["curatorkit_outputs"] = produced

    # Step 2: CollapseWatch gate on the curated train split. The exporter
    # writes sft_alpaca.jsonl under train/ and eval/ subdirectories, so
    # match on the parent directory name, not the file basename.
    train_files = [
        p
        for p in produced
        if os.path.basename(os.path.dirname(p)).lower() == "train"
        and p.endswith(".jsonl")
    ]
    curated_path = train_files[0] if train_files else produced[0]
    curated = read_alpaca(curated_path)
    manifest["curatorkit_curated_rows"] = len(curated)

    gated, gate_stats = fix.fix_rows(curated, max_template_share=GATE_TEMPLATE_SHARE)
    manifest["gate_stats"] = gate_stats
    write_rows(os.path.join(HERE, "dolly_gated.jsonl"), gated)
    print("gated rows:", len(gated), "gate stats:", gate_stats)

    # Step 3: fixed-budget fine-tune slices (raw vs gated, same budget).
    rng = random.Random(SEED)
    raw_slice = rng.sample(curated, min(FINETUNE_BUDGET, len(curated)))
    gated_slice = rng.sample(gated, min(FINETUNE_BUDGET, len(gated)))
    write_rows(os.path.join(HERE, "finetune_raw_5k.jsonl"), raw_slice)
    write_rows(os.path.join(HERE, "finetune_gated_5k.jsonl"), gated_slice)
    manifest["finetune_budget"] = FINETUNE_BUDGET
    manifest["finetune_raw_rows"] = len(raw_slice)
    manifest["finetune_gated_rows"] = len(gated_slice)

    with open(os.path.join(HERE, "pipeline_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    print("wrote pipeline_manifest.json")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
