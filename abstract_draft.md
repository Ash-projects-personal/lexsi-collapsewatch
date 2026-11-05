# Submission abstract — DRAFT (2026-11-04)

**Status: DRAFT. Fine-tune result claims are marked [TBD] and stay empty
until the Colab run completes. Word budget: <500 (draft body ~180 words
excluding the TBD block).**

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

[TBD — fill after Colab run: MMLU / HellaSwag / ARC-Challenge deltas
(gated − raw), safety-refusal deltas, train perplexity, and an ROI sketch
of Tiny Aya vs a closed-model API on the same task mix.]

Code, configs, paper draft, and the Colab notebook are public and fully
reproducible (seed 42 everywhere); models, adapters, logs, and datasets
ship as two public Hugging Face collections.
