# Lexsi submission checklist — CollapseWatch regrounded (Track 1, problem #2
# "Replacing a closed-model API")

Verified against the event requirements (audit 2026-10-27; official rules
page hackathon.lexsi.ai re-fetched and re-verified 2026-11-03 ~13:20 CDT).
Status as of 2026-11-11 (Day-11 re-verify). Stage 1 deadline EXTENDED to Sun Nov 15, 11:59 PM AoE (Lexsi Labs mail from Ram Kadiyala, Gmail id 1a1ca63408625a48; supersedes the Nov 14 date).

## 2026-11-11 Day-11 re-verify (hash compare + manifest + banned-metrics sweep)

- **Determinism: all four hashes MATCH the Nov 10 recorded values
  (ninth consecutive byte-identical run).** Hashes recomputed
  2026-11-11 and compared directly against the Day-10 literals:
  `collapse_dolly_full.json`
  1e4b0fcaf47180ee7ac06a54bb9003177688d5ff006fc1f7eb2f462b141a1529 (match),
  `collapse_dolly_by_category.json`
  ef0574a0547954867306be664e055ba8f6131e9b09411d517ace4fbd8920f016 (match),
  `collapse_slices_5k.json`
  fe6fb810416df397f5c1f472a6d68e51c72b24aaa775c985a8a1fa05ee23813b (match),
  `TABLE1_dolly.md`
  d3c3fbc97b2ae100130bc721498e875a91a39bb149347b60ca05c410966e5f36 (match).
  Hash-only re-verify this run (no measure-script re-run needed: identical
  hashes prove byte-identical files). No HF.co traffic, no credentials.
- **Colab fine-tune results: still NONE (2026-11-11).** Workspace scan
  found no eval outputs, checkpoints, LoRA adapters, training logs, or
  HF result files in `lexsi-collapsewatch/` or `lexsi-prep/`: no
  `.safetensors` / `adapter_config.json` / `trainer_state.json` /
  `training_args.bin` / `checkpoint-*` / `*eval*result*` hits outside
  venv site-packages. The only files changed in `lexsi-collapsewatch/`
  since Nov 10 12:00 UTC are the Day-10 re-run outputs themselves
  (collapse JSONs, TABLE1, Nov 10 18:20–18:21 UTC) and this checklist.
  `lexsi-prep/` has no files changed since Nov 10 12:00 UTC and is
  unchanged since Oct 30 (only the Oct 30 fetch/install/retry logs).
  The `.safetensors` / adapter hits elsewhere in the workspace belong to
  the unrelated `projects/rebuilds/llm-finetuning-pipeline/` portfolio
  rebuild, not Lexsi. Colab NOT launched (Ash-gated); no hf.co access,
  no credits claim. Blocker unchanged: Ash's HF username → Colab launch
  (raw-vs-gated fine-tune + AuditKIT evals) → PAPER.md §6.2, abstract
  final, ROI draft, demo video.
- **Pipeline manifest reconciled against the actual files (2026-11-11):**
  dolly parquet on disk = 15,011 rows (verified via pyarrow, cols
  instruction/context/response/category/_split);
  `curator_out/train/sft_alpaca.jsonl` = 13,231; eval = 1,471 (13,231 +
  1,471 = 14,702 curated); `curator_out/rejected.jsonl` = 270 (schema
  gate); `dolly_gated.jsonl` = 13,225 (13,231 − 6 near-dups, gate stats
  match); both 5k slices = 5,000 rows, seed 42. Every manifest figure
  traces to a real file; no mismatch.
- **Banned-metrics sweep 2026-11-11: zero project claims.** Full banned
  list from the parallel-build-plan grepped across PAPER.md and
  README.md: no banned portfolio-audit metrics, no "JD Keywords" label,
  no spelled-out "percent", no he/his/she/her/him person pronouns, no
  literal "3.4" in either doc. The only they/their hits are the same
  generic plurals documented on Day-10, referring to data/prompts/
  templates (PAPER.md:15, 39, 45–46, 65, 69, 98; README.md:10), plus
  one author initial ("He, K.") in a citation (PAPER.md:273) — not
  person pronouns, not violations. PAPER.md untouched today.
- **Deadline update:** Stage 1 deadline EXTENDED to Sun Nov 15,
  11:59 PM AoE (Lexsi Labs mail from Ram Kadiyala, Gmail id
  1a1ca63408625a48). 4 days left from Nov 11.

## 2026-11-10 Day-10 pipeline re-verification

- **Full pipeline reproduces byte-identically, eighth consecutive run.**
  `measure_dolly.py` re-run 2026-11-10 in the local `.venv`: regenerated
  `collapse_dolly_full.json`, `collapse_dolly_by_category.json`, and
  `TABLE1_dolly.md` are **byte-identical** to the pre-run files
  (sha256-verified before/after, all four hashes match the Day-9 literal
  values exactly: full 1e4b0fca…, by-category ef0574a0…,
  slices fe6fb810…, TABLE1 d3c3fbc9…). `measure_slices.py` re-run:
  `collapse_slices_5k.json` unchanged (fe6fb810…); slice table re-printed
  identical (near-dups 6 vs 0, clusters 3,334 vs 3,360, top-1 1.9% vs
  1.8%, vocab50 36.7% both, answer rep 0.001 both). No HF.co traffic, no
  credentials. /tmp healthy at run start (469M free), nothing written
  to /tmp.
- **Pipeline manifest reconciled against the actual files (2026-11-10):**
  dolly parquet on disk = 15,011 rows, cols
  instruction/context/response/category/_split (at
  `~/workspace/goals/free-ai-hackathon-wins/hidden_files/lexsi-prep/datasets/dolly-15k.parquet`,
  unchanged since Oct 30);
  `curator_out/train/sft_alpaca.jsonl` = 13,231; eval = 1,471 (13,231 +
  1,471 = 14,702 curated); `curator_out/rejected.jsonl` = 270 (schema
  gate); `dolly_gated.jsonl` = 13,225 (13,231 − 6 near-dups, gate stats
  match); both 5k slices = 5,000 rows, seed 42. Every manifest figure
  traces to a real file; no mismatch.
- **PAPER.md: no numeric changes needed (2026-11-10).** Re-run outputs
  are byte-identical, so the Day-5 full truth-check still holds; the
  5k-slice table re-printed today matches the paper's slice block. No
  real artifact contradicts any paper number. PAPER.md untouched today.
- **Banned-metrics sweep 2026-11-10:** full banned list from the
  parallel-build-plan grepped across PAPER.md and README.md:
  **zero project claims.** No "JD Keywords" label; no spelled-out
  "percent". The only pronoun hits are generic plurals referring to
  data/prompts ("They are infrastructure", "their first four") plus one
  author initial ("He, K.") in a citation, not person pronouns. One
  regex artifact noted: the unescaped pattern `3.4` matched "3,360 vs
  3,334" in PAPER.md:219 (the paper's own real measured cluster counts);
  no literal "3.4" exists in either doc, and the banned "3.4–4.6 blind
  eval" pattern scores zero. Colab bundle unchanged since Nov 4 (dir
  mtime Nov 4 18:26 UTC), so its Day-8 clean sweep still stands.
- **Colab fine-tune results: still NONE (2026-11-10).** Workspace scan
  found no eval outputs, checkpoints, LoRA adapters, training logs, or
  HF result files: no `.safetensors` / `adapter_config.json` /
  `trainer_state.json` / `checkpoint-*` hits in `lexsi-collapsewatch/`
  or `lexsi-prep/` outside venv site-packages, and the only files
  changed in `lexsi-collapsewatch/` since Day-9 are the Day-9 re-run
  outputs themselves and this checklist. `lexsi-prep/` unchanged since
  Oct 30. Blocker unchanged: Ash's HF username → Colab launch.
  Submission due end of day Nov 14 AoE — 4 days left.

## 2026-11-09 Day-9 pipeline re-verification

- **Full pipeline reproduces byte-identically, seventh consecutive run.**
  `measure_dolly.py` re-run 2026-11-09 in the local `.venv`: regenerated
  `collapse_dolly_full.json`, `collapse_dolly_by_category.json`, and
  `TABLE1_dolly.md` are **byte-identical** to the pre-run files
  (sha256-verified before/after, all four hashes match the Day-8 literal
  values exactly: full 1e4b0fca…, by-category ef0574a0…,
  slices fe6fb810…, TABLE1 d3c3fbc9…). `measure_slices.py` re-run:
  `collapse_slices_5k.json` unchanged (fe6fb810…). No HF.co traffic, no
  credentials. /tmp was healthy at run start (464M free), nothing written
  to /tmp.
- **Pipeline manifest reconciled against the actual files (2026-11-09):**
  dolly parquet on disk = 15,011 rows, cols
  instruction/context/response/category/_split (at
  `~/workspace/goals/free-ai-hackathon-wins/hidden_files/lexsi-prep/datasets/dolly-15k.parquet`,
  unchanged since Oct 30);
  `curator_out/train/sft_alpaca.jsonl` = 13,231; eval = 1,471 (13,231 +
  1,471 = 14,702 curated); `curator_out/rejected.jsonl` = 270 (schema
  gate); `dolly_gated.jsonl` = 13,225 (13,231 − 6 near-dups, gate stats
  match); both 5k slices = 5,000 rows, seed 42. Every manifest figure
  traces to a real file; no mismatch.
- **PAPER.md: no numeric changes needed (2026-11-09).** Re-run outputs
  are byte-identical, so the Day-5 full truth-check still holds; the
  5k-slice table re-printed today matches the paper's slice block (6 vs
  0 near-dups, 3,334 vs 3,360 clusters, 1.9% vs 1.8% top-1, 36.7% vocab50
  both, 0.001 answer rep both). No real artifact contradicts any paper
  number.
- **Banned-metrics sweep 2026-11-09:** full banned list from the
  parallel-build-plan grepped across PAPER.md and README.md:
  **zero project claims.** No "JD Keywords" label; no spelled-out
  "percent". The only pronoun hits are generic plurals referring to
  data/prompts ("They are infrastructure", "their first four"), not
  person pronouns; no he/his/she/her in the project docs. Colab bundle
  unchanged since Nov 4 (no bundle source changed), so its Day-8 clean
  sweep still stands.
- **Colab fine-tune results: still NONE (2026-11-09).** Workspace-wide
  scan found no eval outputs, checkpoints, LoRA adapters, training
  logs, or HF result files: the only `.safetensors` /
  `*eval*result*` hits in the Lexsi dirs are venv site-packages files,
  and the workspace-wide newer-than-Day-8 scan returned zero new
  fine-tune files. `lexsi-prep/` unchanged since Oct 30; the only
  files changed in `lexsi-collapsewatch/` since Day-7 are the Day-8
  re-run outputs and this checklist. Blocker unchanged: Ash's HF
  username → Colab launch.

- **Full pipeline reproduces byte-identically, sixth consecutive run.**
  `measure_dolly.py` re-run 2026-11-08 in the local `.venv`: regenerated
  `collapse_dolly_full.json`, `collapse_dolly_by_category.json`, and
  `TABLE1_dolly.md` are **byte-identical** to the pre-run files
  (sha256-verified before/after: full 1e4b0fca…, by-category ef0574a0…,
  TABLE1 d3c3fbc9…). `measure_slices.py` re-run: `collapse_slices_5k.json`
  unchanged (fe6fb810…). Note for future runs: the literal 2026-11-01
  hash values were never written into any day log, so the chain rests on
  the Day-5/6/7 sha256-verified claims plus unchanged file mtimes since
  Nov 7; the four hashes above are now recorded here so Day-9 can compare
  directly. No HF.co traffic, no credentials.
- **Pipeline manifest reconciled against the actual files (2026-11-08):**
  dolly parquet on disk = 15,011 rows, cols
  instruction/context/response/category/_split (at
  `~/workspace/goals/free-ai-hackathon-wins/hidden_files/lexsi-prep/datasets/dolly-15k.parquet`,
  unchanged since Oct 30);
  `curator_out/train/sft_alpaca.jsonl` = 13,231; eval = 1,471 (13,231 +
  1,471 = 14,702 curated); `curator_out/rejected.jsonl` = 270 (schema
  gate); `dolly_gated.jsonl` = 13,225 (13,231 − 6 near-dups, gate stats
  match); both 5k slices = 5,000 rows, seed 42. Curator manifest stage
  counts also agree (15,011 → 14,741 after 270 schema rejections →
  14,725 exact-dedup → 14,702 MinHash = train + eval). Every manifest
  figure traces to a real file.
- **PAPER.md: no numeric changes needed (2026-11-08).** Re-run outputs
  are byte-identical, so the Day-5 full truth-check still holds; the
  5k-slice table re-printed today matches the paper's slice block (6 vs
  0 near-dups, 3,334 vs 3,360 clusters, 1.9% vs 1.8% top-1, 36.7% vocab50
  both, 0.001 answer rep both). No real artifact contradicts any paper
  number.
- **Banned-metrics sweep 2026-11-08:** full banned list from the
  parallel-build-plan (14,000-doc RAG, 98.7% uptime, 38ms inference,
  91.4% accuracy, TensorRT, Grad-CAM, heart-failure AUC, plus the
  portfolio-audit set) grepped across the project docs, scripts, and
  configs: **zero project claims.** The only raw hits are this
  checklist's own sweep record naming the searched terms (meta-mention,
  not a claim). Dataset files still carry the known verbatim dolly-15k
  source text ("heart failure" in 3 `dolly_raw.jsonl` rows, "14,000" in
  11) — real public dataset content, not project claims, no fix applies.
  No "JD Keywords" label (only this checklist's "No JD Keywords label"
  meta-mention); no spelled-out "percent" (only the meta-mention);
  no he/his/she/her pronouns in the project docs (the only "He" hits
  are author surnames in PAPER.md references, e.g. "He, K."). Colab
  bundle zip contents clean (notebook + yamls swept, no hits).
- **Colab bundle still in sync:** all 5 bundle files byte-identical to
  the workspace copies (zip rebuilt 2026-11-04; no bundle source changed
  since). No eval outputs, checkpoints, LoRA adapters, training logs, or
  HF result files anywhere in the workspace: the only file changed in
  `lexsi-collapsewatch/` since Day-7 is this checklist, and the only
  `.safetensors`/`adapter_config.json`/`trainer_state.json` hits in the
  workspace belong to unrelated projects (teardown-work timestral /
  statebench models, `projects/rebuilds/llm-finetuning-pipeline`).
- **Configs:** raw vs gated AlignTune recipes still identical except
  dataset name, run_name, output_dir (plus the header comment wording;
  diff re-checked 2026-11-08).
- **Single open blocker, unchanged:** Ash's HF username → Colab launch
  (raw-vs-gated fine-tune + AuditKIT evals) → PAPER.md §6.2, abstract
  final, ROI draft, demo video. Submission due Nov 14 AoE — 6 days left.

## 2026-11-07 Day-7 pipeline re-verification

- **Full pipeline reproduces byte-identically, fifth consecutive run.**
  `measure_dolly.py` re-run 2026-11-07 in the local `.venv`: regenerated
  `collapse_dolly_full.json`, `collapse_dolly_by_category.json`, and
  `TABLE1_dolly.md` are **byte-identical** to the 2026-11-01 outputs
  (sha256-verified before/after). `measure_slices.py` re-run:
  `collapse_slices_5k.json` unchanged. No HF.co traffic, no credentials.
- **Pipeline manifest reconciled against the actual files (2026-11-07):**
  dolly parquet on disk = 15,011 rows, cols
  instruction/context/response/category/_split (at
  `~/workspace/goals/free-ai-hackathon-wins/hidden_files/lexsi-prep/datasets/dolly-15k.parquet`,
  unchanged since Oct 30);
  `curator_out/train/sft_alpaca.jsonl` = 13,231; eval = 1,471 (13,231 +
  1,471 = 14,702 curated); `curator_out/rejected.jsonl` = 270 (schema
  gate); `dolly_gated.jsonl` = 13,225 (13,231 − 6 near-dups, gate stats
  match); both 5k slices = 5,000 rows, seed 42. Every manifest figure
  traces to a real file.
- **PAPER.md: no numeric changes needed (2026-11-07).** Re-run outputs
  are byte-identical to 2026-11-01, so the Day-5 full truth-check still
  holds; spot-verified again today against the regenerated JSONs (16/65
  dups, 8,888/8,882 clusters, 1.8%/5.1% top-1/top-3, 36.5% vocab50,
  0.051 TTR, 0.002/0.001 answer rep, 18.9% modal bucket, 60.9/60.7 mean
  len; gate drops 35 = 16+19, cap drops 0; category counts sum to
  15,011; 5k slices 6 vs 0 near-dups, 3,334 vs 3,360 clusters). No real
  artifact contradicts any paper number.
- **Banned-metrics sweep 2026-11-07:** full banned list from the
  parallel-build-plan (14,000-doc RAG, 98.7% uptime, 38ms inference,
  91.4% accuracy, TensorRT, Grad-CAM, heart-failure AUC, plus the
  portfolio-audit set) grepped across all workspace files: **zero
  project claims.** The only raw hits are verbatim dolly-15k source text
  inside the dataset files themselves ("heart failure" as a pneumonia
  risk factor / disease mention in curator_out rows; "14,000 people",
  "14,000 screens", "14,000 years ago", "91.4"/"97.3"/"8,400" only
  inside dataset rows) — real public dataset content, not project
  claims, and no fix applies. The checklist's own sweep record naming
  the searched terms is a meta-mention, not a claim. No "JD Keywords"
  label; no spelled-out "percent"; no he/his/she/her pronouns in the
  project docs (the only "them" hits refer to datasets/metrics, not a
  person). Colab bundle zip contents clean.
- **Colab bundle still in sync:** all 5 bundle files byte-identical to
  the workspace copies (zip rebuilt 2026-11-04; no bundle source changed
  since). No eval outputs, checkpoints, LoRA adapters, training logs, or
  HF result files anywhere in the workspace.
- **Configs:** raw vs gated AlignTune recipes still identical except
  dataset name, run_name, output_dir (plus the header comment wording;
  diff re-checked 2026-11-07).

## 2026-11-06 Day-6 pipeline re-verification

- **Full pipeline reproduces byte-identically, fourth consecutive run.**
  `measure_dolly.py` re-run 2026-11-06 in the local `.venv`: regenerated
  `collapse_dolly_full.json`, `collapse_dolly_by_category.json`, and
  `TABLE1_dolly.md` are **byte-identical** to the 2026-11-01 outputs
  (sha256-verified before/after). `measure_slices.py` re-run:
  `collapse_slices_5k.json` unchanged. No HF.co traffic, no credentials.
- **Pipeline manifest reconciled against the actual files (2026-11-06):**
  dolly parquet on disk = 15,011 rows, cols
  instruction/context/response/category/_split (at
  `~/workspace/goals/free-ai-hackathon-wins/hidden_files/lexsi-prep/datasets/dolly-15k.parquet`,
  unchanged since Oct 30);
  `curator_out/train/sft_alpaca.jsonl` = 13,231; eval = 1,471 (13,231 +
  1,471 = 14,702 curated); `curator_out/rejected.jsonl` = 270 (schema
  gate); `dolly_gated.jsonl` = 13,225 (13,231 − 6 near-dups, gate stats
  match); both 5k slices = 5,000 rows, seed 42. Every manifest figure
  traces to a real file.
- **PAPER.md: no numeric changes needed (2026-11-06).** Re-run outputs
  are byte-identical to 2026-11-01, so the Day-5 full truth-check still
  holds; no real artifact contradicts any paper number.
- **Banned-metrics sweep 2026-11-06:** full banned list from the
  parallel-build-plan (14,000-doc RAG, 98.7% uptime, 38ms inference,
  91.4% accuracy, TensorRT, Grad-CAM, heart-failure AUC, plus the
  portfolio-audit set) grepped across all workspace files: **zero
  project claims.** The only raw hits are verbatim dolly-15k source text
  inside the dataset files themselves ("14,000 people" at a board-game
  convention, "heart failure" as a pneumonia risk factor, "14,000
  screens" for Avatar, "14,000 years ago" for the Great Lakes, "91.4"
  and "97.3"/"8,400" only inside dataset rows) — real public dataset
  content, not project claims, and no fix applies. The checklist's own
  sweep record naming the searched terms is a meta-mention, not a claim.
- **Colab bundle still in sync:** all 6 bundle files byte-identical to
  the workspace copies (zip rebuilt 2026-11-04; no bundle source changed
  since). No eval outputs, checkpoints, LoRA adapters, training logs, or
  HF result files anywhere in the workspace.
- **Configs:** raw vs gated AlignTune recipes still identical except
  dataset name, run_name, output_dir (diff re-checked 2026-11-06).

## 2026-11-05 Day-5 pipeline re-verification

- **Full pipeline reproduces byte-identically, third consecutive run.**
  `measure_dolly.py` re-run 2026-11-05 in the local `.venv`: regenerated
  `collapse_dolly_full.json`, `collapse_dolly_by_category.json`, and
  `TABLE1_dolly.md` are **byte-identical** to the 2026-11-01 outputs
  (sha256-verified before/after). `measure_slices.py` re-run:
  `collapse_slices_5k.json` unchanged. No HF.co traffic, no credentials.
- **Pipeline manifest reconciled against the actual files (2026-11-05):**
  dolly parquet on disk = 15,011 rows; `curator_out/train/sft_alpaca.jsonl`
  = 13,231; eval = 1,471 (13,231 + 1,471 = 14,702 curated);
  `curator_out/rejected.jsonl` = 270 (schema gate); `dolly_gated.jsonl` =
  13,225 (13,231 − 6 near-dups, gate stats match); both 5k slices =
  5,000 rows, seed 42. Every manifest figure traces to a real file.
- **PAPER.md full truth-check 2026-11-05:** every numeric claim re-traced
  to a real artifact. Table 1 row-verified again (16/65 dups, 8,888/8,882
  clusters, 1.8%/5.1% top-1/top-3, 36.5% vocab50, 0.051 TTR, 0.002/0.001
  answer rep, 18.9% modal bucket, 60.9/60.7 mean len; gate drops 35 =
  16+19, cap drops 0); all 8 category counts sum to 15,011; brainstorming
  14.0% / classification 13.0% top-1 templates; 5k-slice block (6 vs 0
  near-dups, 3,334 vs 3,360 clusters) verified. Config claims verified
  (LoRA r=32, unsloth, bf16, 160 steps/arm, 1 epoch; MMLU/HellaSwag/
  ARC-Challenge 5-shot, temp 0, seed 42). Two wording fixes applied:
  PAPER.md §9 "are hosted" → "will be hosted" (HF hosting is post-Colab,
  not yet done); README "Measured today" → dated 2026-11-01 with
  re-verification dates. No numeric fixes needed.
- **Banned-metrics sweep 2026-11-05:** full banned list from the
  parallel-build-plan (14,000-doc RAG, 98.7% uptime, 38ms inference,
  91.4% accuracy, TensorRT, Grad-CAM, heart-failure AUC, plus the
  portfolio-audit set) grepped across all workspace files: **zero
  project claims.** The only raw hits are verbatim dolly-15k source text
  inside the dataset files themselves ("14,000 people" at a board-game
  convention, "heart failure" as a pneumonia risk factor, "14,000
  screens" for Avatar) — real public dataset content, not project
  claims, and no fix applies. The checklist's own sweep record naming
  the searched terms is a meta-mention, not a claim.
- **Colab bundle still in sync:** all 6 bundle files byte-identical to
  the workspace copies (zip rebuilt 2026-11-04; no source file changed
  since except the two wording fixes above, which do not affect bundle
  contents). Credential grep across scripts/configs/notebook/docs:
  clean (only "token" as in token counts).
- **Configs:** raw vs gated AlignTune recipes still identical except
  dataset name, run_name, output_dir (diff re-checked 2026-11-05).

## 2026-11-04 Day-4 pipeline re-verification

- **Full pipeline reproduces byte-identically.** `measure_dolly.py` re-run
  2026-11-04 on the local dolly-15k parquet (15,011 rows): regenerated
  `collapse_dolly_full.json`, `collapse_dolly_by_category.json`, and
  `TABLE1_dolly.md` are **byte-identical** to the 2026-11-01 outputs.
  `measure_slices.py` re-run: `collapse_slices_5k.json` unchanged.
  Runs in a local `.venv` (pyarrow+pandas; system pip is externally
  managed; `.venv/` is gitignored). No HF.co traffic, no credentials.
- **PAPER.md full truth-check 2026-11-04:** every numeric claim traced to
  a real artifact. Table 1 (16 exact dup / 65 near dup / 8,888 clusters /
  1.8% top-1 / 5.1% top-3 / 36.5% vocab50 / 0.051 TTR / 0.002 answer rep /
  18.9% modal bucket / 60.9 mean len; gate drops 35 = 16+19, cap drops 0),
  all 8 category counts (sum 15,011), brainstorming 14.0% /
  classification 13.0% top-1 templates, and the 5k-slice consistency block
  (6 vs 0 near-dups, 3,334 vs 3,360 clusters) all verified against the
  JSONs. Zero fixes needed; paper numbers match the artifacts.
- **Banned-metrics sweep 2026-11-04:** grepped all workspace files for the
  Oct-22 portfolio metrics (14,000-doc RAG, 98.7% uptime, 38ms inference,
  91.4% accuracy, TensorRT, Grad-CAM, heart-failure AUC): **zero hits.**
- **Configs:** raw vs gated AlignTune recipes verified identical except
  dataset name, run_name, output_dir; seed 42 in both recipes and
  auditkit_eval.yaml; model-id verification comment added to the gated
  recipe; colab_bundle zip rebuilt (same 7 files) to keep bundle copies
  in sync. `run_evals.sh` sane; `<HF_USER>` placeholders intact; no
  credentials anywhere.
- **Pipeline accounting reconciles:** 15,011 -> schema gate 270 rejected
  -> exact dedup -> MinHash 0.85 -> 14,702 curated = train 13,231 + eval
  1,471; CollapseWatch gate on train split drops 6 near-dups -> 13,225;
  5k slices sampled seed 42 from each arm.

## 2026-11-03 re-verification of official rules page

- Three tracks live; Track 1 = Fine-tuning and Data Curation with 9 problem
  statements. Problem #2 = "Replacing a closed-model API: Take a
  high-volume business task that is usually sent to a large closed model
  (classification, extraction, summarisation, drafting) and fine-tune a
  small open model to match it at a fraction of the cost." Confirmed as the
  problem this project targets; fits.
- Project requirements: MINIMUM 2 repos from the track chained into a real
  pipeline (preferred: 3+). Ours chains 4 (CuratorKIT -> CollapseWatch gate
  -> AlignTune -> AuditKIT). Cohere Labs dense open-weights LLM (Tiny Aya).
- Submission due end of day Nov 14 **(AoE)** via the "Submit your project"
  form at hackathon.lexsi.ai. Latest submission counts if resubmitted.
- Submission packet (all items confirmed 2026-11-03):
  registered email; abstract < 500 words; HF **model collection** (all
  models/adapters public, un-gated); HF **dataset collection** (datasets,
  logs, traces, curated data; all public); write-up/article (HF article,
  or GitHub README is acceptable); GitHub repo with reproducibility notes
  in the README; the repos + models used, tracks, and problem statements;
  project deployed publicly (public demo or repo link); before-and-after
  metrics (more than one metric); optional-but-preferred ROI comparison of
  the closed-source model vs the fine-tuned small model.

## Event requirements

- [x] **Use at least two Lexsi Labs toolkits** — three chained:
      CuratorKIT 0.1.22 (curation) -> CollapseWatch gate ->
      AlignTune 0.1.28 (SFT) -> AuditKIT 1.1.3 (eval). Verified installed
      and importing in the build venv.
- [x] **Use a dense open-weights LLM from Cohere Labs** — CohereLabs/tiny-aya-base
      (Tiny Aya, 3B), in both AlignTune recipes. Repo id verified via the
      CohereLabs org listing.
- [ ] **Host models, adapters, logs, and datasets on Hugging Face** —
      prepared, not yet executed. Requirement confirmed 2026-11-03: TWO
      public un-gated collections — one HF model collection (models +
      adapters) and one HF dataset collection (datasets, logs, curated
      data). The Colab notebook (lexsi_finetune.ipynb) pushes the two
      dataset slices, both LoRA adapters, and training logs to HF from
      Colab (never from the build VM, per the hf.co pause). Colab-ready
      bundle packaged 2026-11-02: colab_bundle/
      (lexsi-collapsewatch-colab.zip, 7 files, no credentials).
      Needs: Ash's HF username filled into the notebook + Colab launch.
- [ ] **Before-and-after metrics** — pipeline skeleton + eval configs ready;
      Table 1 (collapse metrics) measured on real data 2026-11-01.
      Internal-consistency check 2026-11-02 (measure_slices.py, real runs):
      gated vs raw 5k slices — near-duplicate rows 0 vs 6 (0.12%), top-1
      template share 1.8% vs 1.9%, vocab top-50 coverage 36.7% vs 36.7%,
      answer repetition 0.001 both; gate removes residual near-dups and
      otherwise passes the slice through. The raw-vs-gated fine-tune +
      AuditKIT evals run on Colab; results TBD.
- [x] **Chain the stack into a real pipeline (Track 1)** —
      `curator_pipeline.py` chains CuratorKIT -> gate -> slice export;
      AlignTune recipes and `run_evals.sh` (AuditKIT) continue the chain.
      Validated end to end on the VM through the slice-export stage.
- [x] **Online hackathon** — fully online Nov 1-21; Ash attends online only.
- [x] **Registered** — solo, ticket #0H8C-TZBE-AJ6K, Fine-tuning and Data
      Curation track. Registration closes Nov 5; already done.
- [x] **Novelty + name checks** — novelty verdict BUILD (fresh check Nov 1);
      "CollapseWatch" name check CLEAN (Oct 27 screening).
- [x] **Real-data plan + paper outline** — done (PAPER.md; dolly-15k measured).
- [ ] **Research paper draft** — intro/method/data drafted; Related work,
      Limitations, Future work, Reproducibility drafted 2026-11-02
      (NeMo Curator + datatrove added). ALL citation [VERIFY] tags resolved
      2026-11-03 via web-source checks: SemDeDup = ICML 2023 (was wrongly
      listed as ICLR 2023, fixed); AlpaGasus = ICLR 2024, full 11-author
      list confirmed; DEITA = ICLR 2024 (confirmed); Hsiung et al. 2026 =
      real (ACL 2026 long paper, arXiv:2506.05346, 7 authors — author list
      corrected to add Chen, P.-Y. and Yang, Y.); Song/Cai/Zhao 2026 =
      real (arXiv:2606.28438, under review); D4 venue refined to NeurIPS
      2023 Datasets and Benchmarks Track. Fine-tune result tables still
      TBD after the Colab run.
- [ ] **Demo video (Ash records, 3 min max)** — after the fine-tune; his only step.
- [ ] **Abstract (< 500 words) for the submission form** — DRAFT skeleton
      written 2026-11-04 (abstract_draft.md, 180 words, no fine-tune result
      claims; results/ROI deltas stay TBD until the Colab run).
- [ ] **Optional-but-preferred ROI comparison** (closed-source vs
      fine-tuned small model) — can be drafted from the fine-tune run's
      GPU-hour numbers once Ash's Colab run completes.
- [ ] **Live demo if shortlisted (Demo Day Nov 22, online option)** — later.

## 2026-11-07 status

- Still blocked on the single Ash-gated chain: Colab notebook NOT yet run
  (no fine-tune metrics, eval outputs, or HF result files in the workspace
  as of 2026-11-07 ~12:40 CST; workspace file scan confirms none outside
  the `.venv`, and no file changed since Nov 6 18:24 except the Day-7
  re-verification outputs). Raw-vs-gated fine-tune + AuditKIT evals remain
  the one blocker for PAPER.md results, the abstract final draft, the ROI
  comparison, and the demo video. Everything upstream is re-verified and
  stable for the fifth consecutive day. Submission due Nov 14 AoE — 7 days
  left.
- Registration: already done (solo, ticket #0H8C-TZBE-AJ6K). Registration
  closed Nov 5 — no action needed, already registered.

## 2026-11-06 status

- Still blocked on the single Ash-gated chain: Colab notebook NOT yet run
  (no fine-tune metrics, eval outputs, or HF result files in the workspace
  as of 2026-11-06 ~12:30 CST; workspace file scan confirms none outside
  the `.venv`, and no file changed since Nov 4 18:27 except the Day-5
  re-verification outputs). Raw-vs-gated fine-tune + AuditKIT evals remain
  the one blocker for PAPER.md results, the abstract final draft, the ROI
  comparison, and the demo video. Everything upstream is re-verified and
  stable for the fourth consecutive day.
- Registration: already done (solo, ticket #0H8C-TZBE-AJ6K). Registration
  closed Nov 5 — no action needed, already registered.

## 2026-11-05 status

- Still blocked on the single Ash-gated chain: Colab notebook NOT yet run
  (no fine-tune metrics, eval outputs, or HF result files in the workspace
  as of 2026-11-05 ~12:30 CST; workspace file scan confirms none outside
  the `.venv`). Raw-vs-gated fine-tune + AuditKIT evals remain the one
  blocker for PAPER.md results, the abstract final draft, the ROI
  comparison, and the demo video. Everything upstream is re-verified and
  stable for the third consecutive day.
- Registration: already done (solo, ticket #0H8C-TZBE-AJ6K). Registration
  closes TODAY Nov 5 — no action needed, already registered.

## 2026-11-04 status

- Still blocked on the single Ash-gated chain: Colab notebook NOT yet run
  (no fine-tune metrics, eval outputs, or HF result files in the workspace
  as of 2026-11-04 ~12:20 CDT). Raw-vs-gated fine-tune + AuditKIT evals
  remain the one blocker for PAPER.md results, the abstract final draft,
  the ROI comparison, and the demo video. Everything upstream is
  re-verified and stable.
- Registration: already done (solo, ticket #0H8C-TZBE-AJ6K). Registration
  closes Nov 5 — no action needed.

## 2026-11-03 status

- Colab notebook NOT yet run: no fine-tune metrics, eval outputs, or HF
  result files appeared in the workspace on Nov 3 (checked). The
  raw-vs-gated fine-tune + AuditKIT evals remain the single blocker for
  the results section, the abstract, the ROI comparison, and the demo video.
- Registration: already done (solo, ticket #0H8C-TZBE-AJ6K). Closes Nov 5 —
  nothing further needed.

## Guardrails (standing)

- [x] Free registration only; nothing paid.
- [x] No HF downloads/uploads from the VM; no HF credentials on the VM;
      $20 HF credits NOT claimed.
- [x] All compute on Google Colab free tier.
- [x] Real measured metrics only; no synthetic data as evidence.
- [x] Nothing outward: no Discord posts, no messages, no early submission.
- [x] No AI/agent involvement revealed anywhere outward.

## Blocked on Ash (unchanged, 2026-11-03)

1. HF username — fill into lexsi_finetune.ipynb (needs his exact
   huggingface.co handle).
2. Colab notebook launch — the only remaining compute step (raw-vs-gated
   fine-tune + AuditKIT evals, GPU free tier).
3. Demo video (3 min max) — after the fine-tune results are in.

## Dates

- Build window: Nov 1-14, 2026. Submit end of day Nov 14 **(AoE)** via the
  "Submit your project" form at hackathon.lexsi.ai. Latest submission
  counts.
- Registration closes Nov 5 (already registered — reminder only).
- Shortlist: Nov 16. Demo Day: Nov 22 (online option).
