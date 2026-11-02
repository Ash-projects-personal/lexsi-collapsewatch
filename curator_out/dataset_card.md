# Dataset Card: collapsewatch_curator_stage

## Summary

- **Run timestamp**: 2026-11-01T18:48:03.275440Z
- **Wall clock time**: 180.8s
- **Pipeline config hash**: `ec939f17b6bfa2ca`

## Source Documents

  - Unknown

## Pipeline Stages

| Step | Input | Passed | Recovered | Rejected | Forward |
|------|-------|--------|-----------|----------|---------|
| JSONLReader | 15011 | 15011 | — | 0 | 15011 |
| SchemaGate | 15011 | 14741 | 0 | 270 | 14741 |
| ExactDeduplicator | 14741 | 14725 | — | — | 14725 |
| MinHashDeduplicator | 14725 | 14702 | — | — | 14702 |

## Gate Pass Rates and Rejection Breakdown

- **JSONLReader**: 15011/0 passed (N/A), 0 rejected
- **SchemaGate**: 14741/15011 passed (98.2%), 270 rejected


**Rejection reasons:**
  - `below_min_tokens:9`: 101
  - `below_min_tokens:8`: 87
  - `below_min_tokens:7`: 38
  - `below_min_tokens:6`: 33
  - `below_min_tokens:5`: 6
  - `below_min_tokens:2`: 3
  - `above_max_tokens:4282`: 1
  - `below_min_tokens:3`: 1

## Deduplication

  - near_duplicates_removed: 23
  - surviving_count: 14702

## Known Limitations

- MinHash threshold used: **0.85** — this is a starting point, not a universal answer. Adjust per domain (legal, medical, and other domain-specific corpora may need a lower threshold to avoid losing structurally similar but semantically valid examples).
- Table extraction requires `extract_tables: true` on the PDF reader and MinerU with GPU support. Disabled by default.
- Token counting uses a whitespace tokenizer by default. For exact LLM context window
  enforcement, enable `use_tiktoken: true` in the SchemaGate config.
- Both within-run (MinHash/Diversity) and cross-run (EmbeddingDeduplicator) deduplication
  are available. Cross-run dedup persists an embedding index across runs; use
  `embedding_reset_index: true` to start fresh.

## Reproduction

```bash
pip install curatorkit
curatorkit run pipeline.yaml --output-dir ./out/
```

## Tool Versions

- **curatorkit**: 0.1.22
- **python**: 3.12.3
