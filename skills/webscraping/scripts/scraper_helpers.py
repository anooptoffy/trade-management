#!/usr/bin/env python3
"""
Helper utilities for web scraping product data and tariff information.
"""

import re
import json
import requests
from typing import Dict, Optional
from datetime import datetime, timedelta
import hashlib


class ScrapingCache:
    """Simple file-based cache for scraped data with TTL."""

    def __init__(self, cache_file: str = "scraping_cache.json", ttl_hours: int = 24):
        self.cache_file = cache_file
        self.ttl = timedelta(hours=ttl_hours)
        self._load_cache()

    def _load_cache(self):
        try:
            with open(self.cache_file, "r") as f:
                self.cache = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.cache = {}

    def _save_cache(self):
        with open(self.cache_file, "w") as f:
            json.dump(self.cache, f, indent=2)

    def _get_key(self, url: str) -> str:
        return hashlib.md5(url.encode()).hexdigest()

    def get(self, url: str) -> Optional[Dict]:
        key = self._get_key(url)
        if key not in self.cache:
            return None

        cached = self.cache[key]
        cached_time = datetime.fromisoformat(cached["timestamp"])

        if datetime.now() - cached_time > self.ttl:
            del self.cache[key]
            self._save_cache()
            return None

        return cached["data"]

    def set(self, url: str, data: Dict):
        key = self._get_key(url)
        self.cache[key] = {
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "data": data,
        }
        self._save_cache()


def get_headers() -> Dict[str, str]:
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }


def validate_weight(weight_str: str) -> Optional[float]:
    if not weight_str:
        return None

    weight_str = weight_str.lower().strip()
    numbers = re.findall(r"\d+\.?\d*", weight_str)
    if not numbers:
        return None

    weight = float(numbers[0])
    if "lb" in weight_str or "pound" in weight_str:
        weight = weight * 0.453592
    elif "oz" in weight_str or "ounce" in weight_str:
        weight = weight * 0.0283495
    elif "g" in weight_str and "kg" not in weight_str:
        weight = weight / 1000

    if 0.01 <= weight <= 1000:
        return round(weight, 2)

    return None


def validate_material(material_str: str) -> Optional[str]:
    if not material_str:
        return None

    material = material_str.lower().strip()
    valid_materials = [
        "leather",
        "synthetic",
        "cotton",
        "polyester",
        "metal",
        "plastic",
        "wood",
        "rubber",
        "ceramic",
        "glass",
        "paper",
        "fabric",
        "steel",
        "aluminum",
    ]

    if material in valid_materials:
        return material

    for valid in valid_materials:
        if valid in material:
            return valid

    return None


def validate_url(url: str) -> bool:
    pattern = re.compile(
        r"^https?://"
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\\.?|"
        r"localhost|"
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        r"(?::\d+)?"
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return pattern.match(url) is not None


def clean_product_specs(specs: Dict) -> Dict:
    cleaned = {}

    if "name" in specs or "product_name" in specs:
        name_key = "name" if "name" in specs else "product_name"
        cleaned["product_name"] = specs[name_key].strip()

    for key in ["material", "materials", "composition"]:
        if key in specs:
            material = validate_material(specs[key])
            if material:
                cleaned["material"] = material
                break

    for key in ["weight", "weight_kg", "shipping_weight", "item_weight"]:
        if key in specs:
            weight = validate_weight(specs[key])
            if weight:
                cleaned["weight_kg"] = weight
                break

    for key in ["origin", "origin_country", "made_in", "country_of_origin", "manufactured_in"]:
        if key in specs:
            cleaned["origin_country"] = specs[key].strip()
            break

    if "description" in specs:
        cleaned["description"] = specs["description"].strip()
    elif "product_description" in specs:
        cleaned["description"] = specs["product_description"].strip()

    if "url" in specs and validate_url(specs["url"]):
        cleaned["source_url"] = specs["url"]

    return cleaned


def extract_json_ld(html: str) -> Optional[Dict]:
    pattern = re.compile(r"<script[^>]*type=\"application/ld\\+json\"[^>]*>([^<]+)</script>", re.IGNORECASE)
    matches = pattern.findall(html)

    if matches:
        try:
            return json.loads(matches[0])
        except json.JSONDecodeError:
            return None

    return None


def safe_request(url: str, timeout: int = 10, max_retries: int = 3) -> Optional[requests.Response]:
    import time
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=get_headers(), timeout=timeout)
            response.raise_for_status()
            return response

        except requests.exceptions.Timeout:
            if attempt == max_retries - 1:
                print(f"Timeout after {max_retries} attempts: {url}")
                return None
            time.sleep(2 ** attempt)

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429 and attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            print(f"HTTP {e.response.status_code}: {url}")
            return None

        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                print(f"Failed to fetch {url}: {str(e)}")
                return None
            time.sleep(2 ** attempt)

    return None


if __name__ == "__main__":
    print("Testing weight validation:")
    print(f"  '2.5 kg' -> {validate_weight('2.5 kg')} kg")
    print(f"  '5.5 lb' -> {validate_weight('5.5 lb')} kg")
    print(f"  '500 g' -> {validate_weight('500 g')} kg")

    print("\nTesting material validation:")
    print(f"  'Leather' -> {validate_material('Leather')}")
    print(f"  'Polyester blend' -> {validate_material('Polyester blend')}")
    print(f"  'Unknown' -> {validate_material('Unknown')}")
