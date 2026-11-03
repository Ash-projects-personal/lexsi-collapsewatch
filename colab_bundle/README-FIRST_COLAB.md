# Lexsi CollapseWatch — Colab launch

Upload `lexsi_finetune.ipynb`, `finetune_raw_5k.jsonl`,
`finetune_gated_5k.jsonl`, `aligntune_sft_raw.yaml`,
`aligntune_sft_gated.yaml`, and `auditkit_eval.yaml` to your Colab
session (same folder), open the notebook on a free T4 GPU, then:

1. Set `HF_USER = "your-username"` in cell 2 of the notebook (the cell that
   says `HF_USER = "YOUR_HF_USERNAME"`).
2. Runtime > Run all. The notebook installs the toolkits, pushes both
   slices to your Hugging Face account, trains both arms, runs the
   AuditKIT evals, and pushes the adapters and logs. You log in to
   Hugging Face inside the notebook session; no credentials are stored
   in these files.
