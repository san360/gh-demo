"""
Flask web application to edit, delete, and save products in products.json.
"""
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
from typing import List, Dict
import os

app = Flask(__name__, static_folder="../static")
CORS(app)

PRODUCTS_FILE = os.path.join(os.path.dirname(__file__), "..", "products.json")

def load_products() -> List[Dict]:
    """Load products from the JSON file."""
    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_products(products: List[Dict]) -> None:
    """Save products to the JSON file."""
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2)

@app.route("/api/products", methods=["GET"])
def get_products():
    """Return the list of products."""
    return jsonify(load_products())

@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id: int):
    """Delete a product by ID."""
    products = load_products()
    products = [p for p in products if p["id"] != product_id]
    save_products(products)
    return jsonify({"success": True})

@app.route("/api/products/<int:product_id>", methods=["PUT"])
def update_product(product_id: int):
    """Update a product by ID."""
    products = load_products()
    data = request.json
    for i, p in enumerate(products):
        if p["id"] == product_id:
            products[i] = data
            break
    save_products(products)
    return jsonify({"success": True})

@app.route("/api/products", methods=["POST"])
def add_product():
    """Add a new product."""
    products = load_products()
    data = request.json
    data["id"] = max((p["id"] for p in products), default=0) + 1
    products.append(data)
    save_products(products)
    return jsonify({"success": True, "id": data["id"]})

@app.route("/")
def serve_index():
    """Serve the frontend index.html."""
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    """Serve static files."""
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    app.run(debug=True)
