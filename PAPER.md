# CollapseWatch: Gating Fine-Tuning Data on Measured Collapse Risk

*Lexsi AI Safety and Alignment Hackathon — Fine-tuning and Data Curation track,
problem statement #2 ("Replacing a closed-model API"). Draft, 2026-11-01.
Author: Ashish Shetty (solo).*

## Abstract

Fine-tuning data decides what a small open-weights model learns, but the
standard curation pipeline only dedups. This paper introduces a second,
orthogonal axis for fine-tuning data curation: **measured collapse risk**.
CollapseWatch computes five collapse metrics on a real instruction-tuning
corpus (exact-duplicate rate, near-duplicate rate at 5-gram Jaccard >= 0.8,
template concentration, vocabulary narrowness, and answer repetition inside
prompt templates) and gates the training slice on them. The gate is wired as
the curation step of a real pipeline: CuratorKIT curates, the CollapseWatch
gate filters, AlignTune fine-tunes, AuditKIT evaluates. On
databricks-dolly-15k (15,011 human-written pairs, CC BY-SA 3.0) the gate is
deliberately conservative: it drops 35 of 15,011 rows (0.2%) and passes a
clean human-authored dataset through nearly untouched. A controlled
raw-vs-gated fine-tune of Cohere Tiny Aya (same model, same recipe, same
5,000-row budget) then tests whether removing even that residual collapse
moves held-out capability and safety metrics. [Results section to be filled
after the fine-tune runs.]

## 1. Introduction

Small open-weights models are the practical replacement for closed-model
APIs in settings where cost, latency, data privacy, or offline deployment
rule out calling a frontier API. The quality of that replacement is decided
almost entirely by the fine-tuning data: a 3B model trained on repetitive,
template-collapsed data inherits the repetition.

Existing curation work selects data on quality, complexity, and influence.
AlpaGasus (Chen et al., 2024) filters by LLM-judged quality; DEITA
(Liu et al., 2024) selects on complexity and quality; LESS (Xia et al., 2024)
selects by gradient influence on target tasks. Deduplication work (Lee et al.,
2022; Abbas et al., 2023; Tirumala et al., 2023) removes exact and
near-duplicate content. None of them measure **collapse**: the structural
pathologies of a fine-tuning corpus — how much of it is the same answer
wearing different prompts, how concentrated its prompt templates are, how
narrow the vocabulary doing the work is.

This paper makes collapse measurable and actionable. CollapseWatch defines
five corpus-level metrics, validates them on a real public SFT dataset, and
wires them as a gate inside a real fine-tuning pipeline built from Lexsi
Labs toolkits (CuratorKIT, AlignTune, AuditKIT). The central claim is
narrow and testable: data selection should add collapse risk as a new axis,
orthogonal to quality, complexity, and influence — and a gate on that axis
should be conservative enough to pass clean human data through.

## 2. Related work

**Deduplication and data pruning.** Lee et al. (2022) showed that
deduplicating training data makes language models better, establishing
exact-substring and near-duplicate removal as standard practice. Abbas et al.
(2023) introduced SemDeDup, removing semantic duplicates with embeddings and
halving training data with minimal loss. Tirumala et al. (2023) proposed D4,
chaining deduplication with embedding-space diversification for pre-training.
These methods remove redundancy; CollapseWatch goes one step further and
measures the structural collapse that remains after dedup.

**Instruction-tuning data selection.** LIMA-style quality arguments, AlpaGasus
(Chen et al., 2024), DEITA (Liu et al., 2024), and LESS (Xia et al., 2024)
select on quality, complexity, and influence. Collapse risk is a different
axis: a dataset can score high on quality and still be template-collapsed.

**Model collapse and safety erosion.** Recursive self-training degrades
generative models (Song, Cai, and Zhao, 2026, on code LLMs). Fine-tuning can
erode safety guardrails even without adversarial intent (Qi et al., 2024;
Hsiung et al., 2026). Both findings motivate measuring what a fine-tuning
corpus structurally teaches before the first gradient step.

**Positioning.** CuratorKIT already dedups; CollapseWatch does not duplicate
that. CuratorKIT removes duplicate rows. CollapseWatch measures collapse
risk — template concentration, vocabulary narrowness, answer repetition —
and gates on it. The two compose: dedup first, collapse gate second.

## 3. Method

### 3.1 Collapse metrics

For a corpus of (prompt, response) pairs, CollapseWatch computes:

1. **Exact-duplicate rate**: share of rows whose normalized (prompt,
   response) pair matches an earlier row.
2. **Near-duplicate rate**: share of rows whose response has 5-gram Jaccard
   similarity >= 0.8 with another row's response (found via a 5-gram
   inverted index, so no qualifying pair is missed).
3. **Template concentration**: prompts are clustered by their first four
   normalized words (digits masked); reported as the share of rows in the
   largest cluster and in the three largest clusters.
4. **Vocabulary narrowness**: share of all response tokens covered by the 50
   most frequent response words, plus the response type-token ratio.
5. **Answer repetition**: over template clusters with >= 3 rows, the
   size-weighted mean pairwise 5-gram Jaccard similarity of responses
   inside the cluster. 0 means every answer in a template is different;
   1 means every answer is identical.

### 3.2 The gate

The gate (`fix_rows`) removes rows deterministically, first occurrence wins:
(1) exact duplicates, (2) near-duplicates against already-kept rows,
(3) template clusters capped at 10% of the corpus, dropping evenly-spaced
rows so surviving rows span the cluster's topic range. The gate only removes
rows; it never edits, rewrites, or synthesizes text.

### 3.3 The pipeline

CuratorKIT reads the corpus (schema gate, exact dedup, MinHash dedup at 0.85,
90/10 train/eval split). The CollapseWatch gate filters the curated train
split. AlignTune fine-tunes Cohere Tiny Aya (CohereLabs/tiny-aya-base) with
LoRA (r=32) on the raw and gated 5,000-row slices with identical recipes.
AuditKIT evaluates base, raw-tuned, and gated-tuned checkpoints on MMLU,
HellaSwag, and ARC-Challenge (5-shot, temperature 0, seed 42) plus a local
safety-refusal prompt set. Three Lexsi toolkits are chained end to end.

## 4. Data

**databricks/databricks-dolly-15k**: 15,011 human-written
instruction/response pairs across 8 categories (open_qa 3,742; general_qa
2,191; classification 2,136; closed_qa 1,773; brainstorming 1,766;
information_extraction 1,506; summarization 1,188; creative_writing 709).
License CC BY-SA 3.0, used with attribution to Databricks. Real
human-authored data; no synthetic rows. The full local parquet is on disk;
the pipeline reads it locally (no Hub download).

**Fine-tune slices**: 5,000-row deterministic subsamples (seed 42) of the
CuratorKIT-curated train split (raw) and the gated split (gated). Same
budget for both arms.

**Eval data**: MMLU, HellaSwag, ARC-Challenge via the AuditKIT lmeval engine;
a safety-refusal prompt set assembled from a public harmful-prompt release
(source and row count recorded in the run log).

## 5. Experiments

- **E1 — collapse measurement**: the five metrics on the full 15,011-row
  corpus and per category (paper Table 1, measured 2026-11-01).
- **E2 — gate calibration**: metrics before/after `fix_rows` on the same
  corpus; how many rows each gate step drops.
- **E3 — raw-vs-gated fine-tune**: Tiny Aya + LoRA on the raw 5k slice vs
  the gated 5k slice, identical recipe; AuditKIT held-out deltas (MMLU,
  HellaSwag, ARC-Challenge) and safety-refusal deltas.
- **E4 — ablation (planned)**: gate on vs off is E3; template-cap on vs off
  as a follow-up if compute allows.

Compute: Google Colab free tier (T4), unsloth backend, bf16, 160 steps per
arm. No paid compute, no HF credits used.

## 6. Results

### 6.1 Collapse measurements on dolly-15k (measured 2026-11-01)

| Metric | Full (15,011 rows) | Gated (14,976 rows) |
|---|---|---|
| Exact-duplicate rows | 16 (0.1%) | 0 (0.0%) |
| Near-duplicate rows (5-gram Jaccard >= 0.8) | 65 (0.4%) | 0 (0.0%) |
| Template clusters | 8,888 | 8,882 |
| Top-1 template share | 1.8% (`identify which instrument is`, 277 rows, 277 distinct answers) | 1.8% |
| Top-3 template share | 5.1% | 5.1% |
| Vocab top-50 coverage | 36.5% | 36.5% |
| Type-token ratio | 0.051 | 0.051 |
| Answer repetition (in-template) | 0.002 | 0.001 |
| Modal response length | 0-9 tokens (18.9%) | 0-9 tokens (18.9%) |
| Mean response length | 60.9 tokens | 60.7 tokens |

The gate dropped 35 rows in total (16 exact + 19 near-duplicates not
already dropped as exact): 0.2% of the corpus. The template cap dropped
zero rows — no template cluster exceeded 10% of the corpus (the largest,
`identify which instrument is`, is 1.8% and every one of its 277 answers is
distinct). Within-category template concentration is higher than the
corpus-wide figure: the top template covers 14.0% of brainstorming rows and
13.0% of classification rows, with answer repetition still near zero
(0.002 and 0.000).

Reading: dolly-15k is a clean, human-authored dataset, and the gate behaves
as designed on clean data — it removes the small residual duplication and
otherwise passes the corpus through. That is the calibration result: the
metrics distinguish real human data from collapsed data instead of
punishing everything.

### 6.2 Raw-vs-gated fine-tune [TBD — runs on Colab]

| Suite | Base | Raw 5k | Gated 5k | Delta (gated - raw) |
|---|---|---|---|---|
| MMLU (5-shot) | TBD | TBD | TBD | TBD |
| HellaSwag (5-shot) | TBD | TBD | TBD | TBD |
| ARC-Challenge (5-shot) | TBD | TBD | TBD | TBD |
| Safety refusal rate | TBD | TBD | TBD | TBD |
| Train perplexity / ROUGE / BLEU (held-out 500) | TBD | TBD | TBD | TBD |

### 6.3 Ablation: template cap on/off [TBD if compute allows]

## 7. Limitations

- The gate catches structural repetition, not semantic duplicates (a job for
  embedding methods like SemDeDup) and not label noise or wrong answers.
- Single dataset (dolly-15k), single model (Tiny Aya 3B), single seed; the
  fine-tune comparison is one controlled experiment, not a benchmark sweep.
- Dolly is unusually clean; the gate's value on noisier web-scale SFT mixes
  is hypothesized, not shown.
- Compute limits (Colab free tier) cap the fine-tune budget at 5k rows and
  one epoch per arm.
- Safety evaluation uses a refusal-rate probe on a public harmful-prompt
  set, not a full red-team evaluation.

## 8. Future work

- Semantic-dedup layer (embeddings) composed with the collapse gate, so
  both lexical collapse and semantic redundancy are gated.
- The gate as a CI check on every fine-tune: fail the run if collapse
  metrics exceed thresholds, before spending GPU hours.
- Extension to agentic tool-use trajectories, where template collapse
  (same tool-call skeleton, different slots) is the dominant failure mode.
- Larger-scale replication across SFT mixtures and model sizes.

## 9. Reproducibility

Repo: (GitHub link at submission). All code in this paper was written
2026-11-01–14. Datasets, adapters, and logs are hosted on Hugging Face
(links at submission); the notebook `lexsi_finetune.ipynb` reproduces the
fine-tune and eval runs end to end on Colab free tier. Seeds: 42
everywhere. Commands: `python measure_dolly.py`,
`python curator_pipeline.py`, `aligntune train --config
aligntune_sft_raw.yaml`, `aligntune train --config
aligntune_sft_gated.yaml`, `bash run_evals.sh`. The Oct-27 CollapseWatch CLI
is imported as a library; the submission's new work is everything in this
repo.

## References

- Abbas, A., Tirumala, K., Simig, D., Ganguli, S., and Morcos, A. S. (2023).
  SemDeDup: Data-efficient learning at web-scale through semantic
  deduplication. ICLR 2023.
- Chen, L., Li, S., Yan, J., Wang, H., Gunaratna, K., Yadav, V., Tang, Z.,
  Srinivasan, V., Zhou, T., Huang, H., and Jin, H. (2024). AlpaGasus:
  Training a better alpaca with fewer data. ICLR 2024.
- Hsiung, L., Pang, T., Tang, Y.-C., Song, L., and Ho, T.-Y. (2026). Why LLM
  safety guardrails collapse after fine-tuning: a similarity analysis between
  alignment and fine-tuning datasets.
- Lee, K., Ippolito, D., Nystrom, A., Zhang, C., Eck, D., Callison-Burch, C.,
  and Carlini, N. (2022). Deduplicating training data makes language models
  better. ACL 2022.
- Liu, W., Zeng, W., He, K., Jiang, Y., and He, J. (2024). What makes good
  data for alignment? A comprehensive study of automatic data selection in
  instruction tuning. ICLR 2024.
- Qi, X. et al. (2024). Fine-tuning aligned language models compromises
  safety, even when users do not intend to. ICLR 2024.
- Song, X., Cai, Z., and Zhao, L. (2026). When AI reviews its own code:
  recursive self-training collapse in code LLMs. arXiv:2606.28438.
- Tirumala, K., Simig, D., Aghajanyan, A., and Morcos, A. S. (2023). D4:
  Improving LLM pretraining via document de-duplication and diversification.
  NeurIPS 2023.
- Xia, M., Malladi, S., Gururangan, S., Arora, S., and Chen, D. (2024). LESS:
  Selecting influential data for targeted instruction tuning. ICML 2024.
- Databricks. databricks-dolly-15k. CC BY-SA 3.0. https://huggingface.co/datasets/databricks/databricks-dolly-15k
