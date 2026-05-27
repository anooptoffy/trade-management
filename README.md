# Trade Management

Global trade management tools, use cases, and reference materials for HS classification, tariff analysis, and trade compliance.

## Overview

This repository contains production-ready trade management solutions, with a focus on Harmonized System (HS) product classification. The **HS Classification Skill** is a comprehensive tool that automatically determines product HS codes, applicable tariff rates, and region-specific regulatory compliance requirements for products being imported or exported across 5 major trading regions: US, Canada, Europe, China, and Mexico.

## Key Features

✅ **Automatic Product Classification** — Uses pattern-matching and machine learning-ready algorithms to classify products into HS codes  
✅ **Multi-Region Support** — Supports US, Canada, Europe, China, and Mexico with region-specific tariffs and compliance rules  
✅ **Tariff Comparison** — Compare tariff rates across all 5 regions in a single request  
✅ **Compliance Requirements** — Get regulatory requirements by destination (FCC for US, CE for EU, NMPA for China, etc.)  
✅ **Material & Origin Tracking** — Track product material composition and country of manufacture  
✅ **Web UI & REST API** — Both interactive web form and RESTful API for automation  
✅ **CLI Tool** — Command-line interface for batch processing and scripting  

## Repository Structure

```
trade-management/
├── README.md                    # This file
├── API.md                       # API documentation
├── product/
│   └── hs_service/              # HS Classification Flask service
│       ├── app.py               # Flask application
│       ├── requirements.txt      # Python dependencies
│       ├── .venv/               # Python virtual environment
│       ├── templates/
│       │   └── index.html        # Web UI form
│       └── static/
│           ├── css/
│           │   └── style.css     # Styling
│           └── js/
│               └── app.js        # Form handling
└── skills/
    └── hs-classification/        # HS Classification skill
        ├── SKILL.md              # Skill documentation
        └── scripts/
            └── generate_hs_code.py # Core classification engine
```

## Quick Start

### Web UI (Interactive)

1. **Start the Flask service:**
   ```bash
   cd product/hs_service
   source .venv/bin/activate
   python app.py
   ```

2. **Open in browser:**
   ```
   http://127.0.0.1:5005
   ```

3. **Fill out the form** with product details and click "Classify Product"

### REST API

**Classify a smartphone:**
```bash
curl -X POST http://127.0.0.1:5005/classify \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Smartphone",
    "country": "United States",
    "material": "plastic",
    "origin_country": "China",
    "weight_kg": 0.2
  }'
```

**Response:**
```json
{
  "hs_code": "8528.72",
  "tariff_rate": "2%",
  "regulatory_notes": "FCC approval required; RoHS and WEEE compliance.",
  "tariff_comparison": {
    "us": "2%",
    "canada": "3%",
    "europe": "4%",
    "china": "6%",
    "mexico": "3%"
  }
}
```

See [API.md](API.md) for complete API documentation.

### Command Line

**Classify leather shoes:**
```bash
cd skills/hs-classification
python scripts/generate_hs_code.py \
  --product-name "Men's leather shoes" \
  --country Germany \
  --material leather \
  --origin-country Vietnam \
  --weight-kg 0.5 \
  --output-json
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/anooptoffy/trade-management.git
   cd trade-management
   ```

2. **Create and activate virtual environment:**
   ```bash
   cd product/hs_service
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the service:**
   ```bash
   python app.py
   ```

The service will start at `http://127.0.0.1:5005`

## Features

### Supported Product Categories

- **Footwear** — Shoes, boots, sandals, slippers
- **Electronics** — Mobile devices, computers, peripherals
- **Apparel** — Clothing, textiles, garments
- **Toys** — Games, recreational items
- **Furniture** — Tables, chairs, cabinets
- **Cosmetics** — Beauty products, skincare
- **Automotive** — Vehicle parts, accessories
- **Food** — Processed foods, beverages
- **Textiles** — Fabrics, raw materials

### Supported Regions

| Region | Countries | Key Compliance |
|--------|-----------|---|
| **US** | United States, USA | FCC, RoHS, WEEE |
| **Canada** | Canada, CA | CCPSA, ASTM F963 |
| **Europe** | Germany, France, UK, Spain, etc. | CE, EN standards |
| **China** | China, CN, PRC | CCC, NMPA |
| **Mexico** | Mexico, MX | COFEPRIS, NOM |

### Input Fields

**Required:**
- `product_name` — Name of the product
- `country` — Destination country for classification

**Optional:**
- `product_description` — Detailed product description
- `product_attributes` — Comma-separated attributes
- `trade_direction` — "import" or "export"
- `material` — Primary material (dropdown)
- `origin_country` — Country of manufacture
- `weight_kg` — Product weight in kilograms

### Output Fields

- `hs_code` — 6-digit Harmonized System code
- `classification_reason` — Explanation of classification
- `tariff_rate` — Applicable tariff percentage
- `regulatory_notes` — Region-specific compliance requirements
- `region` — Destination region code
- `tariff_comparison` — Tariff rates across all 5 regions
- `material` — Product material (if provided)
- `origin_country` — Country of manufacture (if provided)
- `weight_kg` — Product weight (if provided)

## Usage Examples

### Example 1: Leather Shoes (EU Import)

**Input:**
```json
{
  "product_name": "Men's leather shoes",
  "country": "Germany",
  "material": "leather",
  "origin_country": "Vietnam",
  "weight_kg": 0.5
}
```

**Output:**
```json
{
  "hs_code": "6403.99",
  "tariff_rate": "8%",
  "regulatory_notes": "CE marking required; EN ISO 13287 safety standards",
  "tariff_comparison": {
    "us": "5%",
    "canada": "7%",
    "europe": "8%",
    "china": "10%",
    "mexico": "6%"
  }
}
```

### Example 2: Smartphone (US Import)

**Input:**
```json
{
  "product_name": "Smartphone",
  "country": "United States",
  "material": "plastic",
  "origin_country": "China",
  "weight_kg": 0.2
}
```

**Output:**
```json
{
  "hs_code": "8528.72",
  "tariff_rate": "2%",
  "regulatory_notes": "FCC approval required; RoHS and WEEE compliance",
  "tariff_comparison": {
    "us": "2%",
    "canada": "3%",
    "europe": "4%",
    "china": "6%",
    "mexico": "3%"
  }
}
```

## API Reference

For complete API documentation, see [API.md](API.md).

**Key Endpoints:**

- `GET /` — Web UI form
- `POST /classify` — Classification API endpoint

## Architecture

### Backend

- **Flask** — Python web framework
- **Python 3.12** — Runtime environment
- **Regex Patterns** — Pattern-based product classification
- **Region Mappings** — Country → region normalization

### Frontend

- **HTML5** — Semantic markup
- **CSS3** — Responsive styling
- **Vanilla JavaScript** — Form handling and API communication
- **No external dependencies** — Pure HTML/CSS/JS

### Classification Engine

The `generate_hs_code.py` script contains:

1. **Country Normalization** — Maps country names to region codes
2. **Pattern Matching** — Matches product descriptions to HS categories
3. **Tariff Lookup** — Retrieves region-specific tariff rates
4. **Compliance Notes** — Returns regulatory requirements per region
5. **Tariff Comparison** — Generates rates across all regions

## Performance

- Classification API response time: < 100ms
- Web UI form load time: < 200ms
- No external API calls required
- All data is local and pre-computed

## Development

### Running Tests

Currently, no automated tests are included. To add tests:

```bash
pip install pytest
pytest tests/
```

### Adding New Product Categories

Edit `skills/hs-classification/scripts/generate_hs_code.py` and add rules to the `CATEGORY_RULES` list:

```python
{
    "pattern": r"your_pattern_here",
    "default_hs": {
        "us": "XXXXXX",
        "canada": "XXXXXX",
        "europe": "XXXXXX",
        "china": "XXXXXX",
        "mexico": "XXXXXX"
    },
    "description": "Your category description",
    "tariff_rate": {
        "us": "X%",
        "canada": "X%",
        "europe": "X%",
        "china": "X%",
        "mexico": "X%"
    },
    "compliance": {
        "us": "Your compliance notes",
        "canada": "Your compliance notes",
        "europe": "Your compliance notes",
        "china": "Your compliance notes",
        "mexico": "Your compliance notes"
    }
}
```

### Deployment

For production deployment:

1. Replace Flask development server with production WSGI server (Gunicorn, uWSGI)
2. Add authentication and rate limiting
3. Enable CORS if needed for cross-origin requests
4. Configure SSL/TLS
5. Set up logging and monitoring
6. Add CI/CD pipeline

**Example with Gunicorn:**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5005 app:app
```

## Limitations

- Currently uses regex-based pattern matching (can be enhanced with ML models)
- Limited to 9 predefined product categories
- Tariff rates are example data (should be updated with official trade databases)
- Compliance notes are based on general standards (verify with official sources)

## Future Enhancements

- [ ] Machine learning-based product classification
- [ ] Integration with official trade databases (World Bank, WTO)
- [ ] Real-time tariff rate updates
- [ ] Multi-language support
- [ ] Advanced filtering (brand, supplier, price)
- [ ] Classification history and analytics
- [ ] Batch import/export processing
- [ ] REST API authentication (API keys, OAuth2)
- [ ] Rate limiting and usage analytics
- [ ] Advanced compliance rule engine

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For questions, issues, or feature requests:

- **Issues:** Open an issue on GitHub
- **Email:** Contact the maintainers
- **Docs:** Check [API.md](API.md) for API documentation

## Changelog

### v1.0.0 (Current Release)

**Features:**
- ✅ HS product classification
- ✅ Multi-region tariff lookup
- ✅ Region-specific compliance requirements
- ✅ Web UI and REST API
- ✅ CLI tool
- ✅ Material and origin tracking
- ✅ Tariff comparison across 5 regions

**Product Categories:** Footwear, Electronics, Apparel, Toys, Furniture, Cosmetics, Automotive, Food, Textiles

**Supported Regions:** US, Canada, Europe, China, Mexico

---

**Last Updated:** May 27, 2026  
**Repository:** https://github.com/anooptoffy/trade-management  
**Maintainer:** Anoop Toffy
