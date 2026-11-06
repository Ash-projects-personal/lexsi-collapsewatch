# Lexsi submission checklist — CollapseWatch regrounded (Track 1, problem #2
# "Replacing a closed-model API")

Verified against the event requirements (audit 2026-10-27; official rules
page hackathon.lexsi.ai re-fetched and re-verified 2026-11-03 ~13:20 CDT).
Status as of 2026-11-05 EOD (Day-5 build run).

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
