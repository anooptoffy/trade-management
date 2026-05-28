---
name: webscraping
description: Extract product data, tariff information, and compliance requirements from web sources to enhance HS classification. Use this skill when you need to gather product specifications, manufacturer details, material composition, regulatory certifications, or real-time tariff rates from websites. This skill is designed for integrating scraping-based enrichment into HS classification workflows.
---

# Webscraping Skill for HS Classification

## Purpose

This skill helps collect and normalize product data from web sources to improve HS classification accuracy. It is intended for cases where user-provided product details are incomplete and additional specification, origin, material, or compliance data is required.

## When to Use

Use this skill when:

- The product description is sparse or missing key attributes
- You need to verify material, weight, or origin details
- You want to enrich classification with manufacturer or supplier specifications
- You need region-specific compliance requirements from official sources
- You want to compare current tariff rates against static rule data

## What It Does

- Scrapes structured and unstructured web pages for product details
- Extracts data from HTML content, JSON-LD, and dynamic JS content
- Generates a concise summary section from scraped pages when product detail is insufficient
- Collects relevant links and image URLs discovered during scraping
- Validates and normalizes scraped material, weight, origin, and descriptions
- Converts scraped details into HS classification inputs
- Provides patterns for tariff and compliance data retrieval

## Concise Summary Output

When user-provided product details are insufficient, this skill should:

1. Search or scrape trusted sources based on the available product information
2. Extract the most relevant product description and specification text
3. Produce a short summary paragraph that explains the scraped findings
4. Return a list of source links and any image URLs found on the scraped pages

This output is meant to be a concise evidence summary, not a full page dump.

## Supported Scraping Patterns

1. HTML parsing with BeautifulSoup
2. JSON-LD extraction from page scripts
3. Selenium browser automation for JavaScript-heavy pages
4. API-based retrieval for tariff and official trade databases
5. Data validation and normalization for scraped fields

## Integration

Use the scraped data to populate classification fields such as:

- `material`
- `origin_country`
- `weight_kg`
- `product_description`
- `product_attributes`

Then pass enriched data into the HS classification engine for a more accurate result.

When user input is sparse, the skill can also search trusted web sources and generate a concise scraped summary instead of failing due to missing details.

## Classification Workflow

When this skill is used for classification, follow these steps:

1. **Receive the product input** from the user.
2. **Decide if input is sufficient**. If key fields are missing, initiate web enrichment.
3. **Search or scrape web sources** using the product name, category, or URL.
4. **Extract the strongest evidence**: descriptions, material details, weight, origin, and compliance notes.
5. **Collect links and image URLs** to document where the information came from.
6. **Normalize scraped data** into classification fields.
7. **Enrich the HS classification request** with both user data and scraped attributes.
8. **Run the HS classifier** and return the result with a concise scraping summary.

This workflow ensures classification uses the best available evidence instead of failing only because the initial input was insufficient.

## Files

- `scripts/scraper_helpers.py` — helper utilities for scraping, validation, caching, and safe request handling
- `references/scraping-sources.md` — source-specific scraping patterns and examples

## Dependencies

Install the following packages when using this skill:

```bash
pip install requests beautifulsoup4 lxml selenium
```

## Example concise scraping output

```json
{
  "summary": "Scraped product details show this item is a lightweight plastic smartphone accessory with CE and FCC compliance references.",
  "source_links": [
    "https://example.com/product/12345",
    "https://manufacturer.com/specs/xyz"
  ],
  "image_urls": [
    "https://example.com/images/product-main.jpg",
    "https://example.com/images/product-detail.jpg"
  ],
  "material": "plastic",
  "weight_kg": 0.2,
  "origin_country": "China"
}
```

## Notes

- Always respect `robots.txt` and website terms of service.
- Cache scraped results and add retry logic to avoid rate limiting.
- For dynamic pages, prefer Selenium or browser automation.
