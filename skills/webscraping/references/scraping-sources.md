# Scraping Sources and Examples

This reference file contains real-world scraping patterns and examples for web sources commonly used to enrich HS classification data.

## Amazon Product Pages

- Use `extract_json_ld` to parse structured data in Amazon pages.
- Scrape `span#productTitle` for the product name.
- Extract key specifications from HTML tables or bullets.
- Validate weight, material, and origin fields after scraping.

## Alibaba Product Listings

- Use HTML parsing to extract supplier details and product attributes.
- Look for `div.search-attr-list-item` containers and parse label/value pairs.
- Extract MOQ, supplier location, and certifications from supplier info.

## eBay Listings

- Scrape `span#itemTitle` for product name.
- Parse item specifics from `td.label` / `td.value` pairs.
- Capture seller location and shipping country as origin indicators.

## Official Manufacturer Sites

- Use generic selectors like `h1.product-name`, `h1.title`, or `[data-product-name]`.
- Parse tables and definition lists (`<table>`, `<dt>/<dd>`) for full spec sheets.
- Use JSON-LD if present to obtain structured product metadata.

## Tariff Databases

- Prefer APIs where available (World Bank WITS, USITC, TARIC).
- If scraping is required, identify the relevant table or JSON endpoint.
- Use country and HS code filters to retrieve applicable tariff rates.

## Compliance Databases

- FCC, NANDO, NMPA, and COFEPRIS often require specialized scraping logic.
- Search for product names and classification terms to locate certification records.
- Scrape summary cards or result tables rather than raw HTML blobs.

## Best Practices

- Respect robots.txt and site terms of service.
- Use randomized `User-Agent` headers.
- Implement exponential backoff for HTTP 429 and transient server errors.
- Cache results to reduce repeated site load.
- Keep scraping focused on the exact fields needed for classification.
