# HS Classification API Documentation

## Overview

The HS Classification API provides real-time product classification with harmonized system (HS) codes, tariff rates, and region-specific compliance requirements. The API supports multiple product categories across 5 major regions: US, Canada, Europe, China, and Mexico.

## Base URL

```
http://127.0.0.1:5005
```

## Authentication

Currently, no authentication is required for API access. Production deployments should implement API key authentication or OAuth2.

## Endpoints

### 1. GET /

Returns the web UI form for interactive product classification.

**Response:** HTML page with classification form

---

### 2. POST /classify

Classifies a product and returns HS code, tariff rates, and compliance requirements.

#### Request

**Method:** `POST`  
**Content-Type:** `application/json`

#### Request Body

```json
{
  "product_name": "string (required)",
  "country": "string (required)",
  "product_description": "string (optional)",
  "product_attributes": "string (optional, comma-separated)",
  "trade_direction": "string (optional, 'import' or 'export')",
  "material": "string (optional)",
  "origin_country": "string (optional)",
  "weight_kg": "number (optional)"
}
```

#### Request Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `product_name` | string | Yes | Name of the product | "Men's leather shoes" |
| `country` | string | Yes | Destination/source country for classification | "Germany", "United States" |
| `product_description` | string | No | Detailed product description | "Premium leather oxford shoes with rubber sole" |
| `product_attributes` | string | No | Comma-separated product attributes | "leather upper, rubber sole, lace-up" |
| `trade_direction` | string | No | Import or Export (default: "import") | "import", "export" |
| `material` | string | No | Primary material | "leather", "synthetic", "cotton", "polyester", "metal", "plastic", "wood", "rubber", "ceramic" |
| `origin_country` | string | No | Country where product is manufactured | "Vietnam", "China", "Germany" |
| `weight_kg` | number | No | Product weight in kilograms | 0.5, 2.5 |

#### Response

**Status Code:** `200 OK`

```json
{
  "hs_code": "string",
  "classification_reason": "string",
  "tariff_rate": "string",
  "regulatory_notes": "string",
  "region": "string",
  "tariff_comparison": {
    "us": "string",
    "canada": "string",
    "europe": "string",
    "china": "string",
    "mexico": "string"
  },
  "material": "string",
  "origin_country": "string",
  "weight_kg": "number",
  "product_name": "string",
  "product_description": "string",
  "product_attributes": "string"
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `hs_code` | string | 6-digit Harmonized System code for the product |
| `classification_reason` | string | Explanation of how the product was classified |
| `tariff_rate` | string | Applicable tariff rate for the destination region |
| `regulatory_notes` | string | Region-specific compliance and regulatory requirements |
| `region` | string | Destination region code (us, canada, europe, china, mexico) |
| `tariff_comparison` | object | Tariff rates across all 5 supported regions |
| `material` | string | Primary material of the product (if provided) |
| `origin_country` | string | Country of manufacture (if provided) |
| `weight_kg` | number | Product weight in kilograms (if provided) |
| `product_name` | string | Original product name from request |
| `product_description` | string | Original product description from request |
| `product_attributes` | string | Original product attributes from request |

#### Error Response

**Status Code:** `400 Bad Request`

```json
{
  "error": "Missing required field: product_name"
}
```

---

## Supported Product Categories

The API classifies products into the following categories:

1. **Footwear** - Shoes, boots, sandals, slippers
2. **Electronics** - Mobile devices, computers, accessories
3. **Apparel** - Clothing, textiles, garments
4. **Toys** - Toys, games, recreational items
5. **Furniture** - Tables, chairs, cabinets, home furnishings
6. **Cosmetics** - Beauty products, skincare, makeup
7. **Automotive** - Vehicle parts, accessories
8. **Food** - Processed foods, beverages, condiments
9. **Textiles** - Fabrics, materials, cloth

---

## Supported Regions

| Region | Country Examples |
|--------|------------------|
| **US** | United States, USA, US |
| **Canada** | Canada, CA |
| **Europe** | Germany, France, Italy, UK, Spain, etc. |
| **China** | China, CN, PRC |
| **Mexico** | Mexico, MX |

---

## Examples

### Example 1: Leather Shoes Classification

**Request:**
```bash
curl -X POST http://127.0.0.1:5005/classify \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Men'\''s leather shoes",
    "country": "Germany",
    "product_description": "Premium leather oxford shoes",
    "product_attributes": "leather upper, rubber sole, lace-up",
    "material": "leather",
    "origin_country": "Vietnam",
    "weight_kg": 0.5
  }'
```

**Response:**
```json
{
  "hs_code": "6403.99",
  "classification_reason": "Leather footwear classification",
  "tariff_rate": "8%",
  "regulatory_notes": "For import into Europe: CE marking required; EN ISO 13287 safety standards; No specific chemicals restrictions beyond EU standards.",
  "region": "europe",
  "tariff_comparison": {
    "us": "5%",
    "canada": "7%",
    "europe": "8%",
    "china": "10%",
    "mexico": "6%"
  },
  "material": "leather",
  "origin_country": "Vietnam",
  "weight_kg": 0.5,
  "product_name": "Men's leather shoes",
  "product_description": "Premium leather oxford shoes",
  "product_attributes": "leather upper, rubber sole, lace-up"
}
```

### Example 2: Smartphone Classification

**Request:**
```bash
curl -X POST http://127.0.0.1:5005/classify \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Smartphone",
    "country": "United States",
    "product_description": "Android smartphone with 5G capability",
    "material": "plastic",
    "origin_country": "China",
    "weight_kg": 0.2
  }'
```

**Response:**
```json
{
  "hs_code": "8528.72",
  "classification_reason": "Mobile phone classification",
  "tariff_rate": "2%",
  "regulatory_notes": "For import into United States: FCC approval required; RoHS and WEEE compliance.",
  "region": "us",
  "tariff_comparison": {
    "us": "2%",
    "canada": "3%",
    "europe": "4%",
    "china": "6%",
    "mexico": "3%"
  },
  "material": "plastic",
  "origin_country": "China",
  "weight_kg": 0.2,
  "product_name": "Smartphone",
  "product_description": "Android smartphone with 5G capability"
}
```

### Example 3: Toy Classification

**Request:**
```bash
curl -X POST http://127.0.0.1:5005/classify \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Wooden toy train",
    "country": "Canada",
    "product_attributes": "wooden construction, for children ages 3+",
    "material": "wood",
    "origin_country": "Germany",
    "weight_kg": 1.5
  }'
```

**Response:**
```json
{
  "hs_code": "9503.00",
  "classification_reason": "Toy classification",
  "tariff_rate": "0%",
  "regulatory_notes": "For import into Canada: Toy Safety Standards compliance (CCPSA); ASTM F963 safety requirements.",
  "region": "canada",
  "tariff_comparison": {
    "us": "0%",
    "canada": "0%",
    "europe": "0%",
    "china": "10%",
    "mexico": "0%"
  },
  "material": "wood",
  "origin_country": "Germany",
  "weight_kg": 1.5,
  "product_name": "Wooden toy train",
  "product_attributes": "wooden construction, for children ages 3+"
}
```

---

## Error Handling

### Missing Required Fields

**Status Code:** `400 Bad Request`

**Response:**
```json
{
  "error": "Missing required field: product_name"
}
```

### Invalid Request

**Status Code:** `400 Bad Request`

**Response:**
```json
{
  "error": "Invalid request: weight_kg must be a number"
}
```

### Server Error

**Status Code:** `500 Internal Server Error`

**Response:**
```json
{
  "error": "An error occurred during classification"
}
```

---

## Rate Limiting

Currently, no rate limiting is enforced. Production deployments should implement appropriate rate limiting based on deployment requirements.

---

## CORS

CORS headers are not currently configured. For browser-based API access, CORS should be enabled in production deployments.

---

## Changelog

### v1.0.0 (Current)
- Initial API release
- Support for 9 product categories
- 5-region tariff and compliance data
- Material, origin, and weight tracking
- Tariff comparison across regions

---

## Support

For issues, feature requests, or questions about the API, please refer to the main [README.md](README.md) file or contact the development team.
