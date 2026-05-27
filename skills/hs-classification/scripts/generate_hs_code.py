import argparse
import json
import re

REGION_COUNTRIES = {
    "us": ["united states", "usa", "us"],
    "canada": ["canada", "ca"],
    "europe": ["germany", "france", "italy", "spain", "netherlands", "eu", "europe"],
    "china": ["china", "cn"],
    "mexico": ["mexico", "mx"],
}

CATEGORY_RULES = [
    {
        "pattern": r"(shoe|footwear|boot|sneaker|sandals)",
        "default_hs": {
            "us": "6403.99",
            "canada": "6403.99",
            "europe": "6403.99",
            "china": "6403.99",
            "mexico": "6403.99",
        },
        "description": "Men's or women's footwear falls under chapter 64 for most regions.",
        "tariff_rate": {"us": "3%", "canada": "4%", "europe": "8%", "china": "10%", "mexico": "5%"},
    },
    {
        "pattern": r"(phone|tablet|laptop|electronic|charger|adapter|monitor)",
        "default_hs": {
            "us": "8528.72",
            "canada": "8528.72",
            "europe": "8528.72",
            "china": "8528.72",
            "mexico": "8528.72",
        },
        "description": "Electronic devices are usually classified under chapter 85.",
        "tariff_rate": {"us": "2%", "canada": "3%", "europe": "4%", "china": "6%", "mexico": "3%"},
    },
    {
        "pattern": r"(jacket|shirt|dress|pants|jeans|apparel|clothing)",
        "default_hs": {
            "us": "6203.29",
            "canada": "6203.29",
            "europe": "6203.29",
            "china": "6203.29",
            "mexico": "6203.29",
        },
        "description": "Apparel is generally classified under chapter 62 for apparel articles.",
        "tariff_rate": {"us": "7%", "canada": "8%", "europe": "10%", "china": "12%", "mexico": "9%"},
    },
    {
        "pattern": r"(toy|game|puzzle|doll|action figure)",
        "default_hs": {
            "us": "9503.00",
            "canada": "9503.00",
            "europe": "9503.00",
            "china": "9503.00",
            "mexico": "9503.00",
        },
        "description": "Toys and games are usually classified under chapter 95.",
        "tariff_rate": {"us": "4%", "canada": "5%", "europe": "6%", "china": "8%", "mexico": "5%"},
    },
    {
        "pattern": r"(furniture|chair|table|sofa|couch)",
        "default_hs": {
            "us": "9403.60",
            "canada": "9403.60",
            "europe": "9403.60",
            "china": "9403.60",
            "mexico": "9403.60",
        },
        "description": "Household furniture is typically classified under chapter 94.",
        "tariff_rate": {"us": "5%", "canada": "6%", "europe": "7%", "china": "9%", "mexico": "6%"},
    },
    {
        "pattern": r"(cosmetic|makeup|skincare|lotion|perfume)",
        "default_hs": {
            "us": "3304.99",
            "canada": "3304.99",
            "europe": "3304.99",
            "china": "3304.99",
            "mexico": "3304.99",
        },
        "description": "Cosmetics and skincare products are covered under chapter 33.",
        "tariff_rate": {"us": "6%", "canada": "7%", "europe": "8%", "china": "12%", "mexico": "7%"},
    },
    {
        "pattern": r"(car|auto|vehicle|motor|engine|spare part)",
        "default_hs": {
            "us": "8708.99",
            "canada": "8708.99",
            "europe": "8708.99",
            "china": "8708.99",
            "mexico": "8708.99",
        },
        "description": "Automotive components are often classified under chapter 87.",
        "tariff_rate": {"us": "2%", "canada": "3%", "europe": "4%", "china": "7%", "mexico": "3%"},
    },
    {
        "pattern": r"(food|snack|beverage|chocolate|coffee|tea)",
        "default_hs": {
            "us": "2106.90",
            "canada": "2106.90",
            "europe": "2106.90",
            "china": "2106.90",
            "mexico": "2106.90",
        },
        "description": "Packaged food products are typically classified under chapter 21.",
        "tariff_rate": {"us": "2%", "canada": "3%", "europe": "5%", "china": "6%", "mexico": "4%"},
    },
]

DEFAULT_REGION = "europe"
DEFAULT_HS = "9999.99"
DEFAULT_TARIFF = "varies by region"


def normalize_country(country_value: str) -> str:
    normalized = country_value.strip().lower()
    for region, countries in REGION_COUNTRIES.items():
        if normalized in countries:
            return region
    return DEFAULT_REGION


def find_category(product_name: str, description: str, attributes: str) -> dict:
    text = " ".join([product_name, description, attributes]).lower()
    for rule in CATEGORY_RULES:
        if re.search(rule["pattern"], text):
            return rule
    return {}


def classify(product_name: str, product_description: str, country: str, trade_direction: str, product_attributes: str) -> dict:
    region = normalize_country(country)
    rule = find_category(product_name, product_description, product_attributes)
    if rule:
        hs_code = rule["default_hs"].get(region, DEFAULT_HS)
        tariff_rate = rule["tariff_rate"].get(region, DEFAULT_TARIFF)
        classification_reason = (
            f"The product matches '{rule['description']}' for {region.title()} and is therefore classified as HS {hs_code}."
        )
    else:
        hs_code = DEFAULT_HS
        tariff_rate = DEFAULT_TARIFF
        classification_reason = (
            "Insufficient detail was available to map the product to a specific HS chapter. "
            "Please refine the description or provide detailed product attributes."
        )

    regulatory_notes = (
        f"For {trade_direction.lower()} into {country.title()}, verify country-specific customs requirements, labeling, and any trade agreement rules."
    )

    return {
        "hs_code": hs_code,
        "classification_reason": classification_reason,
        "tariff_rate": tariff_rate,
        "regulatory_notes": regulatory_notes,
        "region": region,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="HS Classification generator for trade management use cases.")
    parser.add_argument("--product-name", required=True)
    parser.add_argument("--product-description", default="")
    parser.add_argument("--country", required=True)
    parser.add_argument("--trade-direction", choices=["import", "export"], default="import")
    parser.add_argument("--product-attributes", default="")
    parser.add_argument("--output-json", action="store_true", help="Print output as JSON.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = classify(
        product_name=args.product_name,
        product_description=args.product_description,
        country=args.country,
        trade_direction=args.trade_direction,
        product_attributes=args.product_attributes,
    )

    if args.output_json:
        print(json.dumps(result, indent=2))
    else:
        print("HS Code:", result["hs_code"])
        print("Reason:", result["classification_reason"])
        print("Tariff Rate:", result["tariff_rate"])
        print("Regulatory Notes:", result["regulatory_notes"])
        print("Region:", result["region"].title())


if __name__ == "__main__":
    main()
