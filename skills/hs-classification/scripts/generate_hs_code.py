import argparse
import json
import re
from typing import Dict, List, Optional

REGION_COUNTRIES = {
    "us": ["united states", "usa", "us"],
    "canada": ["canada", "ca"],
    "europe": ["germany", "france", "italy", "spain", "netherlands", "eu", "europe"],
    "china": ["china", "cn"],
    "mexico": ["mexico", "mx"],
}

PRODUCT_CATEGORIES = [
    "footwear",
    "apparel",
    "electronics",
    "toys",
    "furniture",
    "cosmetics",
    "automotive",
    "food",
    "textiles",
    "machinery",
    "chemicals",
]

MATERIALS = ["leather", "synthetic", "cotton", "polyester", "metal", "plastic", "wood", "rubber", "ceramic"]

CATEGORY_RULES = [
    {
        "pattern": r"(shoe|footwear|boot|sneaker|sandals|loafer)",
        "default_hs": {
            "us": "6403.99",
            "canada": "6403.99",
            "europe": "6403.99",
            "china": "6403.99",
            "mexico": "6403.99",
        },
        "description": "Footwear falls under chapter 64 for most regions.",
        "tariff_rate": {"us": "3%", "canada": "4%", "europe": "8%", "china": "10%", "mexico": "5%"},
        "compliance": {
            "us": "Must meet CPSC standards; labeling in English required.",
            "canada": "Canadian footwear regulations; country of origin marking.",
            "europe": "EU shoe labeling directive; safety standards EN ISO 13287.",
            "china": "QS mark not required for imported goods; HS code verification.",
            "mexico": "Mexican product safety requirements; Spanish labeling.",
        },
    },
    {
        "pattern": r"(phone|tablet|laptop|electronic|charger|adapter|monitor|computer)",
        "default_hs": {
            "us": "8528.72",
            "canada": "8528.72",
            "europe": "8528.72",
            "china": "8528.72",
            "mexico": "8528.72",
        },
        "description": "Electronic devices are usually classified under chapter 85.",
        "tariff_rate": {"us": "2%", "canada": "3%", "europe": "4%", "china": "6%", "mexico": "3%"},
        "compliance": {
            "us": "FCC approval required; RoHS and WEEE compliance.",
            "canada": "ISED (Innovation, Science, and Economic Development) certification.",
            "europe": "CE marking; RoHS Directive 2011/65/EU; WEEE registration.",
            "china": "CCC mark may be required; energy efficiency standards.",
            "mexico": "FCC approval accepted; NOM standards for some devices.",
        },
    },
    {
        "pattern": r"(jacket|shirt|dress|pants|jeans|apparel|clothing|blouse|sweater)",
        "default_hs": {
            "us": "6203.29",
            "canada": "6203.29",
            "europe": "6203.29",
            "china": "6203.29",
            "mexico": "6203.29",
        },
        "description": "Apparel is generally classified under chapter 62.",
        "tariff_rate": {"us": "7%", "canada": "8%", "europe": "10%", "china": "12%", "mexico": "9%"},
        "compliance": {
            "us": "Country of origin labeling; CPSIA compliance for children's items.",
            "canada": "Bilingual labeling (English/French); fiber content disclosure.",
            "europe": "Care labeling per EN ISO 3758; textile fiber composition.",
            "china": "Fiber composition labeling; GB standards for certain items.",
            "mexico": "Spanish language labeling; country of origin required.",
        },
    },
    {
        "pattern": r"(toy|game|puzzle|doll|action figure|playset)",
        "default_hs": {
            "us": "9503.00",
            "canada": "9503.00",
            "europe": "9503.00",
            "china": "9503.00",
            "mexico": "9503.00",
        },
        "description": "Toys and games are usually classified under chapter 95.",
        "tariff_rate": {"us": "4%", "canada": "5%", "europe": "6%", "china": "8%", "mexico": "5%"},
        "compliance": {
            "us": "CPSIA compliance; choking hazard warnings; phthalate restrictions.",
            "canada": "Canadian Toy Regulations; ASTM F963-17 compliance.",
            "europe": "CE marking required; EN 71 safety standards.",
            "china": "CCC mark for certain toys; GB 6675 standard.",
            "mexico": "CPSC compliance accepted; NOM product safety standards.",
        },
    },
    {
        "pattern": r"(furniture|chair|table|sofa|couch|desk|cabinet|shelf)",
        "default_hs": {
            "us": "9403.60",
            "canada": "9403.60",
            "europe": "9403.60",
            "china": "9403.60",
            "mexico": "9403.60",
        },
        "description": "Household furniture is typically classified under chapter 94.",
        "tariff_rate": {"us": "5%", "canada": "6%", "europe": "7%", "china": "9%", "mexico": "6%"},
        "compliance": {
            "us": "CPSC regulations for children's furniture; flammability standards.",
            "canada": "Furniture and Fixtures Regulations; stability standards.",
            "europe": "EN 17436 stability requirements; allergen labeling.",
            "china": "Environmental certification; formaldehyde limits.",
            "mexico": "Mexican furniture safety standards; material certification.",
        },
    },
    {
        "pattern": r"(cosmetic|makeup|skincare|lotion|perfume|shampoo|soap|deodorant)",
        "default_hs": {
            "us": "3304.99",
            "canada": "3304.99",
            "europe": "3304.99",
            "china": "3304.99",
            "mexico": "3304.99",
        },
        "description": "Cosmetics and skincare products are covered under chapter 33.",
        "tariff_rate": {"us": "6%", "canada": "7%", "europe": "8%", "china": "12%", "mexico": "7%"},
        "compliance": {
            "us": "FDA cosmetic registration; ingredient disclosure; facility inspection.",
            "canada": "Health Canada cosmetic registration; approved ingredient lists.",
            "europe": "EU Cosmetics Regulation (EC 1223/2009); restricted substances.",
            "china": "NMPA registration required; animal testing restrictions.",
            "mexico": "COFEPRIS authorization; ingredient restrictions.",
        },
    },
    {
        "pattern": r"(car|auto|vehicle|motor|engine|spare part|battery|tire)",
        "default_hs": {
            "us": "8708.99",
            "canada": "8708.99",
            "europe": "8708.99",
            "china": "8708.99",
            "mexico": "8708.99",
        },
        "description": "Automotive components are often classified under chapter 87.",
        "tariff_rate": {"us": "2%", "canada": "3%", "europe": "4%", "china": "7%", "mexico": "3%"},
        "compliance": {
            "us": "DOT standards; EPA emissions compliance; NHTSA safety standards.",
            "canada": "Transport Canada Motor Vehicle Safety Standards (CMVSS).",
            "europe": "EU automotive regulations; CE marking for certain components.",
            "china": "CCC certification for certain parts; CATARC testing.",
            "mexico": "FMVSS accepted; NOM automotive standards.",
        },
    },
    {
        "pattern": r"(food|snack|beverage|chocolate|coffee|tea|candy|nuts)",
        "default_hs": {
            "us": "2106.90",
            "canada": "2106.90",
            "europe": "2106.90",
            "china": "2106.90",
            "mexico": "2106.90",
        },
        "description": "Packaged food products are typically classified under chapter 21.",
        "tariff_rate": {"us": "2%", "canada": "3%", "europe": "5%", "china": "6%", "mexico": "4%"},
        "compliance": {
            "us": "FDA food labeling; allergen disclosure; nutrition facts required.",
            "canada": "Health Canada food labeling; bilingual packaging required.",
            "europe": "EU food regulation (1169/2011); allergen warnings mandatory.",
            "china": "NMPA import registration; ingredient list in Chinese.",
            "mexico": "COFEPRIS food authorization; Spanish labeling required.",
        },
    },
    {
        "pattern": r"(textile|fabric|cloth|cotton|polyester|wool|linen|silk)",
        "default_hs": {
            "us": "6005.00",
            "canada": "6005.00",
            "europe": "6005.00",
            "china": "6005.00",
            "mexico": "6005.00",
        },
        "description": "Textiles and fabrics are classified under chapter 60-63.",
        "tariff_rate": {"us": "5%", "canada": "6%", "europe": "7%", "china": "10%", "mexico": "6%"},
        "compliance": {
            "us": "Fiber content labeling (FTC rule); care instructions required.",
            "canada": "Textile Labeling and Advertising Regulations; fiber percentages.",
            "europe": "EN ISO 1833 fiber composition analysis; care label standards.",
            "china": "GB fiber labeling; testing certification required.",
            "mexico": "IRAM textile labeling; Spanish language requirements.",
        },
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


def classify(
    product_name: str,
    product_description: str,
    country: str,
    trade_direction: str,
    product_attributes: str,
    material: Optional[str] = None,
    origin_country: Optional[str] = None,
    weight_kg: Optional[float] = None,
) -> dict:
    region = normalize_country(country)
    rule = find_category(product_name, product_description, product_attributes)
    
    if rule:
        hs_code = rule["default_hs"].get(region, DEFAULT_HS)
        tariff_rate = rule["tariff_rate"].get(region, DEFAULT_TARIFF)
        compliance_note = rule["compliance"].get(region, "Verify local compliance requirements.")
        classification_reason = (
            f"The product matches '{rule['description']}' for {region.title()} and is therefore classified as HS {hs_code}."
        )
    else:
        hs_code = DEFAULT_HS
        tariff_rate = DEFAULT_TARIFF
        compliance_note = "Consult tariff schedules for accurate classification."
        classification_reason = (
            "Insufficient detail was available to map the product to a specific HS chapter. "
            "Please refine the description or provide detailed product attributes."
        )

    regulatory_notes = f"For {trade_direction.lower()} into {country.title()}: {compliance_note}"
    
    # Build tariff comparison
    tariff_comparison = {}
    if rule:
        tariff_comparison = rule["tariff_rate"].copy()

    result = {
        "hs_code": hs_code,
        "classification_reason": classification_reason,
        "tariff_rate": tariff_rate,
        "regulatory_notes": regulatory_notes,
        "region": region,
        "tariff_comparison": tariff_comparison,
        "material": material or "Not specified",
        "origin_country": origin_country or "Not specified",
        "weight_kg": weight_kg or "Not specified",
    }
    
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="HS Classification generator for trade management use cases.")
    parser.add_argument("--product-name", required=True)
    parser.add_argument("--product-description", default="")
    parser.add_argument("--country", required=True)
    parser.add_argument("--trade-direction", choices=["import", "export"], default="import")
    parser.add_argument("--product-attributes", default="")
    parser.add_argument("--material", default="", help="Primary material (e.g. leather, synthetic, cotton)")
    parser.add_argument("--origin-country", default="", help="Country of manufacture")
    parser.add_argument("--weight-kg", type=float, default=None, help="Product weight in kilograms")
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
        material=args.material or None,
        origin_country=args.origin_country or None,
        weight_kg=args.weight_kg,
    )

    if args.output_json:
        print(json.dumps(result, indent=2))
    else:
        print("HS Code:", result["hs_code"])
        print("Reason:", result["classification_reason"])
        print("Tariff Rate:", result["tariff_rate"])
        print("Regulatory Notes:", result["regulatory_notes"])
        print("Region:", result["region"].title())
        print("Material:", result["material"])
        print("Origin Country:", result["origin_country"])
        print("Weight (kg):", result["weight_kg"])
        if result["tariff_comparison"]:
            print("\nTariff Comparison Across Regions:")
            for reg, rate in result["tariff_comparison"].items():
                print(f"  {reg.title()}: {rate}")


if __name__ == "__main__":
    main()
