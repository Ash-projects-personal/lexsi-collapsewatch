# CollapseWatch regrounded — Lexsi Track A build workspace

Build-window work for the Lexsi AI Safety & Alignment Hackathon
(Nov 1-14, 2026), Fine-tuning and Data Curation track, problem statement
#2 ("Replacing a closed-model API"). Everything here was written Nov 1-14.

**Idea.** Fine-tuning data curation needs a new axis beyond quality,
complexity, and influence: *measured collapse risk*. CollapseWatch
measures five collapse metrics on a real SFT corpus and gates the
training slice on them, wired into a real pipeline:

```
dolly-15k (local) -> CuratorKIT -> CollapseWatch gate -> AlignTune (Tiny Aya, raw vs gated) -> AuditKIT
```

CuratorKIT dedups; CollapseWatch measures collapse risk and gates on it.

**Files**

| File | What it is |
|---|---|
| `measure_dolly.py` | Collapse metrics on dolly-15k (15,011 rows) + gate; writes Table 1 |
| `collapse_dolly_full.json` | Measured metrics, full + gated (Table 1 source of truth) |
| `collapse_dolly_by_category.json` | Per-category metrics (8 categories) |
| `TABLE1_dolly.md` | Paper Table 1, Markdown |
| `curator_config.yaml` | CuratorKIT pipeline (schema gate, exact + MinHash dedup, 90/10 split) |
| `curator_pipeline.py` | Orchestrator: parquet->JSONL, CuratorKIT run, collapse gate, 5k slices, manifest |
| `pipeline_manifest.json` | Row counts at every pipeline stage |
| `aligntune_sft_raw.yaml` / `aligntune_sft_gated.yaml` | Identical SFT recipes (raw vs gated arms) |
| `auditkit_eval.yaml` | Eval config (MMLU, HellaSwag, ARC-Challenge + safety) |
| `run_evals.sh` | Runs AuditKIT on base / raw / gated checkpoints |
| `gen_notebook.py` | Generates the Colab notebook |
| `lexsi_finetune.ipynb` | Colab notebook: installs toolkits, trains both arms, evals, pushes to HF |
| `PAPER.md` | Paper draft (intro/method/data/results-so-far; results TBD after fine-tune) |
| `SUBMISSION_CHECKLIST.md` | Every Lexsi requirement and its status |

**Measured today (real data, dolly-15k):** 16 exact-duplicate rows (0.1%),
65 near-duplicate rows (0.4%), 8,888 template clusters, top-1 template
1.8%, vocab top-50 coverage 36.5%, answer repetition 0.002. Gate dropped
35 rows (0.2%); template cap dropped 0 (clean human data passes through).

**The Oct-27 CLI** at `~/workspace/hackathons/collapsewatch/` is imported
as a library (`sys.path`); it is not modified or copied here.
