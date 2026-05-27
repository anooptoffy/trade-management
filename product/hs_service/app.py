from flask import Flask, request, jsonify
import importlib.util
from pathlib import Path
import sys

# Load the HS classification module from skills path (handles hyphenated folder name)
repo_root = Path(__file__).resolve().parents[2]
module_path = repo_root / "skills" / "hs-classification" / "scripts" / "generate_hs_code.py"

spec = importlib.util.spec_from_file_location("hs_gen", str(module_path))
hs_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hs_mod)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Trade Management HS Classification demo service\n"

@app.route("/classify", methods=["POST"])
def classify_endpoint():
    data = request.get_json(force=True)
    required = ["product_name", "country"]
    for k in required:
        if k not in data:
            return jsonify({"error": f"Missing required field: {k}"}), 400

    result = hs_mod.classify(
        product_name=data.get("product_name", ""),
        product_description=data.get("product_description", ""),
        country=data.get("country", ""),
        trade_direction=data.get("trade_direction", "import"),
        product_attributes=data.get("product_attributes", ""),
    )
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5005, debug=False)
