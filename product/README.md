# Trade Management — Product

This folder contains customer-facing product artifacts and a small demo service exposing the HS Classification skill.

Folders:
- `hs_service/` — A minimal Flask service that wraps the HS Classification skill for demo and customer trials.

Run the demo service locally:

```bash
python product/hs_service/app.py
```

Then POST JSON to `http://127.0.0.1:5005/classify` with fields: `product_name`, `product_description`, `country`, `trade_direction`, `product_attributes`.
