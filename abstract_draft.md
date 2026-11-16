# Submission abstract — FINAL (2026-11-16)

**Status: FINAL. Results filled from the completed Colab run
(2026-11-16). Word count: under 500.**

---

Fine-tuning data decides what a small open-weights model learns, but
standard curation only dedups. We add a second, orthogonal curation axis:
**measured collapse risk**.

CollapseWatch computes five collapse metrics on a real instruction-tuning
corpus — exact-duplicate rate, near-duplicate rate (5-gram Jaccard ≥ 0.8),
prompt-template concentration, vocabulary narrowness, and answer
repetition inside prompt templates — and gates the training slice on
them. The gate is wired into a real four-toolkit pipeline: CuratorKIT
curates, the CollapseWatch gate filters, AlignTune fine-tunes CohereLabs
Tiny Aya (3B), AuditKIT evaluates.

On databricks-dolly-15k (15,011 human-written pairs, CC BY-SA 3.0) the
gate is deliberately conservative: it drops 35 of 15,011 rows (0.2% —
16 exact, 19 near-duplicates), the 10% template cap drops zero rows, and
clean human data passes through nearly untouched. A controlled raw-vs-
gated fine-tune (same model, same AlignTune recipe, same 5,000-row
budget) then tests whether removing even that residual collapse moves
held-out capability and safety metrics.

The controlled run is done. Both fine-tunes (LoRA rank 32, 160 steps,
seed 42, fp16 on a free Colab T4) completed: raw final train loss 1.7829,
gated 1.7727. On ARC-Challenge and HellaSwag (5-shot, lm_eval, n = 100
per task), both adapters score within standard error of the base model
(ARC accuracy 0.44 base, 0.45 raw, 0.45 gated; HellaSwag identical across
all three), so removing the residual collapse cost no measured
capability. The full experiment (both trainings plus evaluation) ran on
free-tier compute, about 43 minutes of T4 training time in total, at
zero compute cost, against the per-call API pricing the same task mix
would carry on a closed model.

Code, configs, paper draft, and the Colab notebook are public and fully
reproducible (seed 42 everywhere); models, adapters, logs, and datasets
ship as public Hugging Face repos.
