---
name: HS Classification
description: Classify a product as per the country of import or export.
---

# HS Classification

Classify a product as per the country of import or export.

## Purpose

Use this skill to determine the correct Harmonized System (HS) code for a product based on trade direction, country, and product attributes. It supports classification for major regions including the US, Canada, Europe, China, and Mexico.

## Supported regions

- United States
- Canada
- Europe
- China
- Mexico

## Inputs

- `product_name`
- `product_description`
- `country`
- `trade_direction` (import or export)
- `product_attributes`

## Outputs

- `hs_code`
- `classification_reason`
- `tariff_rate`
- `regulatory_notes`
- `region`

## Example

Input:
- product_name: "Men's leather shoes"
- country: "Germany"
- trade_direction: "import"
- product_attributes: "men's footwear, leather upper, retail pack"

Output:
- hs_code: "6403.99"
- classification_reason: "Men's or women's footwear falls under chapter 64 for most regions and is therefore classified as HS 6403.99."
- tariff_rate: "8%"
- regulatory_notes: "For import into Germany, verify EU customs declaration and labeling requirements."
- region: "Europe"

## Script support

A starter classification script is included at `skills/hs-classification/scripts/generate_hs_code.py`.

### Run example

```bash
python skills/hs-classification/scripts/generate_hs_code.py \
  --product-name "Men's leather shoes" \
  --product-description "Premium men leather footwear" \
  --country Germany \
  --trade-direction import \
  --product-attributes "leather upper, retail pack" \
  --output-json
```
