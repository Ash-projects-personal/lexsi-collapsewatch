# Lexsi submission checklist — CollapseWatch regrounded (Track A, problem #2)

Verified against the event requirements (audit 2026-10-27, re-check the
official rules page before submitting). Status as of 2026-11-01 EOD.

## Event requirements

- [x] **Use at least two Lexsi Labs toolkits** — three chained:
      CuratorKIT 0.1.22 (curation) -> CollapseWatch gate ->
      AlignTune 0.1.28 (SFT) -> AuditKIT 1.1.3 (eval). Verified installed
      and importing in the build venv.
- [x] **Use a dense open-weights LLM from Cohere Labs** — CohereLabs/tiny-aya-base
      (Tiny Aya, 3B), in both AlignTune recipes. Repo id verified via the
      CohereLabs org listing.
- [ ] **Host models, adapters, logs, and datasets on Hugging Face** —
      prepared, not yet executed. The Colab notebook (lexsi_finetune.ipynb)
      pushes the two dataset slices, both LoRA adapters, and training logs
      to HF from Colab (never from the build VM, per the hf.co pause).
      Needs: Ash's HF username filled into the notebook.
- [ ] **Before-and-after metrics** — pipeline skeleton + eval configs ready;
      Table 1 (collapse metrics) measured on real data today. The
      raw-vs-gated fine-tune + AuditKIT evals run on Colab; results TBD.
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
- [ ] **Research paper draft** — intro/method/data/results-so-far drafted;
      results tables fill in after the fine-tune.
- [ ] **Demo video (Ash records, 3 min max)** — after the fine-tune; his only step.
- [ ] **Live demo if shortlisted (Demo Day Nov 22, online option)** — later.

## Guardrails (standing)

- [x] Free registration only; nothing paid.
- [x] No HF downloads/uploads from the VM; no HF credentials on the VM;
      $20 HF credits NOT claimed.
- [x] All compute on Google Colab free tier.
- [x] Real measured metrics only; no synthetic data as evidence.
- [x] Nothing outward: no Discord posts, no messages, no early submission.
- [x] No AI/agent involvement revealed anywhere outward.

## Dates

- Build window: Nov 1-14, 2026. Submit end of day Nov 14.
- Shortlist: Nov 16. Demo Day: Nov 22 (online option).
