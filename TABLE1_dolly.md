# Table 1 — CollapseWatch measurements on databricks-dolly-15k (15,011 rows, CC BY-SA 3.0)

| Metric | Full dataset | Gated slice (fix_rows, template cap 10%) |
|---|---|---|
| Rows | 15011 | 14976 |
| Exact-duplicate rows | 16 (0.1%) | 0 (0.0%) |
| Near-duplicate rows (5-gram Jaccard >= 0.8) | 65 (0.4%) | 0 (0.0%) |
| Template clusters (first 4 prompt words) | 8888 | 8882 |
| Top-1 template share | 1.8% | 1.8% |
| Top-3 template share | 5.1% | 5.1% |
| Vocab top-50 coverage | 36.5% | 36.5% |
| Type-token ratio | 0.051 | 0.051 |
| Answer repetition (template clusters) | 0.002 | 0.001 |
| Modal response length (10-token bucket) | 0-9 (18.9%) | 0-9 (18.9%) |
| Mean response length (tokens) | 60.9 | 60.7 |

### Largest template clusters (full dataset)

| Template key | Rows | Share | Distinct answers | Mean pairwise response similarity |
|---|---|---|---|---|
| `identify which instrument is` | 277 | 1.8% | 277 | 0.0 |
| `give me a list` | 258 | 1.7% | 258 | 0.0 |
| `classify each of the` | 226 | 1.5% | 226 | 0.0 |
| `given this paragraph about` | 192 | 1.3% | 192 | 0.0 |
| `given a reference text` | 184 | 1.2% | 184 | 0.0 |

### Per-category summary

| Category | Rows | Near-dup rate | Top-1 template | Answer repetition |
|---|---|---|---|---|
| brainstorming | 1766 | 0.0% | 14.0% | 0.002 |
| classification | 2136 | 0.2% | 13.0% | 0.000 |
| closed_qa | 1773 | 0.5% | 10.7% | 0.002 |
| creative_writing | 709 | 0.0% | 3.0% | 0.000 |
| general_qa | 2191 | 0.3% | 2.8% | 0.004 |
| information_extraction | 1506 | 0.3% | 9.0% | 0.001 |
| open_qa | 3742 | 0.3% | 3.2% | 0.003 |
| summarization | 1188 | 0.0% | 2.9% | 0.000 |
