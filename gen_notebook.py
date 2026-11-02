#!/usr/bin/env python3
"""Generate lexsi_finetune.ipynb (Colab) for the CollapseWatch regrounded build.

Run this on the VM to (re)generate the notebook. The notebook itself is
executed on Google Colab free tier, never on this VM.
"""
import json

W = "workspace"
NB = {"nbformat": 4, "nbformat_minor": 5, "metadata": {}, "cells": []}


def md(source):
    NB["cells"].append(
        {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(keepends=True)}
    )


def code(source):
    NB["cells"].append(
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": source.splitlines(keepends=True),
        }
    )


md(
    """# CollapseWatch regrounded — raw-vs-gated Tiny Aya fine-tune (Lexsi Track A)

Lexsi AI Safety & Alignment Hackathon, Fine-tuning and Data Curation track,
problem statement #2 ("Replacing a closed-model API").

This notebook fine-tunes **CohereLabs/tiny-aya-base** twice with the **same
model, same AlignTune recipe, same budget (5,000 rows, seed 42)**: once on
the raw dolly-15k slice, once on the CollapseWatch-gated slice. AuditKIT
then evaluates both on the same held-out suites (MMLU, HellaSwag,
ARC-Challenge) plus a local safety-refusal set, producing the
before/after tables for the paper.

**Run order:** cells top to bottom. One run = raw train, then gated train,
then evals. Do NOT run it twice; the fine-tune is the experiment.

**Prerequisites (uploaded from the build workspace
`~/workspace/hackathons/lexsi-collapsewatch/`):**
`finetune_raw_5k.jsonl`, `finetune_gated_5k.jsonl`, `aligntune_sft_raw.yaml`,
`aligntune_sft_gated.yaml`, `run_evals.sh`, `auditkit_eval.yaml`.
"""
)

code("!nvidia-smi")

code(
    """!pip install -q curatorkit aligntune auditkit datasets huggingface_hub tensorboard
print("toolkits installed")"""
)

md(
    """## 1. Upload the build workspace files

Upload these five files from
`~/workspace/hackathons/lexsi-collapsewatch/` on the build machine:
`finetune_raw_5k.jsonl`, `finetune_gated_5k.jsonl`, `aligntune_sft_raw.yaml`,
`aligntune_sft_gated.yaml`, `run_evals.sh`.
"""
)

code(
    """from google.colab import files
uploaded = files.upload()
print("uploaded:", sorted(uploaded.keys()))"""
)

md(
    """## 2. Push the two slices to Hugging Face (datasets)

The event requires models, adapters, logs, and datasets on Hugging Face.
Set your HF username below. Nothing is pushed from the build VM; all HF
traffic happens here on Colab.
"""
)

code(
    """HF_USER = "YOUR_HF_USERNAME"  # <-- set this
assert HF_USER != "YOUR_HF_USERNAME", "set HF_USER first"

from datasets import Dataset
import json

def push_slice(local_path, repo_name):
    rows = []
    with open(local_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    ds = Dataset.from_list(rows)
    ds.push_to_hub(f"{HF_USER}/{repo_name}", private=False)
    print(repo_name, "->", len(ds), "rows")

push_slice("finetune_raw_5k.jsonl", "lexsi-collapsewatch-dolly-raw-5k")
push_slice("finetune_gated_5k.jsonl", "lexsi-collapsewatch-dolly-gated-5k")"""
)

md(
    """## 3. Point the two recipes at your HF datasets

The recipes in the repo use `<HF_USER>` as a placeholder. This fills in
your username in both, keeping the two recipes identical in every other
field (same model, same hyperparameters, same budget).
"""
)

code(
    """import subprocess
for name in ["aligntune_sft_raw.yaml", "aligntune_sft_gated.yaml"]:
    text = open(name).read().replace("<HF_USER>", HF_USER)
    open(name, "w").write(text)
    print("patched", name)
# sanity: the only intended differences are dataset, run_name, output_dir
out = subprocess.run(
    ["diff", "aligntune_sft_raw.yaml", "aligntune_sft_gated.yaml"],
    capture_output=True, text=True,
)
print(out.stdout)"""
)

md(
    """## 4. Fine-tune run 1: RAW slice

`CohereLabs/tiny-aya-base`, LoRA r=32, 1 epoch, 160 steps, batch 4 x 8
accumulation, lr 1e-4, seed 42, bf16. Expect roughly 30-60 minutes on a
Colab T4. If the runtime disconnects, re-run from cell 1 of section 3
(the train resumes nothing; a fresh start is the clean experiment).
"""
)

code("!aligntune train --config aligntune_sft_raw.yaml 2>&1 | tee train_raw.log")

md("## 5. Fine-tune run 2: GATED slice (identical recipe)")

code("!aligntune train --config aligntune_sft_gated.yaml 2>&1 | tee train_gated.log")

md(
    """## 6. Publish adapters and logs to Hugging Face

Push the two LoRA adapter directories plus the training logs. Use your
own repo names; keep them public so the judges and the paper's
reproducibility section can link them.
"""
)

code(
    """from huggingface_hub import HfApi
api = HfApi()

api.create_repo(f"{HF_USER}/collapsewatch-raw-tinyaya", exist_ok=True)
api.upload_folder(
    folder_path="output/collapsewatch_raw",
    repo_id=f"{HF_USER}/collapsewatch-raw-tinyaya",
)
api.create_repo(f"{HF_USER}/collapsewatch-gated-tinyaya", exist_ok=True)
api.upload_folder(
    folder_path="output/collapsewatch_gated",
    repo_id=f"{HF_USER}/collapsewatch-gated-tinyaya",
)
print("adapters + logs published")"""
)

md(
    """## 7. Assemble the safety-refusal prompt set

Build `safety_prompts.csv` (one column: `prompt`) from a public
harmful-prompt evaluation release (e.g. the HEx-PHI or HarmBench public
release on the Hub). Record the exact source and row count in the cell
output below; the paper cites that number. Do not hand-write prompts.
"""
)

code(
    """# Example assembly (adjust to the release you use):
# from datasets import load_dataset
# ds = load_dataset("<public-safety-release>")
# ... select the harmful-prompt column, write safety_prompts.csv ...
SAFETY_SOURCE = "FILL IN: exact dataset id + revision"
SAFETY_ROWS = "FILL IN: row count"
print("safety source:", SAFETY_SOURCE)
print("safety rows:", SAFETY_ROWS)
import os
print("safety_prompts.csv exists:", os.path.exists("safety_prompts.csv"))"""
)

md(
    """## 8. Run the AuditKIT evals (base, raw, gated)

`run_evals.sh` evaluates all three checkpoints on MMLU, HellaSwag, and
ARC-Challenge (5-shot, temperature 0, seed 42, 1,000 items each) plus the
local safety-refusal CSV. Results land in `eval_results/`.
"""
)

code(
    """import os, subprocess
os.chmod("run_evals.sh", 0o755)
env = dict(
    os.environ,
    BASE_MODEL="CohereLabs/tiny-aya-base",
    RAW_MODEL=f"{HF_USER}/collapsewatch-raw-tinyaya",
    GATED_MODEL=f"{HF_USER}/collapsewatch-gated-tinyaya",
    OUT_DIR="eval_results",
)
subprocess.run(["bash", "run_evals.sh"], env=env, check=False)
print(sorted(os.listdir("eval_results")))"""
)

md(
    """## 9. Record the results

Copy the numbers from `eval_results/*.md` into the paper's Results
section (`PAPER.md`, tables marked TBD). Also paste:

- exact fine-tune wall-clock time per run (from the logs),
- the safety prompt source + row count recorded in section 7,
- links to the two dataset repos and the two adapter repos.

Then Ash records the demo video (3 minutes max) and the submission goes
in end of day Nov 14.
"""
)

with open("lexsi_finetune.ipynb", "w") as f:
    json.dump(NB, f, indent=1)
print("wrote lexsi_finetune.ipynb with", len(NB["cells"]), "cells")
