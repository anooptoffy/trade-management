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
- Validates and normalizes scraped material, weight, origin, and descriptions
- Converts scraped details into HS classification inputs
- Provides patterns for tariff and compliance data retrieval

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

## Files

- `scripts/scraper_helpers.py` — helper utilities for scraping, validation, caching, and safe request handling
- `references/scraping-sources.md` — source-specific scraping patterns and examples

## Dependencies

Install the following packages when using this skill:

```bash
pip install requests beautifulsoup4 lxml selenium
```

## Notes

- Always respect `robots.txt` and website terms of service.
- Cache scraped results and add retry logic to avoid rate limiting.
- For dynamic pages, prefer Selenium or browser automation.
