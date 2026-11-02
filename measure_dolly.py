#!/usr/bin/env python3
"""CollapseWatch — real-data collapse measurement, dolly-15k.

Lexsi Hackathon Track A, problem statement #2. Build-window code,
written 2026-11-01.

Measures the five CollapseWatch collapse metrics on the full
databricks/databricks-dolly-15k parquet (15,011 real human-written
instruction/response pairs, CC BY-SA 3.0), then applies the CollapseWatch
gate (fix_rows) to produce the gated slice. The Oct-27 collapsewatch
package is imported as a library; nothing here touches the synthetic
demo data from the old CLI.

Outputs (in this directory):
  collapse_dolly_full.json   raw metrics on all 15,011 rows + gate stats
  collapse_dolly_by_category.json  per-category metrics (8 categories)
  TABLE1_dolly.md            paper Table 1, Markdown
"""

import json
import os
import sys

SYS_LIB = os.path.expanduser("~/workspace/hackathons/collapsewatch")
if SYS_LIB not in sys.path:
    sys.path.insert(0, SYS_LIB)

from collapsewatch import fix, metrics  # noqa: E402

DATASET = os.path.expanduser(
    "~/workspace/goals/free-ai-hackathon-wins/hidden_files/lexsi-prep/datasets/dolly-15k.parquet"
)
HERE = os.path.dirname(os.path.abspath(__file__))


def load_rows():
    import pyarrow.parquet as pq

    table = pq.read_table(DATASET).to_pandas()
    rows = []
    for _, r in table.iterrows():
        prompt = r["instruction"]
        if str(r["context"]).strip():
            prompt = prompt + "\n\n" + str(r["context"])
        rows.append(
            {
                "prompt": str(prompt),
                "response": str(r["response"]),
                "category": str(r["category"]),
            }
        )
    return rows


def _slim(m):
    keep = [
        "rows",
        "exact_dup_rows",
        "exact_dup_rate",
        "near_dup_rows",
        "near_dup_rate",
        "template_clusters",
        "top1_template_share",
        "top3_template_share",
        "vocab_top50_coverage",
        "type_token_ratio",
        "length_modal_share",
        "length_modal_bucket_tokens",
        "answer_repetition",
    ]
    out = {k: m[k] for k in keep}
    out["response_length"] = m["response_length"]
    out["worst_templates"] = m["worst_templates"]
    return out


def main():
    rows = load_rows()
    print("rows loaded:", len(rows))

    full = metrics.measure(rows)
    gated, gate_stats = fix.fix_rows(rows)

    full_out = {
        "dataset": "databricks/databricks-dolly-15k",
        "license": "CC BY-SA 3.0",
        "rows": len(rows),
        "metrics": _slim(full),
        "gate": {
            "max_template_share": 0.10,
            "stats": gate_stats,
            "gated_metrics": _slim(metrics.measure(gated)),
        },
    }
    with open(os.path.join(HERE, "collapse_dolly_full.json"), "w") as f:
        json.dump(full_out, f, indent=2, ensure_ascii=False)

    by_cat = {}
    for cat in sorted({r["category"] for r in rows}):
        sub = [r for r in rows if r["category"] == cat]
        by_cat[cat] = _slim(metrics.measure(sub))
    with open(os.path.join(HERE, "collapse_dolly_by_category.json"), "w") as f:
        json.dump(by_cat, f, indent=2, ensure_ascii=False)

    m = full_out["metrics"]
    g = full_out["gate"]["gated_metrics"]
    lines = [
        "# Table 1 — CollapseWatch measurements on databricks-dolly-15k (15,011 rows, CC BY-SA 3.0)",
        "",
        "| Metric | Full dataset | Gated slice (fix_rows, template cap 10%) |",
        "|---|---|---|",
        f"| Rows | {m['rows']} | {g['rows']} |",
        f"| Exact-duplicate rows | {m['exact_dup_rows']} ({m['exact_dup_rate']:.1%}) | {g['exact_dup_rows']} ({g['exact_dup_rate']:.1%}) |",
        f"| Near-duplicate rows (5-gram Jaccard >= 0.8) | {m['near_dup_rows']} ({m['near_dup_rate']:.1%}) | {g['near_dup_rows']} ({g['near_dup_rate']:.1%}) |",
        f"| Template clusters (first 4 prompt words) | {m['template_clusters']} | {g['template_clusters']} |",
        f"| Top-1 template share | {m['top1_template_share']:.1%} | {g['top1_template_share']:.1%} |",
        f"| Top-3 template share | {m['top3_template_share']:.1%} | {g['top3_template_share']:.1%} |",
        f"| Vocab top-50 coverage | {m['vocab_top50_coverage']:.1%} | {g['vocab_top50_coverage']:.1%} |",
        f"| Type-token ratio | {m['type_token_ratio']:.3f} | {g['type_token_ratio']:.3f} |",
        f"| Answer repetition (template clusters) | {m['answer_repetition']:.3f} | {g['answer_repetition']:.3f} |",
        f"| Modal response length (10-token bucket) | {m['length_modal_bucket_tokens']} ({m['length_modal_share']:.1%}) | {g['length_modal_bucket_tokens']} ({g['length_modal_share']:.1%}) |",
        f"| Mean response length (tokens) | {m['response_length']['mean']} | {g['response_length']['mean']} |",
        "",
        "### Largest template clusters (full dataset)",
        "",
        "| Template key | Rows | Share | Distinct answers | Mean pairwise response similarity |",
        "|---|---|---|---|---|",
    ]
    for w in m["worst_templates"]:
        lines.append(
            f"| `{w['template']}` | {w['rows']} | {w['share']:.1%} | {w['distinct_answers']} | {w['mean_pairwise_response_similarity']} |"
        )
    lines += [
        "",
        "### Per-category summary",
        "",
        "| Category | Rows | Near-dup rate | Top-1 template | Answer repetition |",
        "|---|---|---|---|---|",
    ]
    for cat, c in by_cat.items():
        lines.append(
            f"| {cat} | {c['rows']} | {c['near_dup_rate']:.1%} | {c['top1_template_share']:.1%} | {c['answer_repetition']:.3f} |"
        )
    with open(os.path.join(HERE, "TABLE1_dolly.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("wrote collapse_dolly_full.json, collapse_dolly_by_category.json, TABLE1_dolly.md")


if __name__ == "__main__":
    main()
