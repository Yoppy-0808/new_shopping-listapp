from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Vueと通信できるようにする！

# 仮のリストデータ
items = [
    {"id": 1, "name": "Apples", "quantity": 5, "category": "Food", "checked": False},
    {"id": 2, "name": "Laundry Detergent", "quantity": 1, "category": "Household", "checked": False},
]

@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(items)

@app.route("/items", methods=["POST"])
def add_item():
    data = request.json
    new_item = {
        "id": len(items) + 1,
        "name": data["name"],
        "quantity": data["quantity"],
        "category": data["category"],
        "checked": False
    }
    items.append(new_item)
    return jsonify(new_item), 201

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    global items
    items = [item for item in items if item["id"] != item_id]
    return jsonify({"message": "Item deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)
